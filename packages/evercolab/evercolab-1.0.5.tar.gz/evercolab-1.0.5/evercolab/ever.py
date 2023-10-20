import requests
import inspect

class NapkinAddapter:
    print("Napkin currently works through passing sorce into your function")

class Client:
    def __init__(self, url):
        self.url = url
    def pub(self, path):
        def engine(fun):
            lines = inspect.getsource(fun)
            fun_data = "\n".join(lines.split("\n")[1:])
            print("...Wait...")
            headers = {'Content-Type': 'application/json'}
            r = requests.post(self.url, json={'source': fun_data, 'endpoint': path}, headers=headers)
            print(r.json())
        return engine
 

