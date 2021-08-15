from typing import List, Union
from pathlib import Path
from textwrap import indent
from io import StringIO
from contextlib import redirect_stdout
from tabulate import tabulate

from pyGHDL.dom.NonStandard import Design, Document, Library
from pyGHDL.dom.DesignUnit import Entity

from pyVHDLModelUtils.resolve import Symbols as resolve_Symbols
from pyVHDLModelUtils.fmt import SubtypeIndication as format_SubtypeIndication


DESIGN = Design()


def initDesign(root: Union[str, Path], **kwargs) -> None:
    """
    Initialize a Design and analyze sources.

    Each argument after `root` defines a library name and the type is expected to be a list of patterns.

    :param root: Location of the root for all provided relative paths. This is relative to the base directory of the build.
    """
    root = Path(root) if isinstance(root, str) else root
    print(".. NOTE:: Output of initDesign:\n")
    for library, patterns in kwargs.items():
        lib = DESIGN.GetLibrary(library)
        print("  * {0}\n".format(library))
        for pattern in patterns:
            for item in root.glob(pattern):
                # FIXME: is_relative_to is new in Python 3.9 (see https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.is_relative_to)
                # Therefore, we use try..except for backwards compatibility.
                # print("    * {0}\n".format(item.relative_to(root) if item.is_relative_to(root) else item))
                try:
                    path = item.relative_to(root)
                except e:
                    path = item
                print("    * {0}\n".format(path))
                f = StringIO()
                with redirect_stdout(f):
                    DESIGN.AddDocument(Document(item), lib)
                print(indent(f.getvalue(), "      * "))
        print("")
    resolve_Symbols(DESIGN)


STYLES = ["rst:list", "rst:table"]


def printDocumentationOfEntity_rstList(entity: Entity, lib: Library = None) -> None:
    """
    Print documentation of an Entity using style 'rst:list'.
    """
    print("Entity *{0}* from Library *{1}*:\n".format(entity.Identifier, lib.Identifier))

    print("* Generics:\n")
    for generic in entity.GenericItems:
        print(
            "   * *{0}* : ``{1}``{2}".format(
                ", ".join(generic.Identifiers),
                format_SubtypeIndication(generic.Subtype),
                "" if generic.DefaultExpression is None else " := ``{0!s}``".format(generic.DefaultExpression),
            )
        )
    print("\n* Ports:\n")
    for port in entity.PortItems:
        print(
            "   * *{0}* : {1} ``{2}``{3}".format(
                ", ".join(port.Identifiers),
                port.Mode,
                format_SubtypeIndication(port.Subtype),
                "" if port.DefaultExpression is None else " := ``{0!s}``".format(port.DefaultExpression),
            )
        )
    print("\n* Architectures:\n")
    for architecture in entity.Architectures:
        print("  * *{0}*".format(architecture.Identifier))


def printDocumentationOfEntity_rstTable(entity: Entity, lib: Library = None) -> None:
    """
    Print documentation of an Entity using style 'rst:table' (through 'tabulate').
    """

    def printTable(data, headers=None, caption=None):
        table = tabulate(data, tablefmt="rst") if headers is None else tabulate(data, headers, tablefmt="rst")
        if caption is not None:
            print(".. table:: {0}\n  :align: center\n".format(caption))
            print(indent(table, "  "))
        else:
            print(table)
        print("\n")

    name = "{0}{1}".format("" if lib is None else "{0}.".format(lib.Identifier), entity.Identifier)

    printTable(
        [
            [
                ", ".join(generic.Identifiers),
                "``{0}``".format(format_SubtypeIndication(generic.Subtype)),
                "" if generic.DefaultExpression is None else "``{0!s}``".format(generic.DefaultExpression),
            ]
            for generic in entity.GenericItems
        ],
        headers=["Identifiers", "Type", "Default"],
        caption="{0} Generics".format(name),
    )

    printTable(
        [
            [
                ", ".join(port.Identifiers),
                port.Mode,
                "``{0}``".format(format_SubtypeIndication(port.Subtype)),
                "" if port.DefaultExpression is None else "``{0!s}``".format(port.DefaultExpression),
            ]
            for port in entity.PortItems
        ],
        headers=["Identifiers", "Mode", "Type", "Default"],
        caption="{0} Ports".format(name),
    )

    printTable(
        [
            [
                architecture.Identifier,
                len(architecture.Statements),
            ]
            for architecture in entity.Architectures
        ],
        headers=["Identifier", "Number of statements"],
        caption="{0} Architectures".format(name),
    )


def printDocumentationOf(targets: List[str] = None, style: str = "rst:list") -> None:
    """
    Generate documentation of resources (either a unit or a whole file).

    Supported syntaxes:

    * libraryName.entityName
    * TODO: libraryName.entityName(architectureName)
    * TODO: libraryName.packageName
    * TODO: libraryName.configurationName
    * TODO: libraryName.architectureName
    * TODO: relative/path/to/file
    * TODO: absolute/path/to/file

    :param targets: list of resources to generate the documentation for.
    :param style: format of the output. Supported values are: 'rst:list' and 'rst:table'.
    """
    if targets is None:
        print("Design content:\n")
        for libName, lib in DESIGN.Libraries.items():
            ents = lib.Entities
            print("* Library *{0}* [{1} entities]\n".format(libName, len(ents)))
            for ent in ents:
                print("  * Entity: *{0}*\n".format(ent.Identifier))
                for arch in ent.Architectures:
                    print("    * Architecture: *{0}*\n".format(arch.Identifier))
            print("")
            return

    if style not in STYLES:
        raise Exception("Unknown style <{0}>".format(style))

    for target in targets:
        # TODO: support other argument types:
        # - libName.packageName
        # - path/to/file (print all the units in the file)
        parts = target.split(".")
        assert len(parts) == 2
        libName, entityName = parts
        lib = DESIGN.GetLibrary(libName)
        entity = None
        for entity in lib.Entities:
            if entity.Identifier == entityName:
                break
        else:
            raise Exception("Entity {0} not found in library {1}.".format(entityName, libraryName))

        if style == "rst:list":
            printDocumentationOfEntity_rstList(entity, lib)
            continue

        if style == "rst:table":
            printDocumentationOfEntity_rstTable(entity, lib)
            continue
