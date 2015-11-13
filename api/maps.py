import setting

from oauth2client.client import flow_from_clientsecrets as FFC

def init():
    flow = FFC(setting.path.api_key, scope='https://www.googleapis.com/auth/calendar', redirect_uri='http://example.com/auth_return')

    auth_uri = flow.step1_get_authorize_url()
    credentials = flow.step2_exchange(auth_uri)
    print(auth_uri)
