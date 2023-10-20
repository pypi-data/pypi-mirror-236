import pandas as pd
import pytest
from data_geocoding_utils.disambiguation import disambiguate, disambiguate_dict, filter_dict_on_col_value, unfold, unfold_dict

class CityGeocode:
    def __init__(self, geo_point, country_alpha3, city, postalcode, administrative_level_1, administrative_level_2,
                 country_alpha2, source):
        self.geo_point = geo_point
        self.country_alpha3 = country_alpha3
        self.city = city
        self.postalcode = postalcode
        self.administrative_level_1 = administrative_level_1
        self.administrative_level_2 = administrative_level_2
        self.country_alpha2 = country_alpha2
        self.source = source

    def __eq__(self, other):
        if self.geo_point!=other.geo_point:
            return False
        elif self.country_alpha3!=other.country_alpha3:
            return False
        elif self.city!=other.city:
            return False
        elif self.postalcode!=other.postalcode:
            return False
        elif self.administrative_level_1!=other.administrative_level_1:
            return False
        elif self.administrative_level_2!=other.administrative_level_2:
            return False
        elif self.country_alpha2!=other.country_alpha2:
            return False
        elif self.source!=other.source:
            return False
        else:
            return True

@pytest.fixture
def sample_city_geocode_data():
    data = {
        'lat': [40.7128, 34.0522],
        'lon': [-74.0060, -118.2437],
        'CityGeocode': [
            CityGeocode(geo_point=(40.7128, -74.0060), country_alpha3='FRA', city='New York', postalcode='10001',
                        administrative_level_1='New York', administrative_level_2='New York County', country_alpha2='FR', source='GoogleMaps'),
            CityGeocode(geo_point=(34.0522, -118.2437), country_alpha3='FRA', city='Saint Andreas', postalcode='90001',
                        administrative_level_1='California', administrative_level_2='Los Angeles County', country_alpha2='FR', source='GoogleMaps')
        ]
    }
    return data

@pytest.fixture
def sample_city_geocode_df(sample_city_geocode_data):
    data = sample_city_geocode_data
    return pd.DataFrame(data)

def test_unfold(sample_city_geocode_df):
    expected_output = pd.DataFrame({'lat': {0: 40.7128, 1: 34.0522},
                                    'lon': {0: -74.006, 1: -118.2437},
                                    'geo_point': {0: (40.7128, -74.006), 1: (34.0522, -118.2437)},
                                    'country_alpha3': {0: 'FRA', 1: 'FRA'},
                                    'city': {0: 'New York', 1: 'Saint Andreas'},
                                    'postalcode': {0: '10001', 1: '90001'},
                                    'administrative_level_1': {0: 'New York', 1: 'California'},
                                    'administrative_level_2': {0: 'New York County', 1: 'Los Angeles County'},
                                    'country_alpha2': {0: 'FR', 1: 'FR'},
                                    'source': {0: 'GoogleMaps', 1: 'GoogleMaps'}})
    # Create a DataFrame
    city_geocode_df = sample_city_geocode_df
    print(city_geocode_df.to_dict())

    # Call the function
    unfolded_df = unfold(city_geocode_df)

    pd.testing.assert_frame_equal(expected_output, unfolded_df)


def test_unfold_dict(sample_city_geocode_data):
    data ={'lat': {0: 40.7128, 1: 34.0522},
           'lon': {0: -74.006, 1: -118.2437},
           'CityGeocode': {0: CityGeocode(geo_point=(40.7128, -74.0060),
                                          country_alpha3='FRA', city='New York',
                                          postalcode='10001',
                                          administrative_level_1='New York',
                                          administrative_level_2='New York County',
                                          country_alpha2='FR',
                                          source='GoogleMaps'),
                            1: CityGeocode(geo_point=(34.0522, -118.2437),
                                           country_alpha3='FRA',
                                           city='Saint Andreas',
                                           postalcode='90001',
                                           administrative_level_1='California',
                                           administrative_level_2='Los Angeles County',
                                           country_alpha2='FR',
                                           source='GoogleMaps')}}
    unfolded_data = unfold_dict(data)
    expected_output = { 'lat': {0: 40.7128, 1: 34.0522},
                        'lon': {0: -74.006, 1: -118.2437},
                        'geo_point': {0: (40.7128, -74.006), 1: (34.0522, -118.2437)},
                        'country_alpha3': {0: 'FRA', 1: 'FRA'},
                        'city': {0: 'New York', 1: 'Saint Andreas'},
                        'postalcode': {0: '10001', 1: '90001'},
                        'administrative_level_1': {0: 'New York', 1: 'California'},
                        'administrative_level_2': {0: 'New York County', 1: 'Los Angeles County'},
                        'country_alpha2': {0: 'FR', 1: 'FR'},
                        'source': {0: 'GoogleMaps', 1: 'GoogleMaps'}}
    assert unfolded_data==expected_output

def test_filter_dict_on_col_value():
    # Sample data for testing
    input_dict = {
        'col1': {'index1': 'value1', 'index2': 'value2'},
        'col2': {'index1': 1, 'index2': 3},
        'col3': {'index1': 'value3', 'index2': 'value4'}
    }

    filtered_result = filter_dict_on_col_value(input_dict, 'col2', 1)

    expected_output = {
        'col1': {'index1': 'value1'},
        'col2': {'index1': 1},
        'col3': {'index1': 'value3'}
    }
    assert filtered_result==expected_output

def test_disambiguate(sample_city_geocode_df):
    # Test case with a single entry, should return the same entry
    result_single_entry = disambiguate(sample_city_geocode_df.iloc[[0]], 'New York', 'FRA')
    pd.testing.assert_frame_equal(sample_city_geocode_df.iloc[[0]], result_single_entry, check_dtype=False)

    # Test case with exact match on basic shaping, should return the matched entry
    result_basic_match = disambiguate(sample_city_geocode_df, 'New York', 'FRA')
    pd.testing.assert_frame_equal(sample_city_geocode_df.iloc[[0]], result_basic_match, check_dtype=False)

    # Test case with exact match on advanced shaping, should return the matched entry
    result_advanced_match = disambiguate(sample_city_geocode_df, 'ST ANDREAS', 'FRA')
    pd.testing.assert_frame_equal(sample_city_geocode_df.iloc[[1]].reset_index(drop=True),
                                  result_advanced_match.reset_index(drop=True),check_dtype=False)

    # Test case with ambiguous advanced shaping, should return the first entry
    result_ambiguous_advanced = disambiguate(sample_city_geocode_df, 'N3W Y0RK', 'FRA')
    pd.testing.assert_frame_equal(sample_city_geocode_df.iloc[[0]], result_ambiguous_advanced, check_dtype=False)


def test_disambiguate_dict():
    sample_city_geocode_dict = {'lat': {0: 40.7128, 1: 34.0522},
                                'lon': {0: -74.006, 1: -118.2437},
                                'CityGeocode': {0: CityGeocode(geo_point=(40.7128, -74.0060),
                                                               country_alpha3='FRA', city='New York',
                                                               postalcode='10001',
                                                               administrative_level_1='New York',
                                                               administrative_level_2='New York County',
                                                               country_alpha2='FR',
                                                               source='GoogleMaps'),
                                                1: CityGeocode(geo_point=(34.0522, -118.2437),
                                                               country_alpha3='FRA',
                                                               city='Saint Andreas',
                                                               postalcode='90001',
                                                               administrative_level_1='California',
                                                               administrative_level_2='Los Angeles County',
                                                               country_alpha2='FR',
                                                               source='GoogleMaps')}}
    output_ny = {'lat': {0: 40.7128},
                 'lon': {0: -74.006},
                 'CityGeocode': {0: CityGeocode(geo_point=(40.7128, -74.0060),
                                                country_alpha3='FRA', city='New York',
                                                postalcode='10001',
                                                administrative_level_1='New York',
                                                administrative_level_2='New York County',
                                                country_alpha2='FR',
                                                source='GoogleMaps')}}
    output_la = {'lat': {1: 34.0522},
                 'lon': {1: -118.2437},
                 'CityGeocode': {1: CityGeocode(geo_point=(34.0522, -118.2437),
                                                country_alpha3='FRA',
                                                city='Saint Andreas',
                                                postalcode='90001',
                                                administrative_level_1='California',
                                                administrative_level_2='Los Angeles County',
                                                country_alpha2='FR',
                                                source='GoogleMaps')}}

    # Test case with a single entry, should return the same entry
    result_single_entry = disambiguate_dict(output_ny, 'New York', 'FRA')
    assert result_single_entry == output_ny

    # Test case with exact match on basic shaping, should return the matched entry
    result_basic_match = disambiguate_dict(sample_city_geocode_dict, 'New York', 'FRA')
    assert result_basic_match == output_ny

    # Test case with exact match on advanced shaping, should return the matched entry
    result_advanced_match = disambiguate_dict(sample_city_geocode_dict, 'ST ANDREAS', 'FRA')
    assert result_advanced_match == output_la

    # Test case with ambiguous advanced shaping, should return a dictionary with a single entry
    result_ambiguous_advanced = disambiguate_dict(sample_city_geocode_dict, 'N3W Y0RK', 'FRA')
    assert result_ambiguous_advanced==output_ny





