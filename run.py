from flask import Flask, request, redirect
import twilio.twiml
import json, urllib
from urllib import urlencode
import googlemaps
from HTMLParser import HTMLParser 


app = Flask(__name__)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

@app.route("/", methods=['GET', 'POST'])
def hello_message():
    body = request.values.get('Body', None)
    z = body.split()
    #start = "57FairfieldStreet,Rehoboth,Ma,UnitedStates"
    #finish = "555HuntingtonAve,Boston,Ma,UnitedStates"
    start = z[0]
    finish = z[1]
    url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
            ('origin', start),
            ('destination', finish)
 ))
    ur = urllib.urlopen(url)
    result = json.load(ur)
    variable = []
    for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
        j = strip_tags(result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] )
        variable.append(j + ' ')

    str1 = '\n'.join(variable)
        
    resp = twilio.twiml.Response()
    resp.message(str1)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
