import datetime
import json
from typing import Dict
from requests import Session

from Crypto.PublicKey import RSA
import python_jwt as jwt
from oauth2client.service_account import ServiceAccountCredentials

from .Exceptions import raise_detailed_error

class Authentication:
    """ Authentication Service """
    def __init__(self, api_key: str, requests: Session, credentials: ServiceAccountCredentials):
        self.api_key            = api_key
        self.current_user       = None
        self.requests           = requests
        self.credentials        = credentials
        self.requests.headers   = {"content-type": "application/json; charset=UTF-8"}

    def sign_in_with_email_and_password(self, email, password) -> Dict[str, any]:
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(self.api_key)
        JSON    = dict(email = email, password = password, returnSecureToken = True, clientType = 'CLIENT_TYPE_ANDROID')
        #data = json.dumps({"email": email, "password": password, "returnSecureToken": True, 'clientType' : 'CLIENT_TYPE_ANDROID'})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        self.current_user = request_object.json()
        return request_object.json()

    def sign_in_anonymous(self) -> Dict[str, any]:
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(self.api_key)
        JSON    = dict(returnSecureToken = True)
        #data = json.dumps({"returnSecureToken": True})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        self.current_user = request_object.json()
        return request_object.json()

    def create_custom_token(self, uid, additional_claims=None, expiry_minutes=60):
        service_account_email = self.credentials.service_account_email
        private_key = RSA.importKey(self.credentials._private_key_pkcs8_pem)
        JSON    = dict(
            iss = service_account_email,
            sub = service_account_email,
            aud = 'https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit',
            uid = uid
        )
        #payload = {
        #    "iss": service_account_email,
        #    "sub": service_account_email,
        #    "aud": "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit",
        #    "uid": uid
        #}
        if additional_claims:
            JSON.update(claims = additional_claims)
            #payload["claims"] = additional_claims
        exp = datetime.timedelta(minutes=expiry_minutes)
        return jwt.generate_jwt(JSON, private_key, "RS256", exp)

    def sign_in_with_custom_token(self, token) -> Dict[str, any]:
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={0}".format(self.api_key)
        JSON    = dict(returnSecureToken = True, token = token)
        #data = json.dumps({"returnSecureToken": True, "token": token})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        return request_object.json()

    def refresh(self, refresh_token) -> Dict[str, any]:
        URL     = "https://securetoken.googleapis.com/v1/token?key={0}".format(self.api_key)
        JSON    = dict(grantType = 'refresh_token', refreshToken = refresh_token)
        #data = json.dumps({"grantType": "refresh_token", "refreshToken": refresh_token})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        request_object_json = request_object.json()
        # handle weirdly formatted response
        user = {
            "userId": request_object_json["user_id"],
            "idToken": request_object_json["id_token"],
            "refreshToken": request_object_json["refresh_token"]
        }
        return dict(userId = request_object_json.get('user_id'), idToken = request_object_json.get('id_token'), refreshToken = request_object_json.get('refresh_token'))

    def get_account_info(self, id_token) -> Dict[str, any]:
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(self.api_key)
        JSON    = dict(idToken = id_token)
        #data = json.dumps({"idToken": id_token})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        return request_object.json()

    def send_email_verification(self, id_token):
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(self.api_key)
        JSON    = dict(requestType = 'VERIFY_EMAIL', idToken = id_token)
        #data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        return request_object.json()

    def send_password_reset_email(self, email) -> Dict[str, any]:
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(self.api_key)
        JSON    = dict(requestType = 'PASSWORD_RESET', email = email)
        #data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        return request_object.json()

    def verify_password_reset_code(self, reset_code, new_password) -> Dict[str, any]:
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/resetPassword?key={0}".format(self.api_key)
        JSON    = dict(oobCode = reset_code, newPassword = new_password)
        #data = json.dumps({"oobCode": reset_code, "newPassword": new_password})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        return request_object.json()

    def create_user_with_email_and_password(self, email, password) -> Dict[str, any]:
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(self.api_key)
        JSON    = dict(email = email, password = password, returnSecureToken = True, clientType = 'CLIENT_TYPE_ANDROID')
        #data = json.dumps({"email": email, "password": password, "returnSecureToken": True, 'clientType' : 'CLIENT_TYPE_ANDROID'})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        return request_object.json()

    def delete_user_account(self, id_token) -> Dict[str, any]:
        URL     = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key={0}".format(self.api_key)
        JSON    = dict(idToken = id_token)
        #data = json.dumps({"idToken": id_token})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        return request_object.json()
    
    def update_profile(self, id_token, display_name = None, photo_url = None, delete_attribute = None) -> Dict[str, any]:
        """
        https://firebase.google.com/docs/reference/rest/auth#section-update-profile
        """
        URL     = "https://identitytoolkit.googleapis.com/v1/accounts:update?key={0}".format(self.api_key)
        JSON    = dict(idToken = id_token, displayName = display_name, photoURL = photo_url, deleteAttribute = delete_attribute, returnSecureToken = True)
        #data = json.dumps({"idToken": id_token, "displayName": display_name, "photoURL": photo_url, "deleteAttribute": delete_attribute, "returnSecureToken": True})
        request_object = self.requests.post(URL, json=JSON, verify=True)
        raise_detailed_error(request_object)
        return request_object.json()
