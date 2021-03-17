import subprocess
import requests
import json
import time

def ngrok_launcher():
    ngrok = subprocess.Popen(['./ngrok','http','5000'], 
                             stdout=subprocess.PIPE)
    time.sleep(10) # to allow the ngrok to fetch the url from the server
    localhost_url = "http://localhost:4040/api/tunnels" #Url with tunnel details
    tunnel_url = requests.get(localhost_url).text #Get the tunnel information
    j = json.loads(tunnel_url)

    tunnel_url = j['tunnels'][1]['public_url'] #Do the parsing of the get

ngrok_launcher()
