from typing import Any

import pandas as pd
from .shaping_rules import (advanced_city_shaping,
                                     alpha3_to_alpha2_map, basic_city_shaping)

def unfold(city_geocode_df: pd.DataFrame) -> pd.DataFrame:
    """
    Unfolds a DataFrame containing CityGeocode information.

    Args:
        city_geocode_df (pandas.DataFrame): A DataFrame containing CityGeocode information.

    Returns:
        pandas.DataFrame: A new DataFrame with unfolded columns, including 'lat', 'lon', 'geo_point',
        'country_alpha3', 'city', 'postalcode', 'administrative_level_1', 'administrative_level_2',
        'country_alpha2', and 'source'.

    Example:
        city_geocode_df = pd.DataFrame({
            'lat': [40.7128, 34.0522],
            'lon': [-74.0060, -118.2437],
            'CityGeocode': [
                CityGeocode(geo_point=(40.7128, -74.0060), country_alpha3='USA', city='New York', postalcode='10001',
                            administrative_level_1='New York', administrative_level_2='New York County', country_alpha2='US', source='Google'),
                CityGeocode(geo_point=(34.0522, -118.2437), country_alpha3='USA', city='Los Angeles', postalcode='90001',
                            administrative_level_1='California', administrative_level_2='Los Angeles County', country_alpha2='US', source='Google')
            ]
        })

        unfolded_df = unfold(city_geocode_df)
        print(unfolded_df)
    """
    unfolded_df = city_geocode_df[['lat', 'lon']].copy(deep=True)

    unfolded_df['geo_point'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].geo_point, axis=1)
    unfolded_df['country_alpha3'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].country_alpha3, axis=1)
    unfolded_df['city'] = city_geocode_df.apply(lambda row: row['CityGeocode'].city, axis=1)
    unfolded_df['postalcode'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].postalcode, axis=1)
    unfolded_df['administrative_level_1'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].administrative_level_1, axis=1)
    unfolded_df['administrative_level_2'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].administrative_level_2, axis=1)
    unfolded_df['country_alpha2'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].country_alpha2, axis=1)
    unfolded_df['source'] = city_geocode_df.apply(
        lambda row: row['CityGeocode'].source, axis=1)
    return unfolded_df


def unfold_dict(city_geocode_dict: dict) -> dict:
    """
    Unfolds a dictionary containing CityGeocode information.

    Args:
        city_geocode_dict (dict): A dictionary containing 'lat', 'lon', and 'CityGeocode' keys.

    Returns:
        dict: A new dictionary with unfolded keys, including 'lat', 'lon', 'geo_point',
        'country_alpha3', 'city', 'postalcode', 'administrative_level_1', 'administrative_level_2',
        'country_alpha2', and 'source'.

    Example:
        city_geocode_dict = {
            'lat': [40.7128, 34.0522],
            'lon': [-74.0060, -118.2437],
            'CityGeocode': {
                'index1': CityGeocode(geo_point=(40.7128, -74.0060), country_alpha3='USA', city='New York', postalcode='10001',
                                       administrative_level_1='New York', administrative_level_2='New York County', country_alpha2='US', source='Google'),
                'index2': CityGeocode(geo_point=(34.0522, -118.2437), country_alpha3='USA', city='Los Angeles', postalcode='90001',
                                       administrative_level_1='California', administrative_level_2='Los Angeles County', country_alpha2='US', source='Google')
            }
        }

        unfolded_dict = unfold_dict(city_geocode_dict)
        print(unfolded_dict)
    """
    unfolded_dict = {
        'lat': city_geocode_dict['lat'],
        'lon': city_geocode_dict['lon'],
        'geo_point': {idx: x.geo_point for idx, x in city_geocode_dict['CityGeocode'].items()},
        'country_alpha3': {idx: x.country_alpha3 for idx, x in city_geocode_dict['CityGeocode'].items()},
        'city': {idx: x.city for idx, x in city_geocode_dict['CityGeocode'].items()},
        'postalcode': {idx: x.postalcode for idx, x in city_geocode_dict['CityGeocode'].items()},
        'administrative_level_1': {idx: x.administrative_level_1 for idx, x in city_geocode_dict['CityGeocode'].items()},
        'administrative_level_2': {idx: x.administrative_level_2 for idx, x in city_geocode_dict['CityGeocode'].items()},
        'country_alpha2': {idx: x.country_alpha2 for idx, x in city_geocode_dict['CityGeocode'].items()},
        'source': {idx: x.source for idx, x in city_geocode_dict['CityGeocode'].items()},
    }

    return unfolded_dict

def filter_dict_on_col_value(input_dict: dict, col_to_filter_on: str, col_value: Any) -> dict:
    """
    Filters a nested dataframe-like dictionary based on a specified column and value.

    Args:
        input_dict (dict): The input nested dictionary to be filtered.
        col_to_filter_on (str): The column key to filter on in the nested dictionaries.
        col_value: The value to filter for in the specified column.

    Returns:
        dict: A new nested dictionary containing only the items that match the specified column value.

    Example:
        input_dict = {
            'col1': {'index1': 'value1', 'index2': 'value2'},
            'col2': {'index1': 1, 'index2': 3},
            'col3': {'index1': 'value3', 'index2': 'value4'}
        }

        filtered_result = filter_dict_on_col_value(input_dict, 'col2', 1)
        print(filtered_result)
    """
    return({col: {k: input_dict[col][k]} for col in input_dict for k in input_dict[col_to_filter_on] if input_dict[col_to_filter_on][k]==col_value})

def disambiguate(city_geocode_df: pd.DataFrame, input_city: str, input_country_code: str) -> pd.DataFrame:
    """
    Disambiguates and selects the most relevant entry from a DataFrame containing CityGeocode information.

    This function is designed to handle cases where multiple entries in the input DataFrame may match the provided
    city name and country code. It prioritizes disambiguation through basic and advanced city shaping techniques.

    Args:
        city_geocode_df (pandas.DataFrame): A DataFrame containing CityGeocode information.
        input_city (str): The input city name for disambiguation.
        input_country_code (str): The country code (either alpha-2 or alpha-3) corresponding to the input city.

    Returns:
        pandas.DataFrame: The selected entry from the input DataFrame after disambiguation.

    Example:
        city_geocode_df = pd.DataFrame({
            'lat': [40.7128, 34.0522],
            'lon': [-74.0060, -118.2437],
            'CityGeocode': [
                CityGeocode(geo_point=(40.7128, -74.0060), country_alpha3='USA', city='New York', postalcode='10001',
                            administrative_level_1='New York', administrative_level_2='New York County', country_alpha2='US', source='Google'),
                CityGeocode(geo_point=(34.0522, -118.2437), country_alpha3='USA', city='Los Angeles', postalcode='90001',
                            administrative_level_1='California', administrative_level_2='Los Angeles County', country_alpha2='US', source='Google')
            ]
        })

        result = disambiguate(city_geocode_df, 'New York', 'USA')
        print(result)
    """
    if city_geocode_df.shape[0] == 1:
        return city_geocode_df.iloc[0].to_frame().T

    if len(input_country_code) == 2:
        input_alpha2 = input_country_code
    else:
        input_alpha2 = alpha3_to_alpha2_map[input_country_code]

    if 'CityGeocode' in city_geocode_df.columns:
        unfolded_df = unfold(city_geocode_df)
    else:
        unfolded_df = city_geocode_df


    unfolded_df['shaped_city_basic'] = unfolded_df['city'].apply(
        lambda city: basic_city_shaping(city))

    basic_matching_df = unfolded_df[unfolded_df['shaped_city_basic'] == basic_city_shaping(
        input_city)]
    if len(basic_matching_df) == 1:
        return city_geocode_df.loc[basic_matching_df.index].iloc[0].to_frame().T

    unfolded_df['shaped_city_advanced'] = unfolded_df.apply(
        lambda row: advanced_city_shaping(row['city'], row['country_alpha2']), axis=1)

    advanced_matching_df = unfolded_df[unfolded_df['shaped_city_advanced']
                                       == advanced_city_shaping(input_city, input_alpha2)]

    if len(advanced_matching_df) == 1:
        return city_geocode_df.loc[advanced_matching_df.index].iloc[0].to_frame().T

    else:
        return city_geocode_df.iloc[0].to_frame().T

def disambiguate_dict(city_geocode_dict: dict, input_city: str, input_country_code: str) -> dict:
    """
    Disambiguates and selects the most relevant entry from a dictionary containing CityGeocode information.

    This function is designed to handle cases where multiple entries in the input dictionary may match the provided
    city name and country code. It prioritizes disambiguation through basic and advanced city shaping techniques.

    Args:
        city_geocode_dict (dict): A dictionary containing 'lat', 'lon', and 'CityGeocode' keys.
        input_city (str): The input city name for disambiguation.
        input_country_code (str): The country code (either alpha-2 or alpha-3) corresponding to the input city.

    Returns:
        dict: A new dictionary containing only the most relevant entry after disambiguation.

    Example:
        city_geocode_dict = {
            'lat': [40.7128, 34.0522],
            'lon': [-74.0060, -118.2437],
            'CityGeocode': {
                'index1': CityGeocode(geo_point=(40.7128, -74.0060), country_alpha3='USA', city='New York', postalcode='10001',
                                       administrative_level_1='New York', administrative_level_2='New York County', country_alpha2='US', source='Google'),
                'index2': CityGeocode(geo_point=(34.0522, -118.2437), country_alpha3='USA', city='Los Angeles', postalcode='90001',
                                       administrative_level_1='California', administrative_level_2='Los Angeles County', country_alpha2='US', source='Google')
            }
        }

        result = disambiguate_dict(city_geocode_dict, 'New York', 'USA')
        print(result)
    """
    if len(city_geocode_dict[list(city_geocode_dict.keys())[0]]) == 1:
        return city_geocode_dict

    if len(input_country_code) == 2:
        input_alpha2 = input_country_code
    else:
        input_alpha2 = alpha3_to_alpha2_map[input_country_code]

    if 'CityGeocode' in city_geocode_dict:
        unfolded_dict = unfold_dict(city_geocode_dict)
    else:
        unfolded_dict = city_geocode_dict

    unfolded_dict['shaped_city_basic'] = {idx: basic_city_shaping(city) for idx, city in unfolded_dict['city'].items()}
    basic_shaped_city =  basic_city_shaping(input_city)
    basic_matching_dict = filter_dict_on_col_value(unfolded_dict, 'shaped_city_basic', basic_shaped_city)

    if len(list(basic_matching_dict.keys())) > 0:
        if len(basic_matching_dict[list(basic_matching_dict.keys())[0]]) == 1:
            idx_to_return = list(basic_matching_dict[list(basic_matching_dict.keys())[0]].keys())[0]
            return {col: {idx_to_return: city_geocode_dict[col][idx_to_return]} for col in city_geocode_dict}

    unfolded_dict['shaped_city_advanced'] = {idx: advanced_city_shaping(unfolded_dict['city'][idx],
                                                                        unfolded_dict['country_alpha2'][idx]) for idx in unfolded_dict['city']}
    advanced_shaped_city = advanced_city_shaping(input_city, input_alpha2)
    advanced_matching_dict = filter_dict_on_col_value(unfolded_dict, 'shaped_city_advanced', advanced_shaped_city)
    if len(list(advanced_matching_dict.keys())) > 0:
        if len(advanced_matching_dict[list(advanced_matching_dict.keys())[0]]) == 1:
            idx_to_return = list(advanced_matching_dict[list(advanced_matching_dict.keys())[0]].keys())[0]
    else:
        idx_to_return = list(city_geocode_dict[list(city_geocode_dict.keys())[0]].keys())[0]
    return {col: {idx_to_return: city_geocode_dict[col][idx_to_return]} for col in city_geocode_dict}