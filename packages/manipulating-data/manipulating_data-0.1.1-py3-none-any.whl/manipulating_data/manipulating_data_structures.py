import pandas as pd
from typing import Union, List
from copy import copy
import numpy as np


def flatten_iterab(iterab : Union[list, tuple]) -> Union[list, tuple] :
    """
    Flattens an iterable of iterables.
    
    Parameters
    ----------
    iterab : list or tuple.
        A nested iterable.
    
    Returns
    -------
    list or tuple.
        A flattened list if the input is a list,
        a flattened tuple if the input is a tuple.
    
    Example
    -------
    flatten_iterab([[1, 2], [3, 4]])
    
        [1, 2, 3, 4]
    """

    if isinstance(iterab, tuple) :
        return tuple([item for sublist in iterab for item in sublist])

    return [item for sublist in iterab for item in sublist]


def replace_value_of_iterab(iterab, value, new_value) :
    """
    Replaces a value in an iterable with a new value.

    Parameters
    ----------
    iterab : list, tuple, set or pd.Series.
        An iterable where we want to replace one value
        with a new value.
    value : any.
        The value to be replaced.
    new_value : any.
        The new value.
    
    Returns
    -------
    list.
        The list with the one value replaced and
        the rest the same as in the original iterable.

    Example
    -------
    replace_value_of_iterab([1, 2, 3, 4, 5], 3, 10)

        [1, 2, 10, 4, 5]
    """    

    old_to_new = dict(zip(iterab, iterab))
    old_to_new[value] = new_value
    new_vals = [old_to_new[i] for i in iterab]

    return new_vals

def slicing_diction(diction : dict, stop : Union[int, None] = None, start = 0,\
                    only_values = False, only_keys = False, vals_limit = None) -> Union[dict, list]:
    
    """
    Takes a dictionary and start and stop index and
    returns a smaller (or same size) dictionary whose
    indices of key, value pairs are between start and stop index,
    in a fashion similar to list slicing.
    
    Parameters
    ----------
    diction : dict. Any dictionary.
    stop : int or None. The index of the last key value pair that we want to
                        include in our dictionary slice.
    
    start : int. Defaults to 0.
    
    Returns
    -------
    list (keys or values of a smaller dictionary) if only_values is True or only_keys is True.
    dict (a smaller dictionary) otherwise.
        
    
    
    Examples
    --------
    slicing_diction({'John' : 'Doe', 'James' : 'Bond', 'Amy' : 'Robertson'})
    
        {'John': 'Doe', 'James': 'Bond', 'Amy': 'Robertson'}
    
    slicing_diction({'John' : 'Doe', 'James' : 'Bond', 'Amy' : 'Robertson'}, stop = 2)
    
        {'John': 'Doe', 'James': 'Bond'}
        
    slicing_diction({'John' : 'Doe', 'James' : 'Bond', 'Amy' : 'Robertson'}, start = 1, stop = None)
    
        {'James': 'Bond', 'Amy': 'Robertson'}
        
    slicing_diction({'John' : 'Doe', 'James' : 'Bond', 'Amy' : 'Robertson'}, start = 1)
    
        {'James': 'Bond', 'Amy': 'Robertson'}
    """
    
    if sum([only_values, only_keys]) == 2:
        raise ValueError("If you want to see the full dictionary leave only_values and only_keys False.")
    
    keys = [k for k in diction.keys()][start : stop]
    values = [v for v in diction.values()][start : stop]

    if vals_limit :
        values = [v[ : vals_limit] if isinstance(v, list) else v\
                  for v in values]
    
    if only_values:
        return values
    
    if only_keys:
        return keys
    
    small_diction = dict(zip(keys, values))
    
    return small_diction

def squeeze_diction(start_key : Union[str, int, float, tuple],\
                    end_key : Union[str, int, float, tuple],\
                    diction : dict, aggregation : Union[None, str] = None) -> dict:
    
    """
    Reduces the number of dictionary keys while keeping all the values.
    For example, if we had, say, some weekly sales data
    and we would want to convert it to monthly data, we can
    assign the first 4 weeks values to the first month, the next 4 weeks
    values to the second month, etc.
    
    
    Parameters
    ----------
    diction : dict.
    start_key : str or int or float or tuple. The key of a diction dictionary.
    end_key : str or int or float or tuple. The key of a diction dictionary.
    aggregation : str or None. The aggregation function to be applied to the values
                                between start_key and end_key. If None, no aggregation
                                is applied and all the values are listed.
                                The valid aggregation functions are 'sum', 'min', 'max', 'np.mean',
                                'np.median', 'np.std', 'np.var', 'np.prod', 'np.sum', 'np.min', 'np.max'.
    
    Returns
    -------
    dict.
    
    Examples
    -------
    squeeze_diction(diction = {'week1' : 50, 'week2' : 30, 'week3' : 50}, start_key = 'week1',\
               end_key = 'week3')
        
        {'From week1 to week3': [50, 30, 50]}

    squeeze_diction(diction = {'week1' : 50, 'week2' : 30, 'week3' : 50}, start_key = 'week1',\
               end_key = 'week3', aggregation='np.mean')
            
        {'From week1 to week3': 43.333333333333336}
    
    """
    if not ( ( isinstance( aggregation, str ) ) or ( aggregation is None ) ):
        raise ValueError("The aggregation parameter must be a string or None.")
    
    key_lab1, key_lab2 = copy(start_key), copy(end_key)

    keys_indices = dict(zip([k for k in diction.keys()], range(len([k for k in diction.keys()]))))

    start_key = keys_indices[start_key]
    end_key = keys_indices[end_key]

    squeezed_diction = {'From {} to {}'.format(key_lab1, key_lab2) :\
                        slicing_diction(diction, stop = end_key + 1, start = start_key, only_values = True)}
    
    if aggregation :
        aggregated_diction = {k : eval(aggregation)(v) for k, v in squeezed_diction.items()}

        return aggregated_diction

    return squeezed_diction
    

def concat_diction(dictions_iterab, non_overlapping_keys = False) -> dict :
    
    """
    Takes a list of dictionaries and output
    one big dictionary with the unique keys of
    the original dictionaries as keys and the combined
    values sharing the same key as values.
    The keys are strings and the values are lists.
    
    
    Parameters
    ----------
    dictions_iterab : list. List of dictionaries, 
                      which we want to combine into one.
                      
    Returns
    -------
    dict.

    Examples
    --------
    concat_diction([{'a' : 1, 'b' : 2}, {'a' : 3, 'b' : 4}])

        {'a': [1, 3], 'b': [2, 4]}

    concat_diction([{'a' : 1, 'b' : 2}, {'c' : 3, 'd' : 4}], non_overlapping_keys = True)

        {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    """
        

    
    
    keys = [k for di in dictions_iterab for k in di.keys()]
    values = [v for di in dictions_iterab for v in di.values()]

    if non_overlapping_keys :
        return dict(zip(keys, values))

    keys_uniq = list(set(keys))
    values_empty = [ [ ] for _ in range(len(keys_uniq))]
    big_diction = dict(zip(keys_uniq, values_empty))
    pairs = [*zip(keys, values)]
    
    for p in pairs :
        key = p[0]
        value = p[1]
        big_diction[key].append(value)
    
    return big_diction

def get_values_under_key_from_iterable_of_dictions(dictions_iterab, key) -> list :
    """
    This function takes an iterable of dictionaries and returns a list of values under a given key, which
    can be NaN if the key is not present in some dictionary.

    Parameters
    ----------
    dictions_iterab : iterable of dictionaries
        The iterable of dictionaries from which the values under a given key are to be extracted.
    key : str.
        The key under which the values are to be extracted.
    
    Returns
    -------
    list.

    Example
    -------
    >>> get_values_under_key_from_iterable_of_dictions( [ {'a' : 1, 'b' : 2}, {'a' : 3, 'b' : 4} ], 'a' )
            
            [1, 3]
    """
    return [d.get(key, np.nan) for d in dictions_iterab]

def is_scalar(item):
    """
    Checks if an item is a scalar (int, float, str, bool).

    Parameter
    ---------
    item : any.
        A Python object, for which we want to find out
        whether it is like an array or like a float/str etc.
    
    Returns
    -------
    bool.
        True if the item is a scalar, False otherwise.
    
    Example
    -------
    is_scalar(1)
        
        >>> True
    
    is_scalar(True)

        >>> True
    
    is_scalar( [ 'a', 'b', 'c' ] )

        >>> False
    """
    return isinstance(item, (int, float, str, bool))

def are_all_scalars(input_list):
    """"
    Checks if all the items in a list are scalars (int, float, str).

    Parameter
    ---------
    input_list : list.

    Returns
    -------
    bool.
        True if all the items in a list are scalars, False otherwise.
    
    Example
    -------
    are_all_scalars([ 1, 'a', 3.77 ])
        
        >>> True
    
    are_all_scalars([ 1, 'a', [ 3.77 ] ])
        
        >>> False
    """
    for item in input_list:
        if not is_scalar(item):
            return False
    return True

def intersection_of_n_sets(iterable_of_sets : list) -> set:
    
    """
    Takes a list of sets and returns the intersection
    of those sets.
    
    Parameters
    ----------
    iterable_of_sets : list.
    
    Returns
    -------
    set.

    Example
    -------
    intersection_of_n_sets([{1, 2, 3}, {2, 3, 4}, {3, 4, 5}])
        
        {3}
    """
    
    string = '{}' + '.intersection({})' * (len(iterable_of_sets) - 2)\
             + '.intersection({})'
    iterab_of_txts = string.split('.')
    iterab_of_formatted_texts = [iot.format(ios) for iot, ios in zip(\
        iterab_of_txts, iterable_of_sets)]
    new_text = '.'.join(iterab_of_formatted_texts)
    
    return eval(new_text)


def intersection_of_dfs(dataframes_iterab: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Parameter
    ----------
    dataframes_iterab : list of DataFrames.

    Returns
    -------
    pd.DataFrame.

    Example
    -------
    print(booking.columns)

        Index(['thumbnail', 'title', 'stars', 'preferredBadge', 'promotedBadge',
            'location', 'subwayAccess', 'sustainability', 'distanceFromCenter',
            'highlights', 'link', 'price_value', 'price_taxesAndCharges',
            'price_currency', 'rating_score', 'rating_scoreDescription',
            'rating_reviews', 'marketplace'],
        dtype='object')

    print(airbnb.columns)

        Index(['thumbnail', 'title', 'subtitles', 'rating', 'link', 'price_value',
            'price_period', 'price_currency', 'marketplace'],
        dtype='object')

    print(hotelscom.columns)

        Index(['title', 'isAd', 'location', 'paymentOptions', 'highlightedAmenities',
            'link', 'snippet_title', 'snippet_text', 'price_value',
            'price_withTaxesAndCharges', 'price_currency', 'rating_score',
            'rating_reviews', 'marketplace'],
        dtype='object')

    # the output will have only the columns that are present in all three dataframes

    print(intersection_of_dfs([airbnb, booking, hotelscom]).head())

        link                                           marketplace price_currency  \
    0  https://www.airbnb.com/rooms/647664199858827562      airbnb              $   
    1            https://www.airbnb.com/rooms/41220512      airbnb              $   
    2            https://www.airbnb.com/rooms/30881310      airbnb              $   
    3             https://www.airbnb.com/rooms/2591901      airbnb              $   
    4            https://www.airbnb.com/rooms/19075304      airbnb              $   

    price_value                                       title  
    0           31                   Private room in Tempelhof  
    1           40                       Private room in Mitte  
    2          108               Hotel room in Prenzlauer Berg  
    3           34                 Private room in Lichtenberg  
    4           71  Private room in Charlottenburg-Wilmersdorf  

        """

    common_cols = intersection_of_n_sets([{c for c in df.columns} for df in dataframes_iterab])
    common_cols = sorted(list(common_cols))

    return pd.concat([df[common_cols] for df in dataframes_iterab], axis=0)


def make_set_into_ordered_list(some_set : set, reverse = False,\
                               key = None) -> list :
    """
    Takes a set and returns a list with the same elements.
    """
    
    return sorted([*some_set], reverse = reverse, key = key)

def check_if_frames_are_equal(df_a, df_b) -> bool :
    """
    Checks if two dataframes are equal (have the same columns),
    regardless of the order of the columns.

    Parameters
    ----------
    df_a : pandas.DataFrame.
        First dataframe.
    df_b : pandas.DataFrame.
        Second dataframe.
    
    Returns
    -------
    bool.
        True if the dataframes are equal, False otherwise.
    
    Example
    -------
    df_a = pd.DataFrame({ 0: ['a', 'b', 'c'], 1: [9, 8, 7], 2: [True, True, False] })
    df_b = pd.DataFrame({ 0: [9, 8, 7], 1: [True, True, False], 2: ['a', 'b', 'c'] })
    df_c = pd.DataFrame({ 0: [9, 8, 7], 1: [True, True, False], 2: ['a', 'd', 'c'] })

    check_if_frames_are_equal(df_a, df_b)
        >>> True
    
    check_if_frames_are_equal(df_a, df_c)
        >>> False
    
    """
    
    return {tuple(df_a[c]) for c in df_a.columns} == {tuple(df_b[c]) for c in df_b.columns}