from pyGHDL.dom.NonStandard import Design


def Symbols(design: Design) -> None:
    """
    Resolve some symbols after parsing, but without complete analysis and elaboration.
    """
    ArchitecturesToEntities(design)


def ArchitecturesToEntities(design: Design) -> None:
    """
    Resolve architectures to entities by simple name matching.
    """
    for library in design.Libraries.values():
        for entityName, architectures in library.Architectures.items():
            for entity in library.Entities:
                if entity.Identifier == str(entityName):
                    for architecture in architectures:
                        entity.Architectures.append(architecture)
