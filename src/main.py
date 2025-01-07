

from models.request import get_request


for i in range(30):
    print(get_request('http://www.google.com'))
