import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple, Protocol

SCALAR_TYPEDEF_RE = re.compile(r"^typedef\s+(\w+)\s+(\w+)\s*;", re.MULTILINE)
OPAQUE_HANDLE_RE = re.compile(
    r"^typedef\s+(?:const\s+)?struct\s+(\w+)\s*\**(\w+)\s*;", re.MULTILINE
)
ENUM_RE = re.compile(r"typedef\s+enum\s*\{([^}]+)\}\s*(\w+)\s*;", re.DOTALL)
STRUCT_UNION_RE = re.compile(r"typedef\s+(?:struct|union)\s*\{([^}]+)\}\s*(\w+)\s*;", re.DOTALL)
FUNC_TYPEDEF_RE = re.compile(
    r"^typedef\s+(\w+)\s*\(\s*\*\s*(\w+)\s*\)\s*\(([^)]*)\)\s*;", re.MULTILINE
)
FUNCTION_RE = re.compile(
    r"^(?:(?P<ptr_return>(?:const\s+)?\w+\s*\*)\s*(?P<ptr_name>\w+)"
    r"|(?P<return>\w+)\s+(?P<name>\w+))\s*\((?P<params>[^)]*)\)\s*;",
    re.MULTILINE,
)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
ARRAY_FIELD_RE = re.compile(r"^(\w+(?:\s*\*)*)\s+(\w+)\s*\[\s*(\w+)\s*\]$")
ARRAY_RE = re.compile(r"^(.+)\[(\d+)\]$")
INT_TYPE_RE = re.compile(r"u?int[0-9]+_t")


class StubSource(Protocol):
    def generate(self) -> str: ...


class EnumMember(NamedTuple):
    name: str
    value: str


class Enum(NamedTuple):
    name: str
    members: list[EnumMember]

    def generate(self) -> str:
        return f"{self.name}: TypeAlias = Literal[{', '.join(mem.value for mem in self.members)}]"

    def generate_protocol_fields(self) -> list[str]:
        return [f"    {member.name}: {self.name}" for member in self.members]


class StructOrUnion(NamedTuple):
    name: str
    fields: list[tuple[str, str]]

    def generate(self) -> str:
        lines = [f"\nclass {self.name}:"]
        for field_type, field_name in self.fields:
            py_type = c_to_python_type(field_type)
            lines.append(f"    {field_name}: {py_type}")
        return "\n".join(lines)


class ScalarTypedef(NamedTuple):
    base_type: str
    name: str

    def generate(self) -> str:
        py_type = c_to_python_type(self.base_type)
        return f"{self.name}: TypeAlias = {py_type}"


class OpaqueHandle(NamedTuple):
    struct_name: str
    alias: str

    def generate(self) -> str:
        return f"\nclass {self.alias}: ..."


class Function(NamedTuple):
    return_type: str
    name: str
    params: list[tuple[str, str]]

    def generate(self) -> str:
        params: list[str] = []
        for param_type, param_name in self.params:
            py_type = c_to_python_type(param_type)
            param_name = safe_python_name(param_name)
            params.append(f"{param_name}: {py_type}" if param_name else py_type)
        ret_type = c_to_python_type(self.return_type)
        params_str = ", ".join(params)
        return f"def {self.name}({params_str}) -> {ret_type}: ..."

    def generate_protocol_method(self) -> str:
        params: list[str] = ["self"]
        for param_type, param_name in self.params:
            py_type = c_to_python_type(param_type)
            param_name = safe_python_name(param_name)
            params.append(f"{param_name}: {py_type}" if param_name else py_type)
        ret_type = c_to_python_type(self.return_type)
        params_str = ", ".join(params)
        return f"def {self.name}({params_str}) -> {ret_type}: ..."


class FunctionPointerTypedef(NamedTuple):
    return_type: str
    name: str
    params: list[tuple[str, str]]

    def generate(self) -> str:
        params = [c_to_python_type(p[0]) for p in self.params]
        ret_type = c_to_python_type(self.return_type)
        params_str = ", ".join(params) if params else ""
        return f"{self.name}: TypeAlias = Callable[[{params_str}], {ret_type}]"


def parse_cdef(content: str) -> list[StubSource]:
    return [
        *parse_scalar_typedefs(content),
        *parse_opaque_handles(content),
        *parse_enums(content),
        *parse_structs_and_unions(content),
        *parse_function_typedefs(content),
        *parse_functions(content),
    ]


def parse_scalar_typedefs(content: str) -> list[ScalarTypedef]:
    # Scalar typedefs are kept separate from opaque handles since they represent
    # type aliases rather than pointer-based handles
    return [ScalarTypedef(m[1], m[2]) for m in SCALAR_TYPEDEF_RE.finditer(content)]


def parse_opaque_handles(content: str) -> list[OpaqueHandle]:
    # Opaque handles use forward-declared struct pointers, so we capture both
    # the implementation struct name and the public alias
    return [OpaqueHandle(m[1], m[2]) for m in OPAQUE_HANDLE_RE.finditer(content)]


def parse_enums(content: str) -> list[Enum]:
    return [parse_enum(m[1], m[2]) for m in ENUM_RE.finditer(content)]


def parse_enum(body: str, name: str) -> Enum:
    members: list[EnumMember] = []
    implicit_value: str = "0"

    for line in map(str.strip, body.strip().splitlines()):
        if not line or line.startswith("/*"):
            continue

        line = line.rstrip(",").strip()

        if "=" not in line:
            members.append(EnumMember(line, implicit_value))
            implicit_value = str(int(implicit_value) + 1)
            continue
        member_name, member_value = line.split("=", 1)
        members.append(EnumMember(member_name.strip(), member_value.strip()))
        try:
            # Track the next implicit value in case subsequent members
            # omit explicit values (C enums auto-increment)
            implicit_value = str(int(member_value) + 1)
        except ValueError:
            # Non-integer values (e.g., macro references) can't be
            # auto-incremented, so preserve them as-is
            implicit_value = member_value.strip()

    return Enum(name, members)


def parse_structs_and_unions(content: str) -> list[StructOrUnion]:
    return [StructOrUnion(m[2], parse_struct_body(m[1])) for m in STRUCT_UNION_RE.finditer(content)]


def parse_struct_body(body: str) -> list[tuple[str, str]]:
    # Strip comments early to simplify subsequent parsing logic
    body = COMMENT_RE.sub("", body)

    return [parse_struct_field(line) for line in split_struct_fields(body) if line]


def split_struct_fields(body: str) -> list[str]:
    return list(map(str.strip, body.split(";")))


def parse_struct_field(line: str) -> tuple[str, str]:
    # Normalize whitespace to make regex patterns simpler
    line = " ".join(line.split())

    # Array fields need special handling: the size belongs to the type,
    # not the field name, for downstream consumers
    if match := ARRAY_FIELD_RE.match(line):
        field_type = f"{match[1]}[{match[3]}]"
        field_name = match[2]
        return field_type, field_name

    # For regular fields, rsplit handles the case where the type itself
    # contains spaces (e.g., "const char *")
    type_str, name = line.rsplit(maxsplit=1)
    return normalize_pointer_notation(type_str, name)


def normalize_pointer_notation(type_str: str, name: str) -> tuple[str, str]:
    # Move leading asterisks from name to type for consistency with
    # how pointer types are typically represented
    # orig = type_str, name
    while name.startswith("*"):
        type_str += "*"
        name = name[1:]
    # assert orig == (type_str, name), (orig, (type_str, name))
    return type_str, name


def parse_function_typedefs(content: str) -> list[FunctionPointerTypedef]:
    return [
        FunctionPointerTypedef(m[1], m[2], parse_params(m[3]))
        for m in FUNC_TYPEDEF_RE.finditer(content)
    ]


def parse_functions(content: str) -> list[Function]:
    results: list[Function] = []

    for m in FUNCTION_RE.finditer(content):
        name = m["ptr_name"] or m["name"]
        # Skip function pointer typedefs that match the function regex pattern
        # (they're already captured by FUNC_TYPEDEF_RE above)
        if name.startswith("(*"):
            continue

        return_type = m["ptr_return"] or m["return"]
        results.append(Function(return_type, name, parse_params(m["params"])))

    return results


def parse_params(params_str: str) -> list[tuple[str, str]]:
    # Empty param lists and explicit void both represent no parameters
    if params_str.strip() in ("", "void"):
        return []

    params: list[tuple[str, str]] = []

    for param in params_str.split(","):
        if not (param := param.strip()):
            continue

        parts = param.rsplit(None, 1)
        if len(parts) == 2:
            params.append(normalize_pointer_notation(*parts))
        else:
            # Some declarations omit parameter names (e.g., function prototypes),
            # so we store an empty name in that case
            params.append((param, ""))

    return params


C_TO_PY_TYPE_MAPPING = {
    "intptr_t": "int",
    "size_t": "int",
    "bool": "bool",
    "char": "str",
    "void": "None",
}

RESERVED_PARAMETER_NAMES = {
    "len": "length",
}


def safe_python_name(name: str) -> str:
    return RESERVED_PARAMETER_NAMES.get(name, name)


def c_to_python_type(c_type: str) -> str:
    c_type = c_type.removeprefix("const").strip()
    if c_type == "void*":
        return "object"
    if c_type.endswith("*"):
        return "object"
    c_type = c_type.rstrip("*").strip()

    # Array types: translate base type to Python and wrap in list[...]
    if match := ARRAY_RE.match(c_type):
        base_type = match[1].strip()
        py_base = c_to_python_type(base_type)
        return f"list[{py_base}]"

    if INT_TYPE_RE.match(c_type):
        return "int"
    return C_TO_PY_TYPE_MAPPING.get(c_type, c_type)


def generate_stubs(definitions: list[StubSource]) -> str:
    lines = [
        "from collections.abc import Callable\n",
        "from typing import Literal, Protocol, TypeAlias\n",
        "\n",
    ]

    for defn in definitions:
        lines.append(defn.generate())
        lines.append("\n")

    protocol_lines = ["\nclass GhosttyVtLib(Protocol):"]
    for defn in definitions:
        if isinstance(defn, Enum):
            protocol_lines.extend(defn.generate_protocol_fields())
        if isinstance(defn, Function):
            protocol_lines.append("    " + defn.generate_protocol_method())
    lines.append("\n".join(protocol_lines))
    lines.append("\n")

    return "".join(lines)


if __name__ == "__main__":
    content = Path("src/libghostty/_cffi/cdef.h").read_text()
    definitions = parse_cdef(content)
    stubs = generate_stubs(definitions).encode()
    formatted_stubs = subprocess.check_output(["uv", "run", "ruff", "format", "-"], input=stubs)
    _ = sys.stdout.buffer.write(formatted_stubs)
    _ = sys.stdout.flush()
