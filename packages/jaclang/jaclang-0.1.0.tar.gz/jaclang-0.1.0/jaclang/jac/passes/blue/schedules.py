"""Pass schedules."""
from .sub_node_tab_pass import SubNodeTabPass
from .import_pass import ImportPass  # noqa: I100
from .sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from .decl_def_match_pass import DeclDefMatchPass  # noqa: I100
from .blue_pygen_pass import BluePygenPass  # noqa: I100
from .pyout_pass import PyOutPass  # noqa: I100
from .dot_exporter_pass import DotGraphPass  # noqa: I100
from .jac_formatter_pass import JacFormatPass  # noqa: I100

py_code_gen = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    BluePygenPass,
]

py_transpiler = [
    *py_code_gen,
    PyOutPass,
]

ast_dot_gen = [
    DotGraphPass,
]

full_ast_dot_gen = [
    SubNodeTabPass,
    ImportPass,
    SymTabBuildPass,
    DeclDefMatchPass,
    DotGraphPass,
]

format_pass = [JacFormatPass]
