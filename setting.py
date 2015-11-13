import os

class path:
    project = os.path.dirname(os.path.abspath(__file__))
    api_key = project + "/key/client_secret_google.json"
