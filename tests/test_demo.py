# import unittest
# from unittest.mock import Mock, MagicMock
#
# def setUpModule():
#     mock=Mock(spec=str)
#     mock.__str__=Mock(return_value='hjsdgvc')
#     mock.addAtt="kjs"
#     mock()
#     mock(3,4)
#     mock(key="key", value="value")
#     print(mock, mock.call_args_list, mock.method_calls, isinstance(mock, str))
#     print("create connection!")
#
#
# def tearDownModule():
#     print("destroy connection!")
#
# class TestStringMethods(unittest.TestCase):
#     def setUp(self):
#         print("setting up the test env!")
#
#     # @classmethod
#     # def setUpClass(cls):
#     #     print("set up class for ", cls)
#
#     def test_upper(self):
#         print("hello world")
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
#
#     # @unittest.skip("demonstrating skipping!")
#     # def test_skip(self):
#     #     self.fail("should not happen and be skipped!")
#
#     # def test_is_even(self):
#     #     for i in range(0, 6):
#     #         self.assertEqual(i % 2, 0)
#
# # class TestIsEven(unittest.TestCase):
# #     def test_is_even(self):
# #         for i in range(0, 6):
# #             with self.subTest(i):
# #                 self.assertEqual(i%2, 0)
#
#
# if __name__ == '__main__':
#     unittest.main()
import json

from main import app
from conftest import test_client
import pytest
from unittest.mock import patch


# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

def get_employees(test_client):
    response = test_client.get('/employees')
    return response.json

@patch('flask.testing.FlaskClient.get')
def test_get_employee_by_id(mock_get, test_client):
    print("hello world!")
    mock_get.return_value.status_code = 200
    mock_get.return_value.get_json.return_value = {
        "username": "naman7",
        "age": "21",
        "email": "naman7@gmail.com",
        "date_of_joining": "2024-07-01",
        "password": "1234",
        "confirm_password": "1234"
    }

    # Act: Use the mocked client.get to make a GET request
    # with app.test_client() as client:
    response = test_client.get('/employees')  # This won't actually hit the endpoint

    # Assert: Ensure the mocked response is returned
    assert response.status_code == 200
    assert response.get_json() == {
        "username": "naman7",
        "age": "21",
        "email": "naman7@gmail.com",
        "date_of_joining": "2024-07-01",
        "password": "1234",
        "confirm_password": "1234"
    }

    # Ensure the mock was called with the correct path
    mock_get.assert_called_once_with('/employees')
    print(response.get_json())

def test_get_employees(test_client):
    response=test_client.get('/employees')
    print(response.json)
    assert response.status_code==200


def test_post_employee(test_client):
    print("hello world!")
    response = test_client.post('/employees', json={
        "username": "naman7",
        "age": "21",
        "email": "naman7@gmail.com",
        "date_of_joining": "2024-07-01",
        "password": "1234",
        "confirm_password": "1234"
    })
    print("kjbkjjknmkr", response.json)
    assert response.status_code==201

#
# def test_put_employee(client):
#     response = client.put('/employees', data={
#         "username": "naman7",
#         "age": 21,
#         "email": "naman7@gmail.com",
#         "date_of_joining": "2024-07-01",
#         "password": 1234,
#         "confirm_password": 1234
#     })
#     print("kjbkjjknmkr", response.json)
#     assert response.status_code==200
