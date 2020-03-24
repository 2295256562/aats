def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义token返回
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        "token": token,
        "id": user.id,
        "username": user.username
    }
