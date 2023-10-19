# simple-range
Weka-inspired index and range using human-readable 1-based indices and placeholders, 
e.g.: `last`, `first-last`, `1-10,12,20-last`.

Available placeholders:
* `first` - the first index
* `second` - the second index
* `third` - the third index
* `last_2` - the third to last index
* `last_1` - the second to last index
* `last` - the last index


## Installation

```
pip install simple-range
```

## Functionality

* Index
  
  * The `simple_range.Index` class parses and interprets a single index.
  * The `simple_range.index_value` method is convenience method to 
    immediately parse and return an index as int.    

* Range
  
  * The `simple_range.Range` class parses and interprets ranges.
  * The `simple_range.range_indices` method is convenience method to 
    immediately parse and return int indices.    


## Examples

The following code:

```python
from simple_range import Range, range_indices

r = Range("1-3", maximum=10)
print(r, "-->", r.indices())
r = Range("first-last", maximum=10) 
print(r, "-->", r.indices(zero_based=False))
r = Range("first-3,11,14-14,30,last", maximum=40)
print(r, "-->", r.indices())
print(r, "-->", r.indices(zero_based=False))
print(range_indices("2-last_2", maximum=10))
```

Will generate this output:

```
1-3 --> [0, 1, 2]
first-last --> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
first-3,11,14-14,30,last --> [0, 1, 2, 10, 13, 29, 39]
first-3,11,14-14,30,last --> [1, 2, 3, 11, 14, 30, 40]
[1, 2, 3, 4, 5, 6, 7]
```

And this code:

```python
from simple_range import Index, index_value

r = Index("1", maximum=10)
print(r, "-->", r.value())
r = Index("second", maximum=10)
print(r, "-->", r.value(zero_based=False))
r = Index("last", maximum=40)
print(r, "-->", r.value())
print(r, "-->", r.value(zero_based=False))
print(index_value("last_1", maximum=100, zero_based=False))
```

outputs this:

```
1 --> 0
second --> 2
last --> 39
last --> 40
99
```
