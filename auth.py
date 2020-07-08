import json
from flask import request, _request_ctx_stack, abort, session, redirect
from functools import wraps
from jose import jwt
from six.moves import urllib
from urllib.request import urlopen
import requests
import sys
import os

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_ALGORITHMS = os.environ['AUTH0_ALGORITHMS']
AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']

# AUTH0_DOMAIN = 'fsndaltwaim.auth0.com'
# AUTH0_ALGORITHMS = ['RS256']
# AUTH0_AUDIENCE = 'estate'
# AUTH0_CLIENT_ID = 'VcpVbf6dzg1v6QGbmdy4eDDjM0CZB2mr'
# AUTH0_CLIENT_SECRET = \
# 'nT9eYe0YXAxemiwpXNbPOyerz5OHgitV3Y3ao0zTiZBHJ8Yax_gIMKrvqQw5-49b'
# AUTH0_CALLBACK_URL = 'https://localhost:5000/login-results'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

# Implement get_token_auth_header() method

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


# Implement check_permissions(permission, payload) method

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


# Implement verify_decode_jwt(token) method
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
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
                algorithms=AUTH0_ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/',
                options={'verify_exp': False},
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
                'description': 'Incorrect claims. \
                    Please, check the audience and issuer.'
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


# Implement @requires_auth(permission) decorator method
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except Exception:
                raise AuthError({
                    'code': 'invalid_token',
                    'description': 'Access denied because of invalid token'
                    }, 401)

            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


def requires_signed_in(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'jwt_token' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated
