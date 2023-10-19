from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import json
import time as tym

def samco_login(body):
    while True:
        ###### SAMCO SWAPNA Login ########
        samco=StocknoteAPIPythonBridge()
        login=samco.login(body=body)
        login=json.loads(login)

        if login['status']!='Success':
            print('login unsuccessful, going to retry')
            tym.sleep(10)
        else:
            samco.set_session_token(sessionToken=login['sessionToken'])
            token=login['sessionToken']
            print('login successful')
            break
    return [token,samco]
        ##this will return a user details and generated session token
