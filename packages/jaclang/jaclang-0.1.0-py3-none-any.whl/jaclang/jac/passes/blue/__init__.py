"""Collection of passes for Jac IR."""
from .sub_node_tab_pass import SubNodeTabPass
from .import_pass import ImportPass  # noqa: I100
from .sym_tab_build_pass import SymTabBuildPass  # noqa: I100
from .decl_def_match_pass import DeclDefMatchPass  # noqa: I100
from .blue_pygen_pass import BluePygenPass  # noqa: I100
from .pyout_pass import PyOutPass  # noqa: I100
from .jac_formatter_pass import JacFormatPass  # noqa: I100
from .dot_exporter_pass import DotGraphPass  # noqa: I100
from .schedules import py_code_gen  # noqa: I100

pass_schedule = py_code_gen

__all__ = [
    "SubNodeTabPass",
    "ImportPass",
    "SymTabBuildPass",
    "DeclDefMatchPass",
    "BluePygenPass",
    "PyOutPass",
    "JacFormatPass",
    "DotGraphPass",
]
