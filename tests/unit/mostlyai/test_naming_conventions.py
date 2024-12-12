import pytest
from datamodel_code_generator.reference import camel_to_snake

from mostlyai.client._naming_conventions import (
    _snake_to_camel,
    _map_snake_to_camel_case,
    _map_camel_to_snake_case,
)


@pytest.mark.parametrize(
    "snake_str, expected",
    [
        ("snake_case", "snakeCase"),
        ("this_is_a_test", "thisIsATest"),
        ("alreadyCamelCase", "alreadyCamelCase"),
    ],
)
def test__snake_to_camel_param(snake_str, expected):
    assert _snake_to_camel(snake_str) == expected


def test_map_snake_to_camel_case():
    input_data = {
        "snake_case_key": "value",
        "nested_dict": {
            "another_snake_case": 123,
            "deep_nested_dict": {
                "yet_another_key": "deepValue",
                "someCamelCaseKey": "someOtherValue",
                "normalNumber": 42,
            },
        },
        "list_of_dicts": [{"list_snake_case": "item1"}, {"another_list_key": "item2"}],
        "mixed_list": ["simpleString", {"nested_snake": "nestedValue"}, 3.14],
        "alreadyCamelCase": "unchangedValue",
        "no_underscore_key": "noChange",
        "empty_string_key": "",
    }

    expected_output = {
        "snakeCaseKey": "value",
        "nestedDict": {
            "anotherSnakeCase": 123,
            "deepNestedDict": {
                "yetAnotherKey": "deepValue",
                "someCamelCaseKey": "someOtherValue",
                "normalNumber": 42,
            },
        },
        "listOfDicts": [{"listSnakeCase": "item1"}, {"anotherListKey": "item2"}],
        "mixedList": ["simpleString", {"nestedSnake": "nestedValue"}, 3.14],
        "alreadyCamelCase": "unchangedValue",
        "noUnderscoreKey": "noChange",
        "emptyStringKey": "",
    }

    assert _map_snake_to_camel_case(input_data) == expected_output


@pytest.mark.parametrize(
    "camel_str, expected",
    [
        ("camelCase", "camel_case"),
        ("thisIsATest", "this_is_a_test"),
        ("already_snake_case", "already_snake_case"),
        ("HTTPRequest", "http_request"),
        ("parseJSONResponse", "parse_json_response"),
        ("XMLHttpRequest", "xml_http_request"),
    ],
)
def test_camel_to_snake(camel_str, expected):
    assert camel_to_snake(camel_str) == expected


def test_map_camel_to_snake_case():
    input_data = {
        "camelCaseKey": "value",
        "nestedDict": {
            "anotherCamelCase": 123,
            "deepNestedDict": {
                "yetAnotherKey": "deepValue",
                "some_snake_case_key": "someOtherValue",
                "NormalNumber": 42,
            },
        },
        "listOfDicts": [{"listCamelCase": "item1"}, {"anotherListKey": "item2"}],
        "mixedList": ["simpleString", {"nestedCamel": "nestedValue"}, 3.14],
        "AlreadySnakeCase": "unchangedValue",
        "NoUnderscoreKey": "noChange",
        "EmptyStringKey": "",
    }

    expected_output = {
        "camel_case_key": "value",
        "nested_dict": {
            "another_camel_case": 123,
            "deep_nested_dict": {
                "yet_another_key": "deepValue",
                "some_snake_case_key": "someOtherValue",
                "normal_number": 42,
            },
        },
        "list_of_dicts": [{"list_camel_case": "item1"}, {"another_list_key": "item2"}],
        "mixed_list": ["simpleString", {"nested_camel": "nestedValue"}, 3.14],
        "already_snake_case": "unchangedValue",
        "no_underscore_key": "noChange",
        "empty_string_key": "",
    }

    assert _map_camel_to_snake_case(input_data) == expected_output
