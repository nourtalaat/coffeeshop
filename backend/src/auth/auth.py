import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-xjvy32fs.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffeeshop'


# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

# Grabs and validates 'Authorization' header in the request
def get_token_auth_header():
    auth = request.headers.get('Authorization')
    if not auth:
        raise AuthError("No authorization header", 401)
    authParts = auth.split()
    if len(authParts) == 2 and authParts[0] == "Bearer":
        return authParts[1]
    raise AuthError("Malformed authorization header", 400)


# Validates permissions in JWT
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError("Token has no 'permissions' key", 400)
    if permission not in payload['permissions']:
        raise AuthError("Token does not include the required permission", 403)
    return True


# Decodes and verifies the JWT
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
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            desc = 'Token expired.'
            raise AuthError({
                'code': 'token_expired',
                'description': desc
            }, 401)

        except jwt.JWTClaimsError:
            desc = 'Incorrect claims. Please, check the audience and issuer.'
            raise AuthError({
                'code': 'invalid_claims',
                'description': desc
            }, 401)
        except Exception:
            desc = 'Unable to parse authentication token.'
            raise AuthError({
                'code': 'invalid_header',
                'description': desc
            }, 400)
    desc = 'Unable to find the appropriate key.'
    raise AuthError({
                'code': 'invalid_header',
                'description': desc
            }, 400)


# Does all the operations required to
# grab, decode, validate and check authorization for a given request
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator
