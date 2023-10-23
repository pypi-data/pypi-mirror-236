import datetime

from src.RESTModels.resources import try_parse_response_content


def test_try_parse_str_response():
    data = "text"
    expected_type = str

    expected_result = "text"

    assert try_parse_response_content(data, expected_type) == expected_result


def test_try_parse_int_response():
    data1 = "5"
    data2 = 5
    expected_type = int

    expected_result = 5

    assert try_parse_response_content(data1, expected_type) == expected_result
    assert try_parse_response_content(data2, expected_type) == expected_result


def test_try_parse_datetime_response():
    data = "2023-10-22T19:50:29.182993"
    expected_type = datetime.datetime

    expected_result = datetime.datetime.fromisoformat(data)

    assert try_parse_response_content(data, expected_type) == expected_result

# def test_try_parse_tuple_response():
#     data1 = [1, 2]
#     data2 = ["1", "2"]
#     expected_type = tuple[int]
#
#     expected_result = (1, 2)
#
#     assert try_parse_response_content(data1, expected_type) == expected_result
#     assert try_parse_response_content(data2, expected_type) == expected_result
