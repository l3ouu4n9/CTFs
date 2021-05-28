import hashlib

print(hashlib.sha256(("a"+"b").encode("UTF-8")).hexdigest())

# fb8e20fc2e4c3f248c60c39bd652f3c1347298bb977b8b4d5903b85055620603

# hashlib.sha256((user["password"] + user["salt"]).encode("UTF-8")).hexdigest() == user["hash"]