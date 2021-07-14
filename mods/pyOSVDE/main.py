#!/usr/bin/env python3

# Authors:
#   Unai Martinez-Corral
#
# Copyright 2021 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


from sys import argv as sys_argv, exit as sys_exit

import tkinter as tk
from tkinter import messagebox as mbox
from tkinter import ttk as ttk, filedialog as fd

from pathlib import Path
from textwrap import dedent

from pyGHDL.dom.NonStandard import Design, Document
from pyVHDLModel.VHDLModel import Mode

from gitignore_parser import parse_gitignore as ignoreParser


class OSVDE(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.title("[OSVDE] Open Source VHDL Design Explorer")

        parent.state("zoomed")

        self.Frame = tk.Frame(parent)
        self.FileTreeView = ttk.Treeview(self)
        self.DesignTreeView = ttk.Treeview(self)

        self.FileTreeView.pack(fill="both", side=tk.TOP, expand=True)
        self.DesignTreeView.pack(fill="both", side=tk.TOP, expand=True)
        self.Frame.pack(fill=tk.X, side=tk.BOTTOM, expand=False)
        self.pack(fill="both", expand=True)

        self._initImages()
        parent.iconphoto(False, self.ImageLogo)

        self._initMenu(parent)
        self._initFileTreeView()
        self._initDesignTreeView()

        # tk.Button(self.Frame, text="Click to Open File", command=self.cbFile).pack(
        #     fill=tk.X, side=tk.LEFT, expand=True
        # )
        # tk.Button(self.Frame, text="Click to Open Directory", command=self.cbDir).pack(
        #     fill=tk.X, side=tk.LEFT, expand=True
        # )

        self.Design = Design()

        self.cbDir()

    def _initImages(self):
        """
        Load images for icons and logo.
        """
        # https://www.flaticon.com/packs/file-folder-13
        imgDir = Path(__file__).parent / "img"
        self.ImageLogo = tk.PhotoImage(file=imgDir / "512" / "icon512.png")
        imgDir16 = imgDir / "16"
        self.Image = {}
        for item in "dir", "file", "lib", "ent", "in", "out", "inout":
            self.Image[item] = tk.PhotoImage(file=imgDir16 / "{}16.png".format(item))

    def _initMenu(self, parent):
        """
        Initialise the main Menu.
        """

        def cbAbout():
            # aboutWindow = tk.Toplevel(parent)
            # aboutWindow.title("About Open Source VHDL Design Explorer (OSVDE)")
            # aboutWindow.geometry("500x350")
            # tk.Label(aboutWindow, text ="This is a new window").pack()
            mbox.showinfo(
                "About",
                dedent(
                    """\
            Open Source VHDL Design Explorer (OSVDE)
            <github.com/umarcor/osvb>

            Copyright 2021 Unai Martinez-Corral
            <unai.martinezcorral@ehu.eus>

            Licensed under the Apache License, Version 2.0
            <apache.org/licenses/LICENSE-2.0>
            """
                ),
            )

        self.Menu = tk.Menu(parent)
        parent.config(menu=self.Menu)

        fileMenu = tk.Menu(self.Menu, tearoff=0)
        fileMenu.add_command(label="Open File...", command=self.cbFile)
        fileMenu.add_command(label="Open Directory...", command=self.cbDir)
        fileMenu.add_separator()
        fileMenu.add_command(label="About...", command=cbAbout)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=parent.quit)
        self.Menu.add_cascade(label="File", menu=fileMenu)

        # editMenu = tk.Menu(self.Menu, tearoff=0)
        # editMenu.add_command(label="Undo")
        # editMenu.add_command(label="Redo")
        # self.Menu.add_cascade(label="Edit", menu=editMenu)

    def _initFileTreeView(self):
        """
        Initialise the File TreeView (define the columns).
        """
        ftw = self.FileTreeView
        ftw["columns"] = "units"
        ftw.heading("#0", text="Sources: **/*vhd")
        ftw.heading("units", text="Units: entity(architecture,...)|<entity>(architecture,...)")

    def _initDesignTreeView(self):
        """
        Initialise the Design TreeView (define the columns).
        """
        dtw = self.DesignTreeView
        dtw.heading("#0", text="Design hierarchies")

    def cbDir(self):
        """
        Callback for '*Open Directory...*'.
        """
        dirName = fd.askdirectory(mustexist=True)
        if dirName != "":
            self.parseDir(Path(dirName))

    def cbFile(self):
        """
        Callback for '*Open File...*'.
        """
        fileName = fd.askopenfilename()
        self.parseFile(Path(fileName))

    def parseDir(self, dirName: Path):
        """
        Parse all the ``.vhd`` files found through a recursive glob, honoring ``osvdeignore`` files.
        """
        ignores = []
        for item in dirName.glob("**/.osvdeignore"):
            ignores.append((item.parent, ignoreParser(item)))

        for item in dirName.glob("**/*.vhd"):
            ignoreItem = False
            for match in ignores:
                if str(match[0]) in str(item) and match[1](item):
                    ignoreItem = True
                    break
            if not ignoreItem:
                self.parseFile(item)

        self.loadFileTree()
        self.loadDesignTree()

    def parseFile(self, sourceFile: Path, library: str = "lib"):
        """
        Add a VHDL source to the pyVHDLModel Design.
        """
        print("parseFile: {}".format(sourceFile))
        lib = self.Design.GetLibrary(library)
        self.Design.AddDocument(Document(sourceFile), lib)

    def loadFileTree(self, parent=""):
        """
        Populate the FileTreeView with the data from the pyVHDLModel Design.
        """
        ftw = self.FileTreeView

        def addTreeItem(parent, text, isDir, data=()):
            return ftw.insert(
                parent,
                tk.END,
                text=text,
                values=data,
                open=isDir,
                image=self.Image["dir"] if isDir else self.Image["file"],
            )

        def traversePath(document, parts, parent):
            item = parts[0]
            isDir = len(parts) > 1

            children = [iid for iid in ftw.get_children(parent) if ftw.item(iid)["text"] == item]
            childrenLen = len(children)

            if isDir:
                if childrenLen > 1:
                    raise Exception("Duplicated item text <{}>: {}".format(item, children))
                return traversePath(
                    document,
                    parts[1:],
                    addTreeItem(parent, item, True, ()) if childrenLen == 0 else children[0],
                )

            if len(children) > 0:
                raise Exception("Item text <{}> exists already: {}".format(item, children))

            units = {}
            for entity in document.Entities:
                units[entity.Identifier] = []

            for architecture in document.Architectures:
                entityName = architecture.Entity.SymbolName
                if entityName in units:
                    units[entityName].append(architecture.Identifier)
                else:
                    units["<{}>".format(entityName)] = [architecture.Identifier]

            addTreeItem(
                parent,
                item,
                False,
                ("| ".join(["{}({})".format(key, ", ".join(val)) for key, val in units.items()])),
            )

        for document in self.Design.Documents:
            traversePath(document, list(document.Path.parts), parent)

    def loadDesignTree(self, parent=""):
        """
        Populate the DesignTreeView with the data from the pyVHDLModel Design.
        """
        dtw = self.DesignTreeView

        def addTreeItem(parent, text, isOpen, image, data=()):
            return dtw.insert(parent, tk.END, text=text, values=data, open=isOpen, image=image)

        for lib in self.Design.Libraries:
            LibItem = addTreeItem(parent, lib, True, self.Image["lib"], ())
            for entity in self.Design.GetLibrary(lib).Entities:
                EntityItem = addTreeItem(LibItem, entity.Identifier, False, self.Image["ent"], ())
                for port in entity.PortItems:

                    image = self.Image["in"]
                    if port.Mode is Mode.Out:
                        image = self.Image["out"]
                    elif port.Mode is Mode.InOut:
                        image = self.Image["inout"]

                    PortItem = addTreeItem(
                        EntityItem,
                        "{} [{}]".format(port.Identifier, port.Subtype),
                        False,
                        image,
                        (),
                    )

                # TODO:
                # - Create items 'generics', 'ports' and 'architectures'.
                # - Move port items into 'ports'.
                # - Add generic items into 'generics'.
                # - Add architecture items into 'architectures'.
                #   Strictly, this would require elaboration.
                #   However, there are three solutions:
                #   - Do a naive elaboration, as in function traversePath of loadFileTree.
                #   - Implement the elaboration in pyVHDLModel.
                #   - Use pyGHDL.libghdl for elaboration.
                #   The most sensible solution is to use the first one, skip the second one, and work on the last one.


if __name__ == "__main__":
    sys_exit(OSVDE(tk.Tk()).mainloop())
