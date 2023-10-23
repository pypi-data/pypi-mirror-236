# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['runtype']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses',
                                                         'contextvars']}

setup_kwargs = {
    'name': 'runtype',
    'version': '0.4.0',
    'description': 'Type dispatch and validation for run-time Python',
    'long_description': '![alt text](logo.png "Logo")\n\n\nRuntype is a collection of run-time type utilities for Python.\n\nIt is:\n\n:runner: Fast! Uses an internal typesystem for maximum performance.\n\n:brain: Smart! Supports `typing`, forward-references, constraints, auto-casting, and more.\n\n:gear: Configurative! Write your own type system, and use it with *dataclass* and *dispatch*.\n\n------\n\n### Modules\n\n- :star: [**validation**](https://runtype.readthedocs.io/en/latest/validation.html) - Provides a smarter alternative to `isinstance` and `issubclass`, with support for the `typing` module, and type constraints.\n\n- :star: [**dataclass**](https://runtype.readthedocs.io/en/latest/dataclass.html) - Adds run-time type validation to the built-in dataclass.\n\n    - Improves dataclass ergonomics.\n    - Supports most mypy constructs, like `typing` and forward-references (`foo: \'Bar\'`).\n    - Supports automatic value casting, Pydantic-style. (Optional, off by default)\n    - Supports types with constraints. (e.g. `String(max_length=10)`)\n    - Supports optional sampling for faster validation of big lists and dicts.\n    - Twice faster than Pydantic-v1 with pure Python ([read here](https://runtype.readthedocs.io/en/latest/dataclass.html#compared-to-pydantic))\n\n- :star: [**dispatch**](https://runtype.readthedocs.io/en/latest/dispatch.html) - Provides fast multiple-dispatch for functions and methods, via a decorator.\n\n    - Dispatch on multiple arguments\n    - Full [specificity](https://runtype.readthedocs.io/en/latest/dispatch.html#specificity) resolution\n    - [Supports Mypy typing](https://runtype.readthedocs.io/en/latest/dispatch.html#mypy-support-overload), using the `@overload` decorator\n    - Inspired by Julia.\n\n- :star: [**type utilities**](https://runtype.readthedocs.io/en/latest/types.html) - Provides a set of classes to implement your own type-system.\n\n    - Supports generics, constraints, phantom types\n    - Used by runtype itself, to emulate the Python type-system.\n \n\n## Docs\n\nRead the docs here: https://runtype.readthedocs.io/\n\n## Install\n\n```bash\npip install runtype\n```\n\nNo dependencies.\n\nRequires Python 3.6 or up.\n\n[![codecov](https://codecov.io/gh/erezsh/runtype/branch/master/graph/badge.svg)](https://codecov.io/gh/erezsh/runtype)\n\n## Examples\n\n### Validation (Isa & Subclass)\n\nUse `isa` and `issubclass` as a smarter alternative to the builtin isinstance & issubclass -\n\n```python\nfrom runtype import isa, issubclass\n\nassert isa({\'a\': 1}, dict[str, int])        # == True\nassert not isa({\'a\': \'b\'}, dict[str, int])  # == False\n\nassert issubclass(dict[str, int], typing.Mapping[str, int])     # == True\nassert not issubclass(dict[str, int], typing.Mapping[int, str]) # == False\n```\n\n### Dataclasses\n\n```python\nfrom runtype import dataclass\n\n@dataclass(check_types=\'cast\')  # Cast values to the target type, when applicable\nclass Person:\n    name: str\n    birthday: datetime = None   # Implicit optional\n    interests: list[str] = []   # The list is copied for each instance\n\n\nprint( Person("Beetlejuice") )\n#> Person(name=\'Beetlejuice\', birthday=None, interests=[])\nprint( Person("Albert", "1955-04-18T00:00", [\'physics\']) )\n#> Person(name=\'Albert\', birthday=datetime.datetime(1955, 4, 18, 0, 0), interests=[\'physics\'])\nprint( Person("Bad", interests=[\'a\', 1]) )\n# TypeError: [Person] Attribute \'interests\' expected value of type list[str]. Instead got [\'a\', 1]\n#     Failed on item: 1, expected type str\n```\n\n### Multiple Dispatch\n\nRuntype dispatches according to the most specific type match -\n\n```python\nfrom runtype import multidispatch as md\n\n@md\ndef mul(a: list, b: list):\n    return [mul(i, j) for i, j in zip(a, b, strict=True)]\n@md\ndef mul(a: list, b: Any):\n    return [ai*b for ai in a]\n@md\ndef mul(a: Any, b: list):\n    return [bi*b for bi in b]\n@md\ndef mul(a: Any, b: Any):\n    return a * b\n\nassert mul("a", 4)         == "aaaa"        # Any, Any\nassert mul([1, 2, 3], 2)   == [2, 4, 6]     # list, Any\nassert mul([1, 2], [3, 4]) == [3, 8]        # list, list\n\n```\n\nDispatch can also be used for extending the dataclass builtin `__init__`:\n\n```python\n@dataclass(frozen=False)\nclass Point:\n    x: int = 0\n    y: int = 0\n    \n    @md\n    def __init__(self, points: list | tuple):\n        self.x, self.y = points\n\n    @md\n    def __init__(self, points: dict):\n        self.x = points[\'x\']\n        self.y = points[\'y\']\n    \n# Test constructors\np0 = Point()                         # Default constructor\nassert p0 == Point(0, 0)             # Default constructor\nassert p0 == Point([0, 0])           # User constructor\nassert p0 == Point((0, 0))           # User constructor\nassert p0 == Point({"x": 0, "y": 0}) # User constructor\n```\n\n\n## License\n\nRuntype uses the [MIT license](LICENSE).\n\n## Donate\n\nIf you like Runtype and want to show your appreciation, you can do so at my [patreon page](https://www.patreon.com/erezsh), or [ko-fi page](https://ko-fi.com/erezsh).\n',
    'author': 'Erez Shinan',
    'author_email': 'erezshin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/erezsh/runtype',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
