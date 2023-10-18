import abc
import contextlib
import dataclasses
import functools
import itertools
import pathlib
from typing import Any, List, Mapping, Optional, Tuple, Union
import weakref

from magma.array import Array, ArrayMeta
from magma.backend.mlir.build_magma_graph import (
    BuildMagmaGrahOpts, build_magma_graph
)
from magma.backend.mlir.builtin import builtin
from magma.backend.mlir.comb import comb
from magma.backend.mlir.common import wrap_with_not_implemented_error
from magma.backend.mlir.compile_to_mlir_opts import CompileToMlirOpts
from magma.backend.mlir.errors import MlirCompilerInternalError
from magma.backend.mlir.graph_lib import Graph
from magma.backend.mlir.hw import hw
from magma.backend.mlir.magma_common import (
    ModuleLike as MagmaModuleLike,
    ValueWrapper as MagmaValueWrapper,
    InstanceWrapper as MagmaInstanceWrapper,
    value_or_type_to_string as magma_value_or_type_to_string,
    visit_value_or_value_wrapper_by_direction as
    visit_magma_value_or_value_wrapper_by_direction,
    tuple_key_to_str as magma_tuple_key_to_str,
)
from magma.backend.mlir.mem_utils import (
    make_mem_reg,
    make_mem_read,
    emit_conditional_assign,
    emit_conditional_assigns,
    make_index_op,
    collect_multiport_memory_operands,
    make_multiport_memory_index_ops,
    make_multiport_memory_read_ops,
)
from magma.backend.mlir.mlir import (
    MlirType, MlirValue, MlirSymbol, MlirAttribute, MlirBlock, push_block,
    push_location
)
from magma.backend.mlir.scoped_name_generator import ScopedNameGenerator
from magma.backend.mlir.sv import sv
from magma.backend.mlir.when_utils import WhenCompiler
from magma.backend.mlir.xmr_utils import get_xmr_paths
from magma.bind2 import maybe_get_bound_instance_info, is_bound_instance
from magma.bit import Bit
from magma.bits import Bits, BitsMeta
from magma.bitutils import clog2, clog2safe
from magma.circuit import AnonymousCircuitType, CircuitKind, DefineCircuitKind
from magma.clock import Reset, ResetN, AsyncReset, AsyncResetN
from magma.common import filter_by_key, assert_false
from magma.compile_guard import get_compile_guard_data
from magma.digital import Digital, DigitalMeta
from magma.inline_verilog_expression import InlineVerilogExpression
from magma.inline_verilog2 import InlineVerilog2
from magma.is_definition import isdefinition
from magma.is_primitive import isprimitive
from magma.linking import (
    has_any_linked_modules,
    get_linked_modules,
    has_default_linked_module,
    get_default_linked_module,
)
from magma.primitives.multiport_memory import MultiportMemory
from magma.primitives.mux import Mux
from magma.primitives.register import Register
from magma.primitives.when import iswhen
from magma.primitives.wire import Wire
from magma.primitives.xmr import XMRSink, XMRSource
from magma.protocol_type import magma_value as get_magma_value
from magma.t import Kind, Type
from magma.tuple import TupleMeta, Tuple as m_Tuple
from magma.value_utils import make_selector, TupleSelector, ArraySelector
from magma.view import PortView


MlirValueList = List[MlirValue]


def _get_defn_or_decl_output_name(
        ctx: 'HardwareModule', defn_or_decl: CircuitKind) -> str:
    metadata = defn_or_decl.coreir_metadata
    try:
        return metadata["verilog_name"]
    except KeyError:
        pass
    name = defn_or_decl.name
    if ctx.opts.user_namespace is not None:
        name = ctx.opts.user_namespace + f"_{name}"
    if ctx.opts.verilog_prefix is not None:
        name = ctx.opts.verilog_prefix + f"{name}"
    return name


def _make_compile_guard_block(compile_guard: Mapping) -> MlirBlock:
    if_def = sv.IfDefOp(compile_guard["condition_str"])
    if compile_guard["type"] == "defined":
        return if_def.then_block
    assert compile_guard["type"] == "undefined"
    return if_def.else_block


def _maybe_set_location_info(op, debug_info):
    if debug_info is None:
        return
    loc = builtin.FileLineColLoc(debug_info.filename, debug_info.lineno, 0)
    op.location = loc


def _make_location_info(debug_info):
    if debug_info is None:
        return builtin.UnknownLoc()
    return builtin.FileLineColLoc(debug_info.filename, debug_info.lineno, 0)


@wrap_with_not_implemented_error
def parse_reset_type(T: Kind) -> Tuple[str, str]:
    if T is Reset:
        return "syncreset", "posedge"
    if T is ResetN:
        return "syncreset", "negedge"
    if T is AsyncReset:
        return "asyncreset", "posedge"
    if T is AsyncResetN:
        return "asyncreset", "negedge"


@wrap_with_not_implemented_error
@functools.lru_cache()
def magma_type_to_mlir_type(type: Kind) -> MlirType:
    type = type.undirected_t
    if issubclass(type, Digital):
        return builtin.IntegerType(1)
    if issubclass(type, Bits):
        return builtin.IntegerType(type.N)
    if issubclass(type, Array):
        if issubclass(type.T, Bit):
            return magma_type_to_mlir_type(Bits[type.N])
        return hw.ArrayType((type.N,), magma_type_to_mlir_type(type.T))
    if issubclass(type, m_Tuple):
        fields = (
            (magma_tuple_key_to_str(k, type), magma_type_to_mlir_type(t))
            for k, t in type.field_dict.items()
        )
        return hw.StructType(tuple(fields))


@wrap_with_not_implemented_error
@functools.lru_cache()
def python_type_to_mlir_type(type_: type) -> MlirType:
    # NOTE(rsetaluri): We only support integer attribtue types right now. All
    # integer parameter types are assumed to be int32's.
    if type_ is int:
        return builtin.IntegerType(32)


@wrap_with_not_implemented_error
def python_value_to_mlir_attribtue(value: Any) -> MlirAttribute:
    # NOTE(rsetaluri): We only support integer attribute types right now.
    if isinstance(value, int):
        return builtin.IntegerAttr(value)


def get_module_interface(
        module: MagmaModuleLike, ctx) -> Tuple[MlirValueList, MlirValueList]:
    operands = []
    results = []
    for port in module.interface.ports.values():
        port = get_magma_value(port)
        visit_magma_value_or_value_wrapper_by_direction(
            port,
            lambda p: operands.append(ctx.get_or_make_mapped_value(p)),
            lambda p: results.append(ctx.get_or_make_mapped_value(p)),
            flatten_all_tuples=ctx.opts.flatten_all_tuples,
        )
    return operands, results


def make_mux(
        ctx: 'HardwareModule',
        data: List[MlirValue],
        select: MlirValue,
        result: MlirValue):
    if ctx.opts.extend_non_power_of_two_muxes:
        closest_power_of_two_size = 2 ** clog2(len(data))
        if closest_power_of_two_size != len(data):
            extension = [data[0]] * (closest_power_of_two_size - len(data))
            data = extension + data
    mlir_type = hw.ArrayType((len(data),), data[0].type)
    array = ctx.new_value(mlir_type)
    hw.ArrayCreateOp(
        operands=data,
        results=[array])
    hw.ArrayGetOp(
        operands=[array, select],
        results=[result])


def get_register_data_and_init(
        ctx: 'HardwareModule', I: Type, operands: List[MlirValue], init: Type):
    T_out, data_out, init_out = [], [], []

    def _visit_input(i):
        T_out.append(type(i))
        data_out.append(operands.pop(0))
        init_out.append(make_selector(i).select(init))

    visit_magma_value_or_value_wrapper_by_direction(
        I,
        _visit_input,
        _visit_input,
        flatten_all_tuples=ctx.opts.flatten_all_tuples
    )
    return T_out, data_out, init_out


def make_hw_param_decl(name: str, value: Any):
    type_ = python_type_to_mlir_type(type(value))
    value = python_value_to_mlir_attribtue(value)
    return hw.ParamDeclAttr(name, type_, value)


def make_hw_instance_op(
        operands: MlirValueList,
        results: MlirValueList,
        name: str,
        module: hw.ModuleOp,
        parameters: Mapping[str, Any] = dict(),
        sym: Optional[MlirSymbol] = None,
        compile_guard: Optional[Mapping] = None,
        attrs: Optional[Mapping] = None,
) -> hw.InstanceOp:
    if compile_guard is not None:
        ctx = push_block(_make_compile_guard_block(compile_guard))
    else:
        ctx = contextlib.nullcontext()
    parameters = [
        make_hw_param_decl(name, value) for name, value in parameters.items()
    ]
    with ctx:
        op = hw.InstanceOp(
            name=name,
            module=module,
            operands=operands,
            results=results,
            parameters=parameters,
            sym=sym)
    if attrs is not None:
        op.attr_dict.update(attrs)
    return op


def resolve_xmr(ctx: 'HardwareModule', xmr: PortView):
    assert isinstance(xmr, PortView)
    mlir_type = magma_type_to_mlir_type(type(xmr)._to_magma_())
    in_out = ctx.new_value(hw.InOutType(mlir_type))
    sv.XMROp(is_rooted=False, path=list(xmr.path()), results=[in_out])
    value = ctx.new_value(mlir_type)
    sv.ReadInOutOp(operands=[in_out], results=[value])
    return value


@dataclasses.dataclass(frozen=True)
class ModuleWrapper:
    module: MagmaModuleLike
    operands: MlirValueList
    results: MlirValueList

    @staticmethod
    def make(module: MagmaModuleLike, ctx) -> 'ModuleWrapper':
        operands, results = get_module_interface(module, ctx)
        return ModuleWrapper(module, operands, results)


class ModuleVisitor:

    class VisitError(RuntimeError):
        pass

    class RevisitedModuleError(VisitError):
        pass

    def __init__(self, graph: Graph, ctx):
        self._graph = graph
        self._ctx = ctx
        self._visited = set()

    @property
    def ctx(self):
        return self._ctx

    @functools.lru_cache()
    def make_constant(
            self, T: Kind, value: Optional[Any] = None) -> MlirValue:
        result = self.ctx.new_value(T)
        if isinstance(T, (DigitalMeta, BitsMeta)):
            value = value if value is not None else 0
            hw.ConstantOp(value=int(value), results=[result])
            return result
        if isinstance(T, ArrayMeta):
            if isinstance(T.T, DigitalMeta):
                return self.make_constant(Bits[T.N], value)
            value = value if value is not None else (None for _ in range(T.N))
            operands = [self.make_constant(T.T, v) for v in value]
            hw.ArrayCreateOp(operands=operands, results=[result])
            return result
        if isinstance(T, TupleMeta):
            fields = list(T.field_dict.items())
            value = value if value is not None else {k: None for k, _ in fields}
            operands = [self.make_constant(t, value[k]) for k, t in fields]
            hw.StructCreateOp(operands=operands, results=[result])
            return result
        raise TypeError(T)

    @functools.lru_cache()
    def make_array_ref(self, arr: MlirValue, i: Union[int, tuple]) -> MlirValue:
        if isinstance(i, tuple):  # slice
            start, stop, step = i
            assert step in [1, None], "Expected step 1 slice"
            n = stop - start
        else:
            start = i
            n = 1

        if isinstance(arr.type, builtin.IntegerType):
            operand = self.ctx.new_value(builtin.IntegerType(n))
            comb.ExtractOp(operands=[arr], results=[operand], lo=start)
            return operand

        num_sel_bits = clog2safe(arr.type.dims[0])
        start = self.make_constant(Bits[num_sel_bits], start)

        if isinstance(i, tuple):
            operand = self.ctx.new_value(hw.ArrayType((n, ), arr.type.T))
            hw.ArraySliceOp(operands=[arr, start], results=[operand])
            return operand

        operand = self.ctx.new_value(arr.type.T)
        hw.ArrayGetOp(operands=[arr, start], results=[operand])
        return operand

    @functools.lru_cache()
    def make_struct_ref(
        self,
        struct: MlirValue,
        key: Union[int, str]
    ) -> MlirValue:
        if isinstance(key, int):
            key = f"_{key}"
        operand = self.ctx.new_value(struct.type.get_field(key))
        hw.StructExtractOp(field=key, operands=[struct], results=[operand])
        return operand

    def make_concat(self, operands, result):
        """Collect single elements and put them into an array create op,
        this allows slices to be concatenated with the surround elements.
        """
        T = result.type
        if isinstance(T, builtin.IntegerType):
            # comb concat supports single elem/slices
            return comb.ConcatOp(operands=operands, results=[result])
        new_operands = []  # packed single elements
        i = 0
        while i < len(operands):
            if i == len(operands):
                break
            if operands[i].type != T.T:
                # Found slice
                new_operands.append(operands[i])
                i += 1
                continue

            # Collect elements until we encounter a slice or the end.
            elems = []
            while i < len(operands) and operands[i].type == T.T:
                elems.append(operands[i])
                i += 1

            if len(elems) == len(operands):
                # Found a whole create op
                return hw.ArrayCreateOp(operands=elems, results=[result])

            # Add create for current elements
            elems_T = hw.ArrayType((len(elems),), T.T)
            curr_result = self.ctx.new_value(elems_T)
            hw.ArrayCreateOp(operands=elems, results=[curr_result])
            new_operands.append(curr_result)

        hw.ArrayConcatOp(operands=new_operands, results=[result])

    @wrap_with_not_implemented_error
    def visit_coreir_mem(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert (
            defn.coreir_name == "mem"
            or defn.coreir_name == "sync_read_mem"
        )
        # TODO(rsetaluri): Add support for initialization.
        if defn.coreir_genargs["has_init"]:
            raise NotImplementedError("coreir.mem init not supported")
        width = defn.coreir_genargs["width"]
        depth = defn.coreir_genargs["depth"]
        is_sync_read_mem = (defn.coreir_name == "sync_read_mem")
        raddr, waddr, wdata, clk, wen = module.operands[:5]
        rdata = module.results[0]
        mem = make_mem_reg(
            self._ctx, inst.name, depth, builtin.IntegerType(width)
        )
        # Register read logic.
        read = make_index_op(self._ctx, mem, raddr)
        read_reg, read_temp = make_mem_read(
            self._ctx, read, rdata, is_sync_read_mem
        )
        # Register write logic.
        write = make_index_op(self._ctx, mem, waddr)
        # Always logic.
        always = sv.AlwaysFFOp(operands=[clk], clock_edge="posedge").body_block
        with push_block(always):
            emit_conditional_assign(write, wdata, wen)
            if is_sync_read_mem:
                ren = module.operands[-1]
                emit_conditional_assign(read_reg, read_temp, ren)
        return True

    @wrap_with_not_implemented_error
    def visit_coreir_not(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_name == "not"
        neg_one = self.make_constant(type(inst.I), -1)
        comb.BaseOp(
            op_name="xor",
            operands=[neg_one, module.operands[0]],
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_coreir_reg(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_name == "reg" or defn.coreir_name == "reg_arst"
        reg = self.ctx.new_value(
            hw.InOutType(magma_type_to_mlir_type(type(defn.O))))
        sv.RegOp(name=inst.name, results=[reg])
        clock_edge = "posedge"
        has_reset = (defn.coreir_name == "reg_arst")
        operands = [module.operands[1]]
        attrs = dict(clock_edge=clock_edge)
        if has_reset:
            reset_type = "asyncreset"
            arst_posedge = defn.coreir_configargs["arst_posedge"]
            reset_edge = "posedge" if arst_posedge else "negedge"
            operands.append(module.operands[2])
            attrs.update(dict(reset_type=reset_type, reset_edge=reset_edge))
        always = sv.AlwaysFFOp(operands=operands, **attrs)
        init = defn.coreir_configargs["init"].value
        const = self.make_constant(type(defn.I), init)
        with push_block(always.body_block):
            sv.PAssignOp(operands=[reg, module.operands[0]])
        if has_reset:
            always.operands.append(module.operands[1])
            with push_block(always.reset_block):
                sv.PAssignOp(operands=[reg, const])
        if not self._ctx.opts.disable_initial_blocks:
            with push_block(sv.InitialOp()):
                sv.BPAssignOp(operands=[reg, const])
        sv.ReadInOutOp(operands=[reg], results=module.results.copy())
        return True

    @wrap_with_not_implemented_error
    def visit_coreir_reduce(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert (defn.coreir_name in ("orr", "andr", "xorr"))
        size = len(defn.I)
        if defn.coreir_name == "orr":
            const = self.make_constant(type(defn.I), value=0)
            comb.ICmpOp(
                predicate="ne",
                operands=[module.operands[0], const],
                results=module.results)
        elif defn.coreir_name == "andr":
            const = self.make_constant(type(defn.I), value=-1)
            comb.ICmpOp(
                predicate="eq",
                operands=[module.operands[0], const],
                results=module.results)
        elif defn.coreir_name == "xorr":
            comb.ParityOp(
                operands=module.operands,
                results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_coreir_wire(self, module: ModuleWrapper) -> bool:
        inst = module.module

        def _visit(value, counter):
            index = next(counter)
            mlir_type = hw.InOutType(module.operands[index].type)
            wire = self.ctx.new_value(mlir_type)
            name = inst.name
            # TODO(rsetaluri): Making a selector and inspecting it in order to
            # find the name is a kind of hacky way to get the qualified name of
            # the sub-field of the value. Instead we should have a common API
            # (what "qualifiedname" really should be...) to obtain this name.
            selector = make_selector(value)
            if isinstance(selector, (TupleSelector, ArraySelector)):
                name += str(selector).replace(".", "_")
            else:
                assert index == 0
            sym = self._ctx.parent.get_or_make_mapped_symbol(
                value, name=f"{self._ctx.name}.{name}", force=True
            )
            sv.WireOp(results=[wire], name=name, sym=sym)
            sv.AssignOp(operands=[wire, module.operands[index]])
            sv.ReadInOutOp(operands=[wire], results=[module.results[index]])

        counter = itertools.count()
        visit_magma_value_or_value_wrapper_by_direction(
            inst.I,
            lambda v: _visit(v, counter),
            assert_false,
            flatten_all_tuples=self._ctx.opts.flatten_all_tuples,
        )
        return True

    @wrap_with_not_implemented_error
    def visit_coreir_primitive(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert (
            defn.coreir_lib == "coreir"
            or defn.coreir_lib == "corebit"
            or defn.coreir_lib == "memory"
        )
        if (
            defn.coreir_name == "mem"
            or defn.coreir_name == "sync_read_mem"
        ):
            return self.visit_coreir_mem(module)
        if defn.coreir_name == "not":
            return self.visit_coreir_not(module)
        if defn.coreir_name in (
                "eq", "ult", "eq", "ne", "slt", "sle", "sgt", "sge", "ult",
                "ule", "ugt", "uge",
        ):
            comb.ICmpOp(
                predicate=defn.coreir_name,
                operands=module.operands,
                results=module.results)
            return True
        if defn.coreir_name in ("reg", "reg_arst"):
            return self.visit_coreir_reg(module)
        if defn.coreir_name in ("orr", "andr", "xorr"):
            return self.visit_coreir_reduce(module)
        if defn.coreir_name == "wire":
            return self.visit_coreir_wire(module)
        if defn.coreir_name == "wrap":
            return self.visit_coreir_wire(module)
        if defn.coreir_name == "term":
            return True
        if defn.coreir_name == "undriven":
            mlir_type = hw.InOutType(module.results[0].type)
            wire = self.ctx.new_value(mlir_type)
            sym = self._ctx.parent.get_or_make_mapped_symbol(
                inst, name=f"{self._ctx.name}.{inst.name}", force=True)
            sv.WireOp(results=[wire], sym=sym)
            sv.ReadInOutOp(operands=[wire], results=module.results)
            return True
        if defn.coreir_name == "neg":
            zero = self.make_constant(type(inst.I), 0)
            comb.BaseOp(
                op_name="sub",
                operands=[zero, module.operands[0]],
                results=module.results)
            return True
        op_name = defn.coreir_name
        if op_name == "ashr":
            op_name = "shrs"
        if op_name == "lshr":
            op_name = "shru"
        if op_name == "udiv":
            op_name = "divu"
        if op_name == "sdiv":
            op_name = "divs"
        comb.BaseOp(
            op_name=op_name,
            operands=module.operands,
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_muxn(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_name == "muxn"
        data = self.ctx.new_value(defn.I.data)
        sel = self.ctx.new_value(defn.I.sel)
        # NOTE(rsetaluri): This is a specialized code path for the case where
        # all tuples are flattened.
        if self._ctx.opts.flatten_all_tuples:
            hw.ArrayGetOp(
                operands=module.operands.copy(),
                results=module.results.copy())
            return True
        hw.StructExtractOp(
            field="data",
            operands=module.operands.copy(),
            results=[data])
        hw.StructExtractOp(
            field="sel",
            operands=module.operands.copy(),
            results=[sel])
        hw.ArrayGetOp(
            operands=[data, sel],
            results=module.results.copy())
        return True

    @wrap_with_not_implemented_error
    def visit_lutN(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_name == "lutN"
        init = defn.coreir_configargs["init"]
        consts = [self.make_constant(Bit, b) for b in reversed(init)]
        mlir_type = hw.ArrayType((len(init),), builtin.IntegerType(1))
        array = self.ctx.new_value(mlir_type)
        hw.ArrayCreateOp(
            operands=consts,
            results=array)
        hw.ArrayGetOp(
            operands=[array, module.operands[0]],
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_commonlib_primitive(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert defn.coreir_lib == "commonlib"
        if defn.coreir_name == "muxn":
            return self.visit_muxn(module)
        if defn.coreir_name == "lutN":
            return self.visit_lutN(module)

    @wrap_with_not_implemented_error
    def visit_array_get(self, module: ModuleWrapper) -> bool:
        inst_wrapper = module.module
        T = inst_wrapper.attrs["T"]
        size = T.N
        operands = module.operands
        index = inst_wrapper.attrs["index"]
        # NOTE(rsetaluri): This is "hacky" way to emit IR for ArrayGet(Array[1,
        # _], _) to work, since MLIR doesn't support i0 integer
        # constants. Instead, we form an Array[2, _] using a concat with a dummy
        # (const) element, and then perform ArrayGet on the Array[2, _] type
        # using an i1 constant.
        # TODO(rsetaluri): Figure out how to emit hw.array_get for
        # !hw.array_type<1x_> types.
        if size == 1:
            assert index == 0
            other = self.make_constant(T)
            concat_type = hw.ArrayType((2,), operands[0].type.T)
            concat = self.ctx.new_value(concat_type)
            hw.ArrayConcatOp(
                operands=[other, operands[0]],
                results=[concat])
            operands = [concat]
            size = 2
        num_sel_bits = clog2(size)
        index = self.make_constant(Bits[num_sel_bits], index)
        hw.ArrayGetOp(
            operands=(operands + [index]),
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_array_slice(self, module: ModuleWrapper) -> bool:
        inst_wrapper = module.module
        T = inst_wrapper.attrs["T"]
        size = T.N
        operands = module.operands
        lo = inst_wrapper.attrs["lo"]
        num_sel_bits = clog2(size)
        lo = self.make_constant(Bits[num_sel_bits], lo)
        hw.ArraySliceOp(
            operands=(operands + [lo]),
            results=module.results)
        return True

    @wrap_with_not_implemented_error
    def visit_when(self, module: ModuleWrapper) -> bool:
        return WhenCompiler(self, module).compile()

    @wrap_with_not_implemented_error
    def visit_multiport_memory(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        clk = module.operands[0]
        read_ports_out = module.results
        read_port_len = 1 + defn.has_read_enable
        read_ports = collect_multiport_memory_operands(
            module.operands, 1, defn.num_read_ports, read_port_len
        )
        write_ports = collect_multiport_memory_operands(
            module.operands,
            1 + defn.num_read_ports * read_port_len,
            defn.num_write_ports,
            3
        )
        elt_type = hw.InOutType(magma_type_to_mlir_type(defn.T))
        mem = make_mem_reg(self._ctx, inst.name, defn.height, elt_type.T)
        read_results = make_multiport_memory_index_ops(
            self._ctx, read_ports, mem
        )
        read_targets = make_multiport_memory_read_ops(
            self._ctx, read_results, read_ports, read_ports_out
        )
        write_results = make_multiport_memory_index_ops(
            self._ctx, write_ports, mem
        )
        write_targets = (
            (write_results[i], *write_ports[i][1:3])
            for i in range(len(write_results))
        )
        always = sv.AlwaysFFOp(operands=[clk], clock_edge="posedge").body_block
        with push_block(always):
            emit_conditional_assigns(write_targets)
            if len(read_targets):
                emit_conditional_assigns(read_targets)
        return True

    @wrap_with_not_implemented_error
    def visit_primitive(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert isprimitive(defn)
        if (
            defn.coreir_lib == "coreir"
            or defn.coreir_lib == "corebit"
            or defn.coreir_lib == "memory"
        ):
            return self.visit_coreir_primitive(module)
        if defn.coreir_lib == "commonlib":
            return self.visit_commonlib_primitive(module)
        if isinstance(defn, MultiportMemory):
            return self.visit_multiport_memory(module)
        if isinstance(defn, InlineVerilogExpression):
            assert len(module.operands) == 0
            assert len(module.results) > 0
            sv.VerbatimExprOp(
                operands=list(),
                results=module.results,
                expr=defn.expr,
            )
            return True
        if isinstance(defn, InlineVerilog2):
            sv.VerbatimOp(string=defn.expr, operands=module.operands)
            return True
        if iswhen(defn):
            return self.visit_when(module)

    @wrap_with_not_implemented_error
    def visit_magma_wire(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert isinstance(defn, Wire) and not defn.flattened
        return self.visit_coreir_wire(module)

    @wrap_with_not_implemented_error
    def visit_magma_mux(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert isinstance(defn, Mux)
        # NOTE(rsetaluri): This is a round-about way to get the height while
        # magma.Mux does not store those parameters. That should be fixed in
        # magma/primitives/mux.py.
        height = len(list(filter(
            lambda p: "I" in p.name.name, defn.interface.outputs())))
        data, select = module.operands[:-1], module.operands[-1]
        # NOTE(rsetaluri): This is a specialized code path for the case where
        # all tuples are flattened.
        if self._ctx.opts.flatten_all_tuples and len(data) != height:
            assert len(data) % height == 0
            stride = len(data) // height
            assert len(module.results) == stride
            for i in range(stride):
                inputs = list(reversed(data[i::stride]))
                make_mux(self._ctx, inputs, select, module.results[i])
            return True
        # NOTE(rsetaluri): Reversing data needs to be done *after* we check for
        # tuple flattening. Otherwise the tuple field ordering gets reversed as
        # well.
        data = list(reversed(data))
        make_mux(self._ctx, data, select, module.results[0])
        return True

    @wrap_with_not_implemented_error
    def visit_magma_register(self, module: ModuleWrapper) -> bool:
        # NOTE(rsetaluri): Refactoring this compilation into the make_register
        # and get_register_data_and_init functions is necessary to support
        # flatten_all_tuples=True. make_register works for arbitrary types of
        # inputs, so we can either invoke it once for the top-level type or call
        # it on all flattened parts. get_register_data_and_init associates the
        # operands with init values (and magma type), so that flattened and
        # unflattened tuples can be treated uniformly.

        def make_register(T, data, init, result):
            reg = self.ctx.new_value(hw.InOutType(data.type))
            sv.RegOp(name=inst.name, results=[reg])
            always = sv.AlwaysFFOp(operands=always_operands, **attrs)
            const = self.make_constant(T, init)
            with push_block(always.body_block):
                ctx = contextlib.nullcontext()
                if has_enable:
                    ctx = push_block(sv.IfOp(operands=[enable]).then_block)
                with ctx:
                    sv.PAssignOp(operands=[reg, data])
            if has_reset:
                with push_block(always.reset_block):
                    sv.PAssignOp(operands=[reg, const])
            if not self._ctx.opts.disable_initial_blocks:
                with push_block(sv.InitialOp()):
                    sv.BPAssignOp(operands=[reg, const])
            sv.ReadInOutOp(operands=[reg], results=[result])

        inst = module.module
        defn = type(inst)
        clock_edge = "posedge"
        has_reset = defn.reset_type is not None
        # NOTE(resetaluri): This is a hack until
        # magma/primitives/register.py:Register is updated to store this
        # generator parameter directly.
        has_enable = "CE" in defn.interface.ports
        operands = module.operands.copy()
        T, data, init = get_register_data_and_init(
            self._ctx, defn.I, operands, defn.init)
        assert len(data) == len(init)
        assert len(data) == len(T)
        assert len(data) == len(module.results)
        if has_enable:
            enable = operands[0]
            clk = operands[1]
        else:
            clk = operands[0]
        always_operands = [clk]
        attrs = dict(clock_edge=clock_edge)
        if has_reset:
            reset = operands[-1]
            always_operands.append(reset)
            reset_type, reset_edge = parse_reset_type(defn.reset_type)
            attrs.update(dict(reset_type=reset_type, reset_edge=reset_edge))
        for T_i, data_i, init_i, result_i in zip(T, data, init, module.results):
            make_register(T_i, data_i, init_i, result_i)
        return True

    @wrap_with_not_implemented_error
    def visit_magma_xmr_sink(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert isinstance(defn, XMRSink)
        xmr = defn.value
        try:
            self._ctx.parent.xmr_paths[xmr]
        except KeyError:
            pass
        else:
            return True
        paths = get_xmr_paths(self._ctx, xmr)
        self._ctx.parent.xmr_paths[xmr] = paths
        return True

    @wrap_with_not_implemented_error
    def visit_magma_xmr_source(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        assert isinstance(defn, XMRSource)
        xmr = defn.value
        paths = self._ctx.parent.xmr_paths[xmr]
        base = defn.value.parent_view.path()
        for result, path in zip(module.results, paths):
            in_out = self.ctx.new_value(hw.InOutType(result.type))
            path = base + path
            sv.XMROp(is_rooted=False, path=path, results=[in_out])
            sv.ReadInOutOp(operands=[in_out], results=[result])
        return True

    @wrap_with_not_implemented_error
    def visit_inline_verilog(self, module: ModuleWrapper) -> bool:
        inst = module.module
        defn = type(inst)
        inline_verilog_strs = defn.inline_verilog_strs
        assert inline_verilog_strs
        for string, references in inline_verilog_strs:
            # NOTE(rsetaluri): We assume that the order of the references
            # matches the order of the ports to the encapsulating inline verilog
            # module (which is safe as of phanrahan/magma:d3e8c95).
            replacement_map = {
                k: f"{{{{{i}}}}}" for i, k in enumerate(references)
            }
            # NOTE(rsetaluri): We need to traverse the replacements in order of
            # decreasing key-length (i.e. strlen) in order to ensure that we
            # don't replace e.g. "key10" with "{repl}0" where both "key1" and
            # "key10" are keys.
            replacements = reversed(sorted(
                replacement_map.items(), key=lambda kv: len(kv[1])))
            for k, v in replacements:
                k = "{" + k + "}"
                string = string.replace(k, v)
            sv.VerbatimOp(operands=module.operands, string=string)
        return True

    @wrap_with_not_implemented_error
    def visit_instance(self, module: ModuleWrapper) -> bool:
        inst = module.module
        assert isinstance(inst, AnonymousCircuitType)
        defn = type(inst)
        elaborate_magma_registers = self._ctx.opts.elaborate_magma_registers
        if isinstance(defn, Wire) and not defn.flattened:
            return self.visit_magma_wire(module)
        if isinstance(defn, Mux):
            return self.visit_magma_mux(module)
        if isinstance(defn, Register) and not elaborate_magma_registers:
            return self.visit_magma_register(module)
        if isinstance(defn, XMRSink):
            return self.visit_magma_xmr_sink(module)
        if isinstance(defn, XMRSource):
            return self.visit_magma_xmr_source(module)
        if getattr(defn, "inline_verilog_strs", []):
            return self.visit_inline_verilog(module)
        if isprimitive(defn):
            return self.visit_primitive(module)
        module_type = self._ctx.parent.get_hardware_module(defn).hw_module
        parameters = filter_by_key(
            lambda key: key not in ["name", "locl"],
            inst.kwargs
        )
        compile_guard = get_compile_guard_data(inst)
        sym = None
        attrs = {}
        if is_bound_instance(inst):
            sym = self._ctx.parent.get_or_make_mapped_symbol(
                inst, name=f"{inst.defn.name}.{inst.name}", force=True
            )
            attrs["doNotPrint"] = builtin.BoolAttr(True)
        make_hw_instance_op(
            name=inst.name,
            module=module_type,
            operands=module.operands,
            results=module.results,
            sym=sym,
            parameters=parameters,
            compile_guard=compile_guard,
            attrs=attrs)
        return True

    @wrap_with_not_implemented_error
    def visit_instance_wrapper(self, module: ModuleWrapper) -> bool:
        inst_wrapper = module.module
        assert isinstance(inst_wrapper, MagmaInstanceWrapper)
        if inst_wrapper.name.startswith("magma_array_get_op_"):
            T = inst_wrapper.attrs["T"]
            if isinstance(T, BitsMeta) or issubclass(T.T, Bit):
                comb.ExtractOp(
                    operands=module.operands,
                    results=module.results,
                    lo=inst_wrapper.attrs["index"])
                return True
            return self.visit_array_get(module)
        if inst_wrapper.name.startswith("magma_array_slice_op_"):
            T = inst_wrapper.attrs["T"]
            if isinstance(T, BitsMeta) or issubclass(T.T, Bit):
                comb.ExtractOp(
                    operands=module.operands,
                    results=module.results,
                    lo=inst_wrapper.attrs["lo"])
                return True
            return self.visit_array_slice(module)
        if inst_wrapper.name.startswith("magma_array_create_op"):
            self.make_concat(
                list(reversed(module.operands)),
                module.results[0]
            )
            return True
        if inst_wrapper.name.startswith("magma_tuple_get_op"):
            index = magma_tuple_key_to_str(
                inst_wrapper.attrs["index"],
                inst_wrapper.attrs["T"]
            )
            hw.StructExtractOp(
                field=index,
                operands=module.operands,
                results=module.results)
            return True
        if inst_wrapper.name.startswith("magma_tuple_create_op"):
            hw.StructCreateOp(
                operands=module.operands,
                results=module.results)
            return True
        is_const = (
            inst_wrapper.name.startswith("magma_bit_constant_op") or
            inst_wrapper.name.startswith("magma_bits_constant_op"))
        if is_const:
            value = inst_wrapper.attrs["value"]
            hw.ConstantOp(value=int(value), results=module.results)
            return True

    @wrap_with_not_implemented_error
    def visit_module(self, module: ModuleWrapper) -> bool:
        if isinstance(module.module, DefineCircuitKind):
            return True
        if isinstance(module.module, AnonymousCircuitType):
            with push_location(_make_location_info(module.module.debug_info)):
                return self.visit_instance(module)
        if isinstance(module.module, MagmaInstanceWrapper):
            return self.visit_instance_wrapper(module)

    def _process_magma_module(self, magma_module: MagmaModuleLike):
        if not self._graph.has_node(magma_module):
            return
        for predecessor in self._graph.predecessors(magma_module):
            if predecessor in self._visited:
                continue
            self.visit(predecessor)
        for src, _, data in self._graph.in_edges(magma_module, data=True):
            info = data["info"]
            src_port, dst_port = info["src"], info["dst"]
            src_value = self._ctx.get_or_make_mapped_value(src_port)
            self._ctx.set_mapped_value(dst_port, src_value)

    def visit(self, module: MagmaModuleLike):
        if module in self._visited:
            raise ModuleVisitor.RevisitedModuleError(module)
        self._visited.add(module)
        self._process_magma_module(module)
        self.visit_module(ModuleWrapper.make(module, self._ctx))
        instances = getattr(module, "instances", [])
        for inst in instances:
            if inst in self._visited:
                continue
            self.visit(inst)


def treat_as_primitive(
        defn_or_decl: CircuitKind,
        ctx: 'HardwareModule'
) -> bool:
    # NOTE(rsetaluri): This is a round-about way to mark new types as
    # primitives. These definitions should actually be marked as primitives.
    elaborate_magma_registers = ctx.opts.elaborate_magma_registers
    if isprimitive(defn_or_decl):
        return True
    if isinstance(defn_or_decl, Mux):
        return True
    if isinstance(defn_or_decl, Register) and not elaborate_magma_registers:
        return True
    if getattr(defn_or_decl, "inline_verilog_strs", []):
        return True
    return False


def treat_as_definition(defn_or_decl: CircuitKind) -> bool:
    if not isdefinition(defn_or_decl):
        return False
    if getattr(defn_or_decl, "verilog", ""):
        return False
    if getattr(defn_or_decl, "verilogFile", ""):
        return False
    return True


class BindProcessorInterface(abc.ABC):
    def __init__(self, ctx: 'HardwareModule', defn: CircuitKind):
        self._ctx = ctx
        self._defn = defn

    @abc.abstractmethod
    def preprocess(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def process(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def postprocess(self):
        raise NotImplementedError()


class NativeBindProcessor(BindProcessorInterface):
    def preprocess(self):
        for bind_module in self._defn.bind_modules:
            # TODO(rsetaluri): Here we should check if @bind_module has already
            # been compiled, in the case that the bound module is either used
            # multiple times or is also a "normal" module that was compiled
            # elsewhere. Currently, the `set_hardware_module` call will raise an
            # error if @bind_module has been compiled already.
            hardware_module = self._ctx.parent.new_hardware_module(bind_module)
            hardware_module.compile()
            assert hardware_module.hw_module is not None
            self._ctx.parent.set_hardware_module(bind_module, hardware_module)

    @wrap_with_not_implemented_error
    def _resolve_arg(self, arg) -> MlirValue:
        if isinstance(arg, Type):
            return self._ctx.get_mapped_value(arg)
        if isinstance(arg, PortView):
            return resolve_xmr(self._ctx, arg)

    def process(self):
        self._syms = []
        for bind_module, (args, _) in self._defn.bind_modules.items():
            operands = []
            for port in self._defn.interface.ports.values():
                port = get_magma_value(port)
                visit_magma_value_or_value_wrapper_by_direction(
                    port,
                    lambda p: operands.append(self._ctx.get_mapped_value(p)),
                    lambda p: operands.append(self._ctx.get_mapped_value(p)),
                    flatten_all_tuples=self._ctx.opts.flatten_all_tuples,
                )
            operands += list(map(self._resolve_arg, args))
            inst_name = f"{bind_module.name}_inst"
            sym = self._ctx.parent.get_or_make_mapped_symbol(
                (self._defn, bind_module),
                name=f"{self._defn.name}.{inst_name}",
                force=True)
            module = self._ctx.parent.get_hardware_module(bind_module)
            inst = hw.InstanceOp(
                name=inst_name,
                module=module.hw_module,
                operands=operands,
                results=[],
                sym=sym)
            inst.attr_dict["doNotPrint"] = builtin.BoolAttr(True)
            self._syms.append(sym)

    def postprocess(self):
        defn_sym = self._ctx.parent.get_mapped_symbol(self._defn)
        for sym in self._syms:
            instance = hw.InnerRefAttr(defn_sym, sym)
            sv.BindOp(instance=instance)
        for instance in self._defn.instances:
            bound_instance_info = maybe_get_bound_instance_info(instance)
            if bound_instance_info is None:
                continue
            inst_sym = self._ctx.parent.get_mapped_symbol(instance)
            ref = hw.InnerRefAttr(defn_sym, inst_sym)
            with contextlib.ExitStack() as stack:
                for compile_guard_info in bound_instance_info.compile_guards:
                    block = _make_compile_guard_block(
                        dataclasses.asdict(compile_guard_info)
                    )
                    stack.enter_context(push_block(block))
                sv.BindOp(instance=ref)


class CoreIRBindProcessor(BindProcessorInterface):
    def preprocess(self):
        return

    def process(self):
        for name, content in self._defn.compiled_bind_modules.items():
            path = pathlib.Path(self._ctx.opts.basename).parent
            filename = path / f"{name}.sv"
            with open(filename, "w") as f:
                f.write(content)
            self._ctx.parent.add_external_bind_file(filename.name)

    def postprocess(self):
        return


def _make_bind_processor(ctx: 'HardwareModule', defn: CircuitKind):
    if ctx.opts.use_native_bind_processor:
        return NativeBindProcessor(ctx, defn)
    return CoreIRBindProcessor(ctx, defn)


def _visit_linked_module(
        ctx: 'HardwareModule', decl: CircuitKind, op: hw.ModuleOp):
    # In order to emit a linked module, we perform the following steps:
    #   (1) Declare a wire for each output of the module.
    #   (2) For each linked module, first enter an `ifdef block.
    #       (a) Instantiate the linked target.
    #       (b) Assign the wires with the outputs of the instance.
    #       (c) Enter the `else of the `ifdef block.
    #   (3) If we have a default link target, perform (2a-b).
    module = ModuleWrapper.make(decl, ctx)
    wires = {
        output: ctx.new_value(hw.InOutType(output.type))
        for output in module.operands
    }

    def _process_target(defn):
        hw_module = ctx.parent.get_hardware_module(defn).hw_module
        results = [ctx.new_value(output.type) for output in module.operands]
        make_hw_instance_op(
            name=f"{defn.name}_inst",
            module=hw_module,
            operands=module.results,
            results=results,
        )
        for result, wire in zip(results, wires.values()):
            sv.AssignOp(operands=[wire, result])

    with push_block(op):
        for output, wire in wires.items():
            sv.WireOp(results=[wire])
            sv.ReadInOutOp(operands=[wire], results=[output])
        with contextlib.ExitStack() as stack:
            for key, linked_module in get_linked_modules(decl).items():
                if_def = sv.IfDefOp(key)
                stack.enter_context(push_block(if_def.then_block))
                _process_target(linked_module)
                stack.enter_context(push_block(if_def.else_block))
            if has_default_linked_module(decl):
                default_linked_module = get_default_linked_module(decl)
                _process_target(default_linked_module)
        hw.OutputOp(operands=module.operands)
    return op


class HardwareModule:
    def __init__(
            self, magma_defn_or_decl: CircuitKind,
            parent: weakref.ReferenceType, opts: CompileToMlirOpts):
        self._magma_defn_or_decl = magma_defn_or_decl
        self._parent = parent
        self._opts = opts
        self._hw_module = None
        self._name_gen = ScopedNameGenerator(disallow_duplicates=False)
        self._value_map = {}

    @property
    def magma_defn_or_decl(self) -> CircuitKind:
        return self._magma_defn_or_decl

    @property
    def parent(self):
        return self._parent()

    @property
    def opts(self) -> CompileToMlirOpts:
        return self._opts

    @property
    def hw_module(self) -> hw.ModuleOpBase:
        return self._hw_module

    @property
    def name(self) -> str:
        return self._magma_defn_or_decl.name

    def get_mapped_value(self, port: Type) -> MlirValue:
        return self._value_map[port]

    def get_or_make_mapped_value(self, port: Type, **kwargs) -> MlirValue:
        try:
            return self._value_map[port]
        except KeyError:
            pass
        self._value_map[port] = value = self.new_value(port, **kwargs)
        return value

    def set_mapped_value(self, port: Type, value: MlirValue):
        if port in self._value_map:
            raise ValueError(f"Port {port} already mapped")
        self._value_map[port] = value

    def new_value(
            self, value_or_type: Union[Type, Kind, MlirType],
            **kwargs) -> MlirValue:
        if isinstance(value_or_type, Type):
            mlir_type = magma_type_to_mlir_type(type(value_or_type))
        elif isinstance(value_or_type, Kind):
            mlir_type = magma_type_to_mlir_type(value_or_type)
        elif isinstance(value_or_type, MlirType):
            mlir_type = value_or_type
        elif isinstance(value_or_type, MagmaValueWrapper):
            mlir_type = magma_type_to_mlir_type(value_or_type.T)
        else:
            raise TypeError(value_or_type)
        name = self._name_gen(**kwargs)
        return MlirValue(mlir_type, name)

    def compile(self):
        self._hw_module = self._compile()
        if self._hw_module is None:
            return
        self._add_module_parameters(self._hw_module)
        _maybe_set_location_info(
            self._hw_module,
            self._magma_defn_or_decl.debug_info
        )

    def _compile(self) -> hw.ModuleOpBase:
        if treat_as_primitive(self._magma_defn_or_decl, self):
            return

        def new_values(fn, ports):
            namer = magma_value_or_type_to_string
            return [
                fn(port, name=namer(port), force=True)
                for port in map(get_magma_value, ports)
            ]

        i, o = [], []
        for port in self._magma_defn_or_decl.interface.ports.values():
            port = get_magma_value(port)
            visit_magma_value_or_value_wrapper_by_direction(
                port, i.append, o.append,
                flatten_all_tuples=self._opts.flatten_all_tuples,
            )
        inputs = new_values(self.get_or_make_mapped_value, o)
        named_outputs = new_values(self.new_value, i)
        defn_or_decl_output_name = _get_defn_or_decl_output_name(
            self, self._magma_defn_or_decl)
        name = self.parent.get_or_make_mapped_symbol(
            self._magma_defn_or_decl,
            name=defn_or_decl_output_name, force=True)
        if has_any_linked_modules(self._magma_defn_or_decl):
            op = hw.ModuleOp(
                name=name,
                operands=inputs,
                results=named_outputs,
            )
            return _visit_linked_module(self, self._magma_defn_or_decl, op)
        if not treat_as_definition(self._magma_defn_or_decl):
            return hw.ModuleExternOp(
                name=name,
                operands=inputs,
                results=named_outputs)
        bind_processor = _make_bind_processor(self, self._magma_defn_or_decl)
        bind_processor.preprocess()
        op = hw.ModuleOp(
            name=name,
            operands=inputs,
            results=named_outputs)
        build_magma_graph_opts = BuildMagmaGrahOpts(
            self._opts.flatten_all_tuples)
        graph = build_magma_graph(
            self._magma_defn_or_decl, build_magma_graph_opts)
        visitor = ModuleVisitor(graph, self)
        with push_block(op):
            try:
                visitor.visit(self._magma_defn_or_decl)
            except ModuleVisitor.VisitError:
                raise MlirCompilerInternalError(visitor)
            bind_processor.process()
            output_values = new_values(self.get_or_make_mapped_value, i)
            if named_outputs:
                hw.OutputOp(operands=output_values)
        bind_processor.postprocess()
        return op

    def _add_module_parameters(self, hw_module: hw.ModuleOpBase):
        defn_or_decl = self._magma_defn_or_decl
        try:
            param_types = defn_or_decl.coreir_config_param_types
        except AttributeError:
            return
        for name, type in param_types.items():
            type = python_type_to_mlir_type(type)
            param = hw.ParamDeclAttr(name, type)
            hw_module.parameters.append(param)
