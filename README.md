eigenPath
=========

Easily search for data in python structures using xpath-like syntax.

The idea is to be able to search a variable structure for sub-structures without having to chain multiple gets i.e. `data.get('name', {}).get('first_name', '')` . This is especially useful when a key may or may not exist, and the user doesn't want a KeyError when accessing that key. For example, in Genshi/Dojo templates, the template may not require `name` to be defined but its presence will result in the name being displayed.


Usage (see tests.py for more details/examples):
```
data = {'level1-dict': {level2: 'two', level2b: 'to be'}, 
        'matrix': [{'row':[1,0,0], 'desc': 'First row in list'},{'row':[0,1,0]},{'row':[0,0,1]}]
      }

path_get(data, 'level1-dict/level2')
> 'two'

path_get(data, '/matrix/row') #Return all elements named 'row'
>[[1,0,0], [0,1,0], [0,0,1]]

path_get(data, '/matrix/row[0]') #Return first element named 'row'
> [[1,0,0]]
```
