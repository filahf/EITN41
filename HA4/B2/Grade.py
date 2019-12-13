import requests
import numpy as np
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import operator 

def send_req(bundled_url):
    resp = requests.get(bundled_url,verify=False)
    time = resp.elapsed.total_seconds()
    if(resp.text.strip() == "1"):

        print("Correct", bundled_url[bundled_url.find("signature"):])
    return time


def find_signature(name,grade, iterations):
    base_url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name={}&grade={}&signature=".format(name,grade)
    rec_time = [0] * 16
    characters = "0123456789abcdef"
    for i in range(iterations):
        for char in characters:
            print(base_url + char)
            rec_time[characters.find(char)] = send_req(base_url + char)
        base_url += characters[np.argmax(rec_time)]

    return base_url


signature = find_signature("Kalle",5,20)
send_req(signature)