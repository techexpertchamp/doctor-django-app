from rest_framework.exceptions import APIException


class UserCredentialWrongError(APIException):
    status_code = 400
    default_detail = "Your email or password was incorrect. Please try again."
    default_code = "user_credential_wrong"
