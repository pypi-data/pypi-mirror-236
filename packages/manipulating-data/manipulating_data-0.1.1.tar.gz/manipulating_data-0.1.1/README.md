# manipulating_data

manipulating_data is a package for slicing and dicing Python data structures,
such as dictionaries, sets, or pandas DataFrames.

### Features

- Conveniently examine the contents of dictionaries by subsetting them in a fashion similar to list slicing.
- Determine whether two pandas DataFrames are equal (have the same values in the same columns).
- Find the intersection of an arbitrary number of sets.
- Combine dictionaries with parts of the data into a larger dictionary with all of the data.
- Determine the intersection (shared columns) of an arbitrary number of pandas DataFrames.


### Installation

```
pip install manipulating_data
```

### Usage

```
import manipulating_data as md

md.intersection_of_n_sets( [ {'a', 'b', 'c'}, {'a', 'b', 'd'}, {'a', 'b', 'e'} ] )
	
	{'a', 'b'}

md.slicing_diction( { 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}, stop = 2 )
	
	{'a': 1, 'b': 2}

md.concat_diction( [ {'USA' : 73899, 'Canada' : 89743}, {'USA' : 85876, 'Canada' : 56899} ] )
	
	{'Canada': [89743, 56899], 'USA': [73899, 85876]}
```
### Contributing

Contributions from the community to improve this project are welcomed. To contribute, please follow these steps:

1. Fork this repository.
2. Make your changes.
3. Create a pull request.

We appreciate your help in making this project better!

### License

[MIT License](./LICENSE)

