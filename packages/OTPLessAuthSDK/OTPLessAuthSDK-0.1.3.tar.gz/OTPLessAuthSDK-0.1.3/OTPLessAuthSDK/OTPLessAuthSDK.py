import requests
import json
import jwt
import rsa
from Constants import OTPLESS_KEY_API
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class UserDetail:
    
    @staticmethod
    def decode_id_token(id_token, client_id, client_secret, audience=None):
        try:
            oidc_config = get_config()
            public_key = get_public_key(oidc_config['jwks_uri'])
            decoded = decode_jwt(id_token, public_key['n'], public_key['e'], oidc_config['issuer'], audience)

            # Construct the user_detail dictionary from the decoded JWT            
            user_detail = {
                'success': True,
                # 'iss': decoded['iss'],
                # 'sub': decoded['sub'],
                # 'aud': decoded['aud'],
                # 'exp': decoded['exp'] * 1000,
                # 'iat': decoded['iat'] * 1000,
                'auth_time': int(decoded['auth_time']),
                'phone_number': decoded['phone_number'],
                'email': decoded['email'],
                'name': decoded['name'],
                'country_code': decoded['country_code'],
                'national_phone_number': decoded['national_phone_number']
            }            
            # auth_details = json.loads(str(decoded['authentication_details']).replace('\\', "").strip('"'))
            # user_detail['authentication_details'] = auth_details

            return user_detail
        except Exception as error:            
            raise Exception(f"Something went wrong, please try again. Error: {error}")

    @staticmethod
    def verify_code(code, client_id, client_secret, audience=None):
        try:
            oidc_config = get_config()
            form_data = {
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
            }
            response = requests.post(oidc_config['token_endpoint'], data=form_data)
            
            if response.status_code == 200:
                return UserDetail.decode_id_token(response.json()['id_token'], client_id, client_secret, client_id)
            else:
                raise Exception(f"Request failed with status code {response.status_code}, message: {response.json()['message']}, full response: {response.text}")
        except Exception as error:            
            raise Exception(f"Something went wrong, please try again. Error: {error}")


def decode_jwt(jwt_token, modulus, exponent, issuer, audience=None):
    public_key = create_rsa_public_key(modulus, exponent)
    verify_options = {
        'algorithms': ['RS256'],
        'issuer': issuer,
    }    
    if audience:
        verify_options['audience'] = audience
    
    try:
        decoded = jwt.decode(jwt_token, public_key, **verify_options)
        return decoded
    except jwt.InvalidAudienceError:
        raise Exception("Invalid audience")
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except Exception as error:
        raise Exception(f'JWT verification failed: {str(error)}')


def create_rsa_public_key(modulus_b64, exponent_b64):
    try:
        modulus_bytes = base64.urlsafe_b64decode(modulus_b64 + '=' * (4 - len(modulus_b64) % 4))
        exponent_bytes = base64.urlsafe_b64decode(exponent_b64 + '=' * (4 - len(exponent_b64) % 4))
    except Exception as e:
        raise Exception(f"Error during base64 decoding: {str(e)}")
    
    try:
        modulus = int.from_bytes(modulus_bytes, byteorder="big")
        exponent = int.from_bytes(exponent_bytes, byteorder="big")
    except Exception as e:
        raise Exception(f"Error during byte conversion: {str(e)}")

    try:
        public_numbers = rsa.RSAPublicNumbers(exponent, modulus)
        public_key = public_numbers.public_key(backend=default_backend())
    except Exception as e:
        raise Exception(f"Error during public key creation: {str(e)}")

    try:
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    except Exception as e:
        raise Exception(f"Error during PEM serialization: {str(e)}")

    try:
        return serialization.load_pem_public_key(pem, backend=default_backend())
    except Exception as e:
        raise Exception(f"Error during PEM public key loading: {str(e)}")


def get_config():
    response = requests.get(OTPLESS_KEY_API, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    if response.json():
        return response.json()
    raise Exception('Unable to fetch OIDC config')


def get_public_key(url):
    response = requests.get(url, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    if response.json() and 'keys' in response.json() and response.json()['keys'][0]:
        return response.json()['keys'][0]
    raise Exception('Unable to fetch public key')
