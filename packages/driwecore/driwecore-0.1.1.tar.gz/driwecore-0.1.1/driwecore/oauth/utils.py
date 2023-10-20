import jwt

from .secret import get_token_secret


# Need to change to accept request and attach user oauth id to request.oauth_id


def validateJWTAccessToken(token):
    secret_key_list = get_token_secret()

    audience = 'https://services-vehicle-ibpoflkccq-as.a.run.app/'

    for secret_key in secret_key_list:
        try:
            decoded_payload = jwt.decode(
                token, secret_key, audience=audience, algorithms=['HS256'])

            print(decoded_payload)

            return True

        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return False

        except jwt.InvalidTokenError as e:
            print("Token is invalid, error: ", e)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    return False


def getJWTAccessTokenOauthId(token):

    try:
        # Decode the JWT without validation
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print('decoded_token', decoded_token)
        return decoded_token['user']
    except Exception as e:
        print("Error: ", e)
