def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserJWTSerializer(user, context={'request': request}).data
    }
