import requests
import light

def checkInternet():
    req = requests.get('http://clients3.google.com/generate_204')
    if req.status_code != 204:
        light.lightWifiBad()
        raise Exception
    else:
        light.lightWifiGood()
        #print("Youve got internet!")