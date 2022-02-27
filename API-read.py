from urllib.request import urlopen
import json
READ_API_KEY = "AALOIQGCNR869UZ5"
CHANNEL_ID = "1662430"

def main():
    conn = urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (CHANNEL_ID,READ_API_KEY))

    response = conn.read()
    http_status_code = conn.getcode()

    if (http_status_code == 200):
        print("HTTP Connection Successfull!")
    else:
        print("HTTP Connection Failed!")

    data=json.loads(response)
    print (data['field1'])
    conn.close()



if __name__ == '__main__':
    main()

