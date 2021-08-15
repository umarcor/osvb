from typing import Union
from pyGHDL.dom.Symbol import (
    SimpleSubtypeSymbol,
    ConstrainedCompositeSubtypeSymbol,
)


# From pyGHDL's dom/formatting/prettyprint.py
def SubtypeIndication(subtypeIndication: Union[SimpleSubtypeSymbol, ConstrainedCompositeSubtypeSymbol]) -> str:
    """
    Format the subtype indication of generics/ports as an string.
    """
    if isinstance(subtypeIndication, SimpleSubtypeSymbol):
        return "{type}".format(type=subtypeIndication.SymbolName)
    elif isinstance(subtypeIndication, ConstrainedCompositeSubtypeSymbol):
        constraints = []
        for constraint in subtypeIndication.Constraints:
            constraints.append(str(constraint))

        return "{type}({constraints})".format(type=subtypeIndication.SymbolName, constraints=", ".join(constraints))
    else:
        raise Exception("Unhandled subtype kind '{type}'.".format(type=subtypeIndication.__class__.__name__))
