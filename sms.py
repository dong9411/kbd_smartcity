import boto3
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import json



def StaticMaps(Lat, Lng):
    LatLng = '{},{}'.format(Lat, Lng)
    url = 'https://maps.googleapis.com/maps/api/staticmap?center={LatLng}&markers=label:Fire%7C${LatLng}&zoom=22&size=640x640&key=AIzaSyArR-qtXXWXuHXUuOOdWJrwALRCNKPuA84'.format(
        LatLng=LatLng)
    response = requests.get(url, stream=True)
    print(url, response)
    #plt.imshow(Image.open(response.raw))
    #plt.show()


#StaticMaps(12,23)


def get_address(lat, lng):
    _url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}&language=ko".format(
        lat, lng, "AIzaSyC6HOyrf4Ea2z9gF5j5O-VsTEIs1X8Tbes")
    #    address = requests.get(_url).json()["plus_code"]["compound_code"]
    address = requests.get(_url).json()['results'][0]['formatted_address']
    return address


def loc(APIkey):
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key={}".format(
        APIkey)
    data = {
        "considerIP": True,
        #        "wifiAccessPoints": [{
        #            "macAddress": "10-7B-44-53-B8-70"
        #        }, {
        #            "macAddress": "70-5D-CC-7E-38-99"
        #        }]
    }
    loc_inf = requests.post(url, json.dumps(data))

    return loc_inf.json()


location = loc("AIzaSyC6HOyrf4Ea2z9gF5j5O-VsTEIs1X8Tbes")
geo_address = get_address(location['location']['lat'],
                          location['location']['lng'])
#StaticMaps(37, 126)

client = boto3.client(
    'sns',
    region_name='ap-southeast-1',
    aws_access_key_id='AKIATT37AHORBIXBA66H',
    #aws_secret_access_key=''
    )

response = client.publish(
    #TopicArn='arn:aws:sns:ap-southeast-1:248837585826:DH_phone',
    #TargetArn='string',
    PhoneNumber='+8201035693132',
    Message="{0} [lat:{1}, lng:{2}] fire detected".format(
        geo_address, location['location']['lat'], location['location']['lng']),
    Subject='string',
)
