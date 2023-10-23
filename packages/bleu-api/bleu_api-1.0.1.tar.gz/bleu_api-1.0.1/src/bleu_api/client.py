import requests
import datetime


class BleuAPIClient:

    BASE_URL = "https://sdk.faceki.com"

    API_ENDPOINTS = {
        'get_token': 'auth/api/access-token',
        'single_kyc_verification': 'kycverify/api/kycverify/kyc-verification',
        'multiple_kyc_verification': 'kycverify/api/kycverify/multi-kyc-verification',
        'face_match_verification': 'facelink/api/face-check',
        'generate_kyc_link': 'kycverify/api/kycverify/kyc-verify-link',
        'kyc_records_by_link': 'kycverify/api/kycverify/link',
        'kyc_records_by_request_id': 'kycverify/api/kycverify/records',
        'kyc_records_by_reference': 'kycverify/api/kycverify/reference'
    }

    RESPONSE_CODES = {
        "SUCCESS": 0,
        "INTERNAL_SYSTEM_ERROR": 1000,
        "NO_RULES_FOR_COMPANY": 7001,
        "NEED_REQUIRED_IMAGES": 8001,
        "DOCUMENT_VERIFY_FAILED": 8002,
        "PLEASE_TRY_AGAIN": 8003,
        "FACE_CROPPED": 8004,
        "FACE_TOO_CLOSED": 8005,
        "FACE_NOT_FOUND": 8006,
        "FACE_CLOSED_TO_BORDER": 8007,
        "FACE_TOO_SMALL": 8008,
        "POOR_LIGHT": 8009,
        "ID_VERIFY_FAIL": 8010,
        "DL_VERIFY_FAIL": 8011,
        "PASSPORT_VERIFY_FAIL": 8012,
        "DATA_NOT_FOUND": 8013,
        "INVALID_VERIFICATION_LINK": 8014,
        "VERIFICATION_LINK_EXPIRED": 8015,
        "FAIL_TO_GENERATE_LINK": 8016,
        "KYC_VERIFICATION_LIMIT_REACHED": 8017,
        "SELFIE_MULTIPLE_FACES": 8018,
        "FACE_BLURR": 8019
    }

    def __init__(self, client_id, client_secret):
        self.base_url = BleuAPIClient.BASE_URL
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = None

    def access_token_expired(self):
        return (not self.access_token) or (self.token_expiry < datetime.current())

    def make_request(self, endpoint, method='GET', params=None, data=None, headers=None, files=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif method == 'POST':
                if files:
                    response = requests.post(url, data=data, files=files, headers=headers)
                else:
                    response = requests.post(url, data=data, headers=headers)
            # Add support for other HTTP methods as needed

            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            return response.json() if 'application/json' in response.headers.get('content-type',
                                                                                 '').lower() else response.text
        except requests.exceptions.RequestException as e:
            # Handle request errors here
            print(f"Request error: {e}")
            return None

    def get_access_token(self):
        endpoint = self.__class__.API_ENDPOINTS['get_token']
        params = {'clientId': self.client_id, 'clientSecret': self.client_secret}
        response = self.make_request(endpoint=endpoint, method='GET', params=params)

        if response['responseCode'] == self.__class__.RESPONSE_CODES["SUCCESS"]:
            self.access_token = response['data']['access_token']
            self.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=response['data']['expires_in'])
        return self.access_token

    def single_kyc_verification(self, selfie_image_path, doc_front_path, doc_back_path):
        endpoint = self.__class__.API_ENDPOINTS['single_kyc_verification']

        if self.access_token_expired():
            self.get_access_token()

        headers = {
            'Authorization': "Bearer %s" % self.access_token
        }

        files = [
            ('selfie_image', (selfie_image_path.split('/')[-1], open(selfie_image_path, 'rb'), 'image/jpeg')),
            ('doc_front_image',
             (doc_front_path.split('/')[-1], open(doc_front_path, 'rb'), 'image/jpeg')),
            ('doc_back_image',
             (doc_back_path.split('/')[-1], open(doc_back_path, 'rb'), 'image/jpeg'))
        ]
        response = self.make_request(endpoint=endpoint, method='POST', params={}, data={}, headers=headers, files=files)
        return response

    def multiple_kyc_verification(self, selfie_image_path, id_front_path, id_back_path, dl_front_path=None,
                                  dl_back_path=None,  pp_front_path=None, pp_back_path=None):
        endpoint = self.__class__.API_ENDPOINTS['multiple_kyc_verification']

        if self.access_token_expired():
            self.get_access_token()

        headers = {
            'Authorization': "Bearer %s" % self.access_token
        }

        files = [
            ('selfie_image', (selfie_image_path.split('/')[-1], open(selfie_image_path, 'rb'), 'image/jpeg')),
            ('id_front_image', (id_front_path.split('/')[-1], open(id_front_path, 'rb'), 'image/jpeg')),
            ('id_back_image', (id_back_path.split('/')[-1], open(id_front_path, 'rb'), 'image/jpeg'))
        ]
        if dl_front_path and dl_back_path:
            files.extend([
                ('dl_front_image', (dl_front_path.split('/')[-1], open(dl_front_path, 'rb'), 'image/jpeg')),
                ('dl_back_image', (dl_back_path.split('/')[-1], open(dl_front_path, 'rb'), 'image/jpeg'))
            ])
        if pp_front_path and pp_back_path:
            files.extend([
                ('pp_front_image', (pp_front_path.split('/')[-1], open(pp_front_path, 'rb'), 'image/jpeg')),
                ('pp_back_image', (pp_back_path.split('/')[-1], open(pp_front_path, 'rb'), 'image/jpeg'))
            ])

        response = self.make_request(endpoint=endpoint, method='POST', params={}, data={}, headers=headers, files=files)
        return response

    def face_match_verification(self, selfie_image_path):
        endpoint = self.__class__.API_ENDPOINTS['face_match_verification']

        if self.access_token_expired():
            self.get_access_token()

        headers = {
            'Authorization': "Bearer %s" % self.access_token
        }

        files = [
            ('selfie_image', (selfie_image_path.split('/')[-1], open(selfie_image_path, 'rb'), 'image/jpeg'))
        ]
        response = self.make_request(endpoint=endpoint, method='POST', params={}, data={}, headers=headers, files=files)
        return response

    def generate_kyc_link(self):
        endpoint = self.__class__.API_ENDPOINTS['generate_kyc_link']

        if self.access_token_expired():
            self.get_access_token()

        headers = {
            'Authorization': "Bearer %s" % self.access_token
        }

        response = self.make_request(endpoint=endpoint, method='POST', params={}, data={}, headers=headers, files=None)
        return response

    def kyc_records_by_link(self, link):
        endpoint = self.__class__.API_ENDPOINTS['kyc_records_by_link']

        if self.access_token_expired():
            self.get_access_token()

        headers = {
            'Authorization': "Bearer %s" % self.access_token
        }

        params = {'linkId': link}
        response = self.make_request(endpoint=endpoint, method='GET', params=params, data={}, headers=headers, files=None)
        return response

    def kyc_records_by_request_id(self, request_id):
        endpoint = self.__class__.API_ENDPOINTS['kyc_records_by_request_id']

        if self.access_token_expired():
            self.get_access_token()

        headers = {
            'Authorization': "Bearer %s" % self.access_token
        }

        params = {'requestId': request_id}
        response = self.make_request(endpoint=endpoint, method='GET', params=params, data={}, headers=headers, files=None)
        return response

    def kyc_records_by_request_id(self, reference):
        endpoint = self.__class__.API_ENDPOINTS['kyc_records_by_reference']

        if self.access_token_expired():
            self.get_access_token()

        headers = {
            'Authorization': "Bearer %s" % self.access_token
        }

        params = {'referenceId': reference}
        response = self.make_request(endpoint=endpoint, method='GET', params=params, data={}, headers=headers, files=None)
        return response
