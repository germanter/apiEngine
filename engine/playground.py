import httpx as x
url = "https://www.amazon.com/"

r = x.head(url, timeout = 7,follow_redirects=True)
print(r.status_code)

#############################
# import json
# x = '{ "name":"John", "age":30, "city":"New York"}'
# y = json.loads(x)
# print(y["city"])

# x1 = {
#   "name": "John",
#   "age": 30,
#   "city": "New York"
# }

# y1 = json.dumps(x1)
# # print(y1)

# print(json.dumps({"name": "John", "age": 30}))
# print(json.dumps(["apple", "bananas"]))
# print(json.dumps(("apple", "bananas")))
# print(json.dumps("hello"))
# print(json.dumps(42))
# print(json.dumps(31.76))
# print(json.dumps(True))
# print(json.dumps(False))
# print(json.dumps(None))

# x2 = {
#   "name": "John",
#   "age": 30,
#   "married": True,
#   "divorced": False,
#   "children": ("Ann","Billy"),
#   "pets": None,
#   "cars": [
#     {"model": "BMW 230", "mpg": 27.5},
#     {"model": "Ford Edge", "mpg": 24.1}
#   ]
# }

# # print(json.dumps(x2, indent = 4))

# url = "https://openai.com/docs/"
# cl = url.split("://")[1]
# cl = cl.rstrip("/")
# print(cl)