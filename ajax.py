import requests
from pprint import pprint 
from bs4 import BeautifulSoup
arr=[]
for i in range(0,10):
    payload={'start':i*9,' limit':9}
    r=requests.get('http://www.boldsky.com/scripts/cms/index.php?action=dynamic-page&type=show_more_category&category_id=6',data=payload)
    bsBody=BeautifulSoup(r.content,'lxml')
    for j in bsBody.find_all('figure'):
        if j.a:
            arr.append(j.a['href'])

arr.sort()
pprint(arr)
