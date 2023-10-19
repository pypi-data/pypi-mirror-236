### Randomify — A simple module for convenient and fast generation of a character set



####  Installation

| Windows                   | Linux/MacOs                |
| ------------------------- | -------------------------- |
| `pip install pyrandomify` | `pip3 install pyrandomify` |



#### Usage

```python
from randomify import Text, Digits, Generate

# generating text a-Z
Text().generate(lenght=15)
# output: AUyapxMKqDzSyQx

# generating numbers 0-9
Digits().generate(lenght=15)
# output: 500797162564347

# generating random printable symbols (text, digits, symbols, spaces)
Generate().generate(lenght=15)
# output: q?1wQ#}jpR*;w-.
```



