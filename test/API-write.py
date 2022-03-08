import urllib.request
from urllib.request import urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context # uses unverified to bypass certificate error
# import requests

msg = "Correct"
msg = msg.replace('\n', "%0A")
field_num = 2

write_con=urlopen('https://api.thingspeak.com/update?api_key=LKDF3RROONZUUTAS&field'+field_num+'='+msg)
print("\nYour message has successfully been sent!")




# msg=requests.get("https://thingspeak.com/channels/1461170/field/1")
# msg=msg.json()['feeds'][-1]['field1']
# print("\nThe Message sent was: \n\n"+str(msg))