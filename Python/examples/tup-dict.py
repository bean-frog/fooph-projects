dict = {
    1: "hello",
    2: "world"
}
result = sorted([(value, key) for key, value in dict.items()], reverse=True)
print(result)