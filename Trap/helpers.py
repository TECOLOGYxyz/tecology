import requests
import light

def checkInternet():
    req = requests.get('http://clients3.google.com/generate_204')
    if req.status_code != 204:
        light.lightWifiBad()
        return False
        #raise Exception
    else:
        light.lightWifiGood()
        return True
        #print("Youve got internet!")