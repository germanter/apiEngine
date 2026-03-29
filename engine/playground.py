import httpx as x
url = "https://api.apis.guru/v2/list.json"

# r = x.get(url, timeout = 7.5)

#############################
import json
x = '{ "name":"John", "age":30, "city":"New York"}'
y = json.loads(x)
# print(y["city"])

x1 = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

y1 = json.dumps(x1)
# print(y1)

# print(json.dumps({"name": "John", "age": 30}))
# print(json.dumps(["apple", "bananas"]))
# print(json.dumps(("apple", "bananas")))
# print(json.dumps("hello"))
# print(json.dumps(42))
# print(json.dumps(31.76))
# print(json.dumps(True))
# print(json.dumps(False))
# print(json.dumps(None))

x2 = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

# print(json.dumps(x2, indent = 4))