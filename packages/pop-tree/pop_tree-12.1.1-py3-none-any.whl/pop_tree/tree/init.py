from types import ModuleType
from typing import Any
from typing import Dict

import pop.hub
from dict_tools import data as data_

__func_alias__ = {"format_": "format"}


def __init__(hub):
    hub.pop.sub.add(dyne_name="rend", omit_class=False)
    hub.pop.sub.add(dyne_name="graph", omit_class=False)


def doc_cli(hub):
    hub.pop.config.load(["pop_doc", "pop_tree", "rend"], cli="pop_doc")
    hub.pop.loop.create()
    hub.tree.sub.load_all()
    ref = hub.OPT.pop_doc.ref.replace("[", ".").replace("]", "")

    tree = hub.pop.Loop.run_until_complete(hub.tree.init.traverse(ref=ref))

    tree = hub.tree.ref.get(tree, ref)
    ret = hub.tree.ref.list(tree)

    if not (ret or tree):
        raise KeyError(f"Reference does not exist on the hub: {ref}")

    try:
        result = ret[ref]
    except:
        result = {}

        for r, docs in ret.items():
            if r.startswith(ref) and "parameters" in docs:
                result[r] = docs

    outputter = hub.OPT.rend.output or "nested"
    print(hub.output[outputter].display(result))


def cli(hub):
    hub.pop.config.load(["pop_tree", "rend"], cli="pop_tree")
    hub.pop.loop.create()
    hub.tree.sub.load_all(pypaths=hub.OPT.pop_tree.pypaths)

    tree = hub.pop.Loop.run_until_complete(hub.tree.init.traverse())
    result = hub.tree.ref.get(tree, hub.OPT.pop_tree.ref)

    if hub.OPT.pop_tree.graph:
        hub.graph.GRAPH = hub.OPT.pop_tree.graph
    else:
        # Find the first plugin that was loaded for graphing
        loaded_mods = hub.graph._loaded
        if "simple" in loaded_mods:
            hub.graph.GRAPH = "simple"
        else:
            iter_mods = iter(hub.graph._loaded)
            hub.graph.GRAPH = next(iter_mods)
            if hub.graph.GRAPH == "init":
                hub.graph.GRAPH = next(iter_mods)

    hub.graph.init.show(result)


async def traverse(hub, ref: str = None) -> Dict[str, Any]:
    """
    :param hub: The redistributed pop central hub
    :return: A dictionary representation of all the subs on the hub. I.E:
        pprint(hub.pop.tree.traverse())
    """
    root = data_.NamespaceDict()

    if ref is None:
        ref = hub.OPT.pop_tree.ref

    # Default behavior, enumerate everything on th hub
    if not ref:
        for sub in hub._iter_subs:
            loaded_sub = getattr(hub, sub)
            sub_refs = await hub.tree.sub.parse(loaded_sub)
            root.update(sub_refs)
    # Only parse things under the named ref
    else:
        # Contract references on the hub after pop26 look like this:
        #    mod._recursive_contract_subs[0].test.post
        # Here we transform it to look like this:
        #    mod._recursive_contract_subs.0.test.post
        # So that it works with existing pop-tree logic
        parts = ref.replace("[", ".").replace("]", "").split(".")

        base = hub
        for p in parts:
            # Include possible numbers existing in the fun new list of contracts ref
            if p.isdigit() and isinstance(base, list):
                try:
                    base = base[int(p)]
                except IndexError:
                    return root
            else:
                base = getattr(base, p)

        await hub.tree.init.parse_base(base, root, ref, parts)

    return root


async def parse_base(hub, base, root: dict, ref: str, parts: list):
    """
    Take an object that exists on the hub and find the documentation recursively under it.
    """
    if isinstance(base, pop.hub.ReverseSub):
        hub.log.trace(f"Resolving ReverseSub reference")
        # handle getting the docs from a reverse sub
        base = base._resolve()

    if isinstance(base, pop.hub.Sub):
        hub.log.trace(f"Parsing a single sub")
        subs = parts[:-1]
        sub_refs = await hub.tree.sub.parse(base, base_ref=".".join(subs))

        builder = root
        for sub in subs:
            builder[sub] = data_.NamespaceDict()
            builder = builder[sub]

        builder.update(sub_refs)
    elif isinstance(base, ModuleType):
        hub.log.trace(f"Parsing a single module")
        mod = base.__name__
        subs = parts[:-1]

        builder = root
        for sub in subs:
            builder[sub] = data_.NamespaceDict()
            builder = builder[sub]

        ret = await hub.tree.mod.parse(base, ref=ref)
        builder[mod] = ret
    elif isinstance(base, list):
        # This is probably a list of contracts
        for i, item in enumerate(base):
            if isinstance(item, pop.hub.Sub):
                item._subname = str(i)
                await hub.tree.init.parse_base(item, root, f"{ref}.{i}", parts + [i])
            else:
                raise TypeError(f"Unknown base in list: {item.__class__.__name__}")
    else:
        # Everything else that could be inside a loaded mod: functions, classes, and variables
        subs = parts[:-1]
        mod_ref = ".".join(subs)
        mod = hub

        for p in subs:
            if isinstance(mod, list) and str(p).isdigit():
                mod = mod[int(p)]
            else:
                mod = mod[p]

        mod_docs = (await hub.tree.mod.parse(mod, mod_ref),)

        builder = root

        for sub in subs:
            builder[sub] = data_.NamespaceDict()
            builder = builder[sub]

        builder.update(mod_docs[0])
