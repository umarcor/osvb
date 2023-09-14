#!/usr/bin/env python3

from sys import argv as sys_argv

from pathlib import Path

from pyGHDL.dom.InterfaceItem import GenericConstantInterfaceItem, GenericTypeInterfaceItem
from pyGHDL.dom.NonStandard import Design, Document
from pyGHDL.dom.Concurrent import (
    ConcurrentBlockStatement,
    ProcessStatement,
    IfGenerateStatement,
    CaseGenerateStatement,
    ForGenerateStatement,
    GenerateCase,
    OthersGenerateCase,
)
from pyVHDLModel.SyntaxModel import (
    Instantiation,
    Mode,
)
from pyVHDLModelUtils.resolve import Symbols as resolve_Symbols

from gitignore_parser import parse_gitignore as ignoreParser


class OSVDE:
    def __init__(self, dirName):
        self.Design = Design()
        self.parseDir(Path(dirName))
        resolve_Symbols(self.Design)
        self.printDesignTree()

    def parseDir(self, dirName: Path):
        """
        Parse all the ``.vhd`` files found through a recursive glob, honoring ``osvdeignore`` files.
        """
        ignores = []
        for item in dirName.glob("**/.osvdeignore"):
            ignores.append((item.parent, ignoreParser(item)))

        for item in dirName.glob("**/*.vhd*"):
            ignoreItem = False
            for match in ignores:
                if str(match[0]) in str(item) and match[1](item):
                    ignoreItem = True
                    break
            if not ignoreItem:
                self.parseFile(item)

    def parseFile(self, sourceFile: Path, library: str = "lib"):
        """
        Add a VHDL source to the pyVHDLModel Design.
        """
        print(f"parseFile: {sourceFile}")
        lib = self.Design.GetLibrary(library)
        self.Design.AddDocument(Document(sourceFile), lib)

    def printDesignTree(self, parent=""):
        """
        Print the Design Tree with the data from the pyVHDLModel Design.
        """

#        def addTreeItem(parent, text, isOpen, image):
#            return dtw.insert(parent, tk.END, text=text, open=isOpen, image=self.Image[image])

        def loadStatementsTree(id, statements):
#        def loadStatementsTree(item, statements):
            for statement in statements:

                # Note: the following share the same base class 'Instantiation'
                # ComponentInstantiation, EntityInstantiation, ConfigurationInstantiation

                if isinstance(statement, Instantiation):
                    print(f"{'  '*(id+1)}{statement.Label}: inst")
#                    addTreeItem(item, "{}: inst".format(statement.Label), False, "inst")

#                elif isinstance(statement, ConcurrentBlockStatement):
#                    instItem = addTreeItem(item, "{}: block".format(statement.Label), False, "file")
#                    innerstatements = statement.Statements
#                    if len(innerstatements) != 0:
#                        loadStatementsTree(instItem, innerstatements)
#
#                # Note: the following share the same base class 'GenerateStatement'
#                # ForGenerateStatement, CaseGenerateStatement, IfGenerateStatement
#
#                elif isinstance(statement, IfGenerateStatement):
#                    instItem = addTreeItem(item, "{}: if .. generate".format(statement.Label), False, "file")
#                    loadStatementsTree(
#                        addTreeItem(
#                            instItem,
#                            "if: {}".format(statement.IfBranch.Condition),
#                            False,
#                            "file",
#                        ),
#                        statement.IfBranch.Statements,
#                    )
#                    for elsifbranch in statement.ElsifBranches:
#                        loadStatementsTree(
#                            addTreeItem(
#                                instItem,
#                                "elsif: {}".format(elsifbranch.Condition),
#                                False,
#                                "file",
#                            ),
#                            elsifbranch.Statements,
#                        )
#                    if statement.ElseBranch is not None:
#                        loadStatementsTree(
#                            addTreeItem(instItem, "else:", False, "file"),
#                            statement.ElseBranch.Statements,
#                        )
#
#                elif isinstance(statement, CaseGenerateStatement):
#                    instItem = addTreeItem(item, "{}: case .. generate".format(statement.Label), False, "file")
#                    for case in statement.Cases:
#                        if isinstance(case, GenerateCase):
#                            loadStatementsTree(
#                                addTreeItem(
#                                    instItem,
#                                    "case: {}".format(" | ".join([str(c) for c in case.Choises])),
#                                    False,
#                                    "file",
#                                ),
#                                case.Statements,
#                            )
#                        elif isinstance(case, OthersGenerateCase):
#                            loadStatementsTree(
#                                addTreeItem(instItem, "others:", False, "file"),
#                                case.Statements,
#                            )
#
#                elif isinstance(statement, ForGenerateStatement):
#                    instItem = addTreeItem(
#                        item,
#                        "{0}: for {1!s} generate".format(statement.Label, statement.Range),
#                        False,
#                        "file",
#                    )
#                    innerstatements = statement.Statements
#                    if len(innerstatements) != 0:
#                        loadStatementsTree(instItem, innerstatements)
#
#                elif isinstance(statement, ProcessStatement):
#                    addTreeItem(
#                        item,
#                        "{}: process".format(statement.Label or "DefaultLabel"),
#                        False,
#                        "file",
#                    )

        for libName, lib in self.Design.Libraries.items():
            print(f"Library: {libName}")
            #LibItem = addTreeItem(parent, libName, True, "lib")
            for entity in lib.Entities:
                print(f"  Entity: {entity.Identifier}")
                #EntityItem = addTreeItem(LibItem, entity.Identifier, False, "ent")

                generics = entity.GenericItems
                if len(generics) != 0:
                    print("    Generics:")
                    #GenericsItem = addTreeItem(EntityItem, "Generics", False, "generics")
                    for generic in generics:
                        if isinstance(generic, GenericConstantInterfaceItem):
                            print(f"      {','.join(generic.Identifiers)} [{generic.Subtype}]")
#                            addTreeItem(
#                                GenericsItem,
#                                "{} [{}]".format(",".join(generic.Identifiers), generic.Subtype),
#                                False,
#                                "generic",
#                            )
                        elif isinstance(generic, GenericTypeInterfaceItem):
                            print(f"      type: {generic.Identifier}")
#                            addTreeItem(
#                                GenericsItem,
#                                "type: {}".format(generic.Identifier),
#                                False,
#                                "generic",
#                            )
                        else:
                            print(
                                "[NOT IMPLEMENTED] Generic item class not supported yet: {0}",
                                generic.__class__.__name__,
                            )

                ports = entity.PortItems
                if len(ports) != 0:
                    print("    Ports:")
#                    PortsItem = addTreeItem(EntityItem, "Ports", False, "ports")
                    for port in ports:
                        dir = "< " if port.Mode is Mode.Out else "<>" if port.Mode is Mode.InOut else " >"
                        print(f"      {dir} {','.join(port.Identifiers)} [{port.Subtype}]")
#                        addTreeItem(
#                            PortsItem,
#                            "{} [{}]".format(",".join(port.Identifiers), port.Subtype),
#                            False,
#                            "out" if port.Mode is Mode.Out else "inout" if port.Mode is Mode.InOut else "in",
#                        )

                architectures = entity.Architectures
                if len(architectures) != 0:
                    print("    Architectures:")
#                    ArchitecturesItem = addTreeItem(EntityItem, "Architectures", False, "archs")
                    for architecture in entity.Architectures:
                        print(f"      {architecture.Identifier}")
                        loadStatementsTree(3, architecture.Statements)
#                        loadStatementsTree(
#                            addTreeItem(ArchitecturesItem, "{}".format(architecture.Identifier), False, "arch"),
#                            architecture.Statements,
#                        )

if __name__ == "__main__":
    if len(sys_argv) < 2:
        raise Exception('Needs one argument: the path to a directory containing VHDL sources.')

    OSVDE(Path(sys_argv[1]))
