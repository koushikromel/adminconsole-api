import requests
import inspect
import json
# a = requests.post(url="http://127.0.0.1:8118/absentees", data={"test":"data"})
# a = requests.post(url="http://127.0.0.1:8118/absentees/fordate", json={"date": "2023-05-19", "b":12})

# a = requests.get(url="http://127.0.0.1:8118/inventory")
# print(a.json())

# a = requests.post(url="http://127.0.0.1:8118/inventory/id", json={"id": "ON30A1CH"})
# print(a.json())

# result = a.json()['info']['description']
# print('desc s', result)
# print('asdf',a.__doc__)
# print(f"Absentees list is {result['absentees_list']}")
# print(f"Absentees count is {result['absentees_count']}")

# def add_two_numbers(num1: int, num2: int) -> int:
#     return f"Added sum is {num1+num2}"

# print(add_two_numbers("1","2"))
# response = requests.get('http://localhost:8118/absentees')  # Replace with your endpoint URL

# example_endpoint = inspect.getmembers(response.json(), inspect.isfunction)[0][1]
# docstring = example_endpoint.__doc__

# print(docstring)


a = requests.get(url="http://127.0.0.1:8118/login/sanjeev@onwords.in/san20")
print(a.json())

# a = requests.post(url="http://127.0.0.1:8118/customer/number", json={"number":"1522328535"})
# print(a.json())