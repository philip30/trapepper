import http.client, urllib.parse

class SpeechRecognition:
    def recognize(self, audio_file):
        conn = http.client.HTTPSConnection("api.apigw.smt.docomo.ne.jp")
        params = urllib.parse.urlencode({'v': 'on', 'a': open(audio_file, 'rb').read()})
        headers = {"Content-type": "multipart/form-data; boundary=--------------------------102852708831426\r\n"}
        conn.request("POST", "/amiVoice/v1/recognize?APIKEY=707a6849514d336d636e54316d69776e696170737a775236387574585145444b416c35476f32365754302e", params, headers)
        response = conn.getresponse()
        return (response.status, response.read())

speechRec = SpeechRecognition()
print(speechRec.recognize("./resources/nara.mp3"))
