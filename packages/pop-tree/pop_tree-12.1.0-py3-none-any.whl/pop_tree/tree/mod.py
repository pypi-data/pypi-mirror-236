import enum
import inspect
import re
import textwrap
from collections import OrderedDict
from dataclasses import is_dataclass
from typing import _GenericAlias
from typing import Any
from typing import Callable
from typing import Dict
from typing import get_origin
from typing import List
from typing import Literal
from typing import Set
from typing import Tuple

import aiofiles
from docstring_parser import Docstring
from docstring_parser import parse as docstring_parse

UNKNOWN_REF = "< unknown ref >"


def get_ref(hub, mod) -> str:
    """
    Try to find a reference on the hub for the given mod
    """
    try:
        sister_func = next(iter(mod._funcs.values()))
        return sister_func.ref
    except StopIteration:
        ...


def serialize_signature(
    hub,
    signature: inspect.Signature,
    param_aliases: Dict[str, Set[str]],
    func_docstring,
):
    ret = _serialize_params(signature.parameters, param_aliases, func_docstring)

    final_ret = {"parameters": ret}
    if signature.return_annotation is not inspect._empty:
        final_ret["return_annotation"] = signature.return_annotation
    return final_ret


def _serialize_params(
    params, aliases: Dict[str, Set[str]] = None, func_docstring: Docstring = None
):
    if aliases is None:
        aliases = {}
    ret = OrderedDict()
    for p in params:
        param: inspect.Parameter = params[p]
        ret[param.name] = {}

        matched_func_docstring_param = None
        if func_docstring:
            matched_func_docstring_params = []
            for func_docstring_param in func_docstring.params:
                arg_name = func_docstring_param.arg_name
                if arg_name.startswith(
                    "* "
                ):  # properties of complex objects are prefixed with `* ` in docstring
                    arg_name = arg_name[2:].strip()
                if arg_name == p or (p in aliases and arg_name in aliases[p]):
                    matched_func_docstring_params.append(func_docstring_param)

            if (
                len(matched_func_docstring_params) == 1
                and matched_func_docstring_params[0].description
            ):
                matched_func_docstring_param = matched_func_docstring_params[0]
                ret[param.name][
                    "description"
                ] = matched_func_docstring_param.description

        if p in aliases:
            ret[param.name]["aliases"] = sorted(aliases[p])

        if param.default is not inspect._empty:
            ret[param.name]["default"] = param.default

        annotation = param.annotation
        if annotation is inspect._empty:
            continue

        # If there are aliases for this parameter, then the annotation might be the first value in a tuple
        if p in aliases:
            if isinstance(annotation, str):
                # The annotation is just a string containing an "alias=..."
                continue
            else:
                try:
                    # See if the annotation is a tuple (<actual annotation>, "alias=", ...)
                    # The first argument can be the actual annotation, the rest are string aliases
                    annotation = annotation[0]
                except IndexError:
                    # The annotation is
                    continue

        # Check if the annotation is "Computed", "Sensitive", or any other type created from "typing.Optional"
        match = re.match(r"typing\.Union\[(.*)\]", str(annotation))
        if match:
            try:
                # The sub_type is the second value from the Union
                ret[param.name]["sub_type"] = annotation.__args__[1]
                # The real annotation is the first value from the Union
                annotation = annotation.__args__[0]
            except:
                ...

        param_type = annotation
        if isinstance(param_type, _GenericAlias) and annotation.__origin__ == list:
            param_type = annotation.__args__[0]

        if is_dataclass(param_type):
            matched_param_docstring = None
            if matched_func_docstring_param:
                param_description = matched_func_docstring_param.description
                # Find where the description of the first nested property starts
                first_nested_arg_matched = re.search(
                    r"^ *\* +.*\(.*\): *$", param_description, re.MULTILINE
                )

                if first_nested_arg_matched:
                    # Everything before the description of the first nested property can be considered the description
                    # of the current field itself
                    parent_field_description_end = param_description[
                        : first_nested_arg_matched.start()
                    ].strip()
                    nested_args_all = param_description[
                        first_nested_arg_matched.start() :
                    ]

                    # Interpret everything, starting from the description of the first nested property, as a docstring
                    # in order to leverage the docstring_parser. In order to achieve that augment (only in memory) it
                    # to adhere to the Google docstring format by prepending `Args:\n` to signify beginning of function
                    # parameters section and indent the section itself by 4 spaces to comply with expectations
                    matched_param_docstring = _docstring_parse(
                        "\nArgs:\n" + textwrap.indent(nested_args_all, 4 * " ")
                    )
                    if len(matched_param_docstring.params) > 0:
                        ret[param.name]["description"] = parent_field_description_end

            # Serialize parameters of the dataclass init method
            ret[param.name]["annotation"] = {
                # Serialize parameters of the Dataclass init method
                # Skip self argument of the Dataclass init method
                str(annotation): _serialize_params(
                    {
                        k: v
                        for k, v in inspect.signature(
                            param_type.__init__
                        ).parameters.items()
                        if k != "self"
                    },
                    aliases,
                    matched_param_docstring if matched_param_docstring else Docstring(),
                )
            }
        elif isinstance(param_type, enum.EnumMeta):
            ret[param.name]["choices"] = tuple(
                m.value for m in param_type.__members__.values()
            )
            ret[param.name]["annotation"] = str(annotation)
        elif get_origin(param_type) is Literal:
            ret[param.name]["choices"] = param_type.__args__
            ret[param.name]["annotation"] = param_type.__args__[0].__class__
        else:
            ret[param.name]["annotation"] = str(annotation)

    return ret


def _docstring_parse(text):
    try:
        return docstring_parse(text)
    except Exception:
        return Docstring()


def format_func(hub, f: Callable, **kwargs):
    lines, start_line = hub.tree.mod.get_source_lines(f)
    return {
        "doc": textwrap.dedent(str(f.__doc__ or "")).strip("\n"),
        "file": inspect.getfile(f),
        "start_line_number": start_line,
        "end_line_number": start_line + len(lines),
        **kwargs,
    }


def funcs(hub, mod, ref: str) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded functions in a pop plugin. I.E:
        pprint(hub.pop.tree.funcs(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :param ref: The current reference on the hub
    :return: A Dictionary of loaded modules names mapped to a list of their functions
    """
    funcs = sorted(mod._funcs.keys())
    ret = {}
    for f in funcs:
        contract = mod._funcs[f]

        organized_contracts = {}
        for contract_type, contracts in contract.contract_functions.items():
            organized_contracts[contract_type] = []

            for c in contracts:
                c_ref = f"{c.ref}.{c.func.__name__}"
                organized_contracts[contract_type].append(c_ref)

        func_info = hub.tree.mod.format_func(
            contract.func,
            ref=f"{ref}.{f}",
            contracts=organized_contracts,
        )
        func_info.update(
            hub.tree.mod.serialize_signature(
                contract.signature,
                contract.param_aliases,
                _docstring_parse(func_info["doc"]),
            ),
        )
        ret[f] = func_info
    return ret


def _format_var(name: str, value: Any, source_lines: List[str], **kwargs):
    line_number = 0
    for num, line in enumerate(source_lines):
        if name in line:
            line_number = num + 1
            break

    return {
        "type": value.__class__.__name__,
        "value": value,
        "start_line_number": line_number,
        **kwargs,
    }


async def data(hub, mod, ref: str) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded data in a pop plugin. I.E:
        pprint(hub.pop.tree.data(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :param ref: The current reference on the hub
    """
    datas = sorted(x for x in mod._vars if x.isupper() and not x.startswith("_"))
    ret = {}

    source_file = inspect.getsourcefile(mod)
    async with aiofiles.open(source_file, "r") as fh:
        lines = await fh.readlines()

    for d_name in datas:
        ret[d_name] = _format_var(
            d_name, mod._vars[d_name], lines, ref=f"{ref}.{d_name}", file=source_file
        )

    return ret


async def types(hub, mod, ref: str) -> List[str] or Dict[str, str]:
    """
    Find all of the loaded types in a pop plugin. I.E:
        pprint(hub.pop.tree.types(hub.pop.tree))
    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :param ref: The current reference on the hub
    """
    classes = sorted(x for x in mod._classes if not x.startswith("_"))
    ret = {}
    for class_name in classes:
        c = mod._classes[class_name]
        source_file = inspect.getsourcefile(c)

        async with aiofiles.open(source_file, "r") as fh:
            source_lines = await fh.readlines()

        try:
            lines, start_line = hub.tree.mod.get_source_lines(c)
        except OSError:
            start_line = 0
            for num, line in enumerate(source_lines):
                if class_name in line:
                    start_line = num + 1
                    break
            lines = []

        signature = inspect.signature(c.__init__)
        functions = {}
        variables = {}
        attributes = []
        for name, value in inspect.getmembers(c):
            if name.startswith("_"):
                continue
            attributes.append(name)
            attr_ref = f"{ref}.{class_name}.{name}"
            if inspect.isfunction(value):
                functions[name] = hub.tree.mod.format_func(value, ref=attr_ref)
            else:
                variables[name] = _format_var(
                    name, value, source_lines, ref=attr_ref, file=source_file
                )
        class_info = {
            "ref": f"{ref}.{class_name}",
            "doc": textwrap.dedent(c.__doc__ or "").strip("\n"),
            "signature": hub.tree.mod.serialize_signature(signature, {}, Docstring()),
            "attributes": attributes,
            "functions": functions,
            "variables": variables,
            "file": source_file,
            "start_line_number": start_line,
            "end_line_number": start_line + len(lines),
        }
        ret[class_name] = class_info
    return ret


async def parse(hub, mod, ref: str) -> Dict[str, Any]:
    """
    Parse a loaded mod object

    :param hub: The redistributed pop central hub
    :param mod: A plugin that has been loaded onto a sub
    :param ref: The current reference on the hub
    """
    return {
        "ref": ref,
        "doc": (mod._attrs.get("__doc__") or "").strip(),
        "file": getattr(mod, "__file__", None),
        "attributes": sorted(
            a for a in mod._attrs if not (a.startswith("__") and a.endswith("__"))
        ),
        "classes": await hub.tree.mod.types(mod, ref),
        "functions": hub.tree.mod.funcs(mod, ref),
        "variables": await hub.tree.mod.data(mod, ref),
    }


def get_source_lines(hub, module: Callable) -> Tuple[List, int]:
    try:
        return inspect.getsourcelines(module)
    except OSError:
        # This can happen when running pop-tree from within a binary
        return [], -1
