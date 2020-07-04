import json
from flask import request, _request_ctx_stack, abort, session, redirect
from functools import wraps
from jose import jwt
from six.moves import urllib
from urllib.request import urlopen



AUTH0_DOMAIN = 'fsndaltwaim.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'estate'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

# implement get_token_auth_header() method

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


# implement check_permissions(permission, payload) method

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


# implement verify_decode_jwt(token) method
def verify_decode_jwt(token):
    print('jwt')
    # print(f'https://fsndaltwaim.auth0.com/.well-known/jwks.json')
    # link = 'https://fsndaltwaim.auth0.com/.well-known/jwks.json'
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    # print(jsonurl.read())
    print('jwt2')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/',
                options={'verify_exp':False},
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


# implement @requires_auth(permission) decorator method
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            # print(token)
            # payload = verify_decode_jwt(token)
            print('kkkkkk')
            try:
                print('rrrr')
                print(verify_decode_jwt(token))
                
                payload = verify_decode_jwt(token)
                print(payload)
                print('hello')
            except Exception:
                # print(token)
                print(f)
                # print(payload)
                print(permission)
                print('hello')
                raise AuthError({
                    'code':'invalid_token',
                    'description':'Access denied because of invalid token'
                    }, 401)
            # print(payload)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
# def requires_signed_in(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if 'jwt_token' not in session:
#             return redirect('/')
#         return f(*args, **kwargs)
#     return decorated