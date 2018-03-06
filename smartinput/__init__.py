"""Two-three sentences about what your project does
Examples:
>>> import myproject as mp
>>> print mp.variableC
42
List of modules
"""

import smartinput

from smartinput.smart_input import SmartInput

__all__ = [smart_input.__all__]


if __name__ == "__main__":
    
    import doctest
    doctest.testmod()
