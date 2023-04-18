from rest_framework import status, authentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from otp_auth.serializers import RegisterUserSerializer, LoginUserSerializer, VerifyOTPSerializer
from otp_auth.user import (
    get_user_by_mobile_number,
    is_user_active,
    send_otp_verification_code,
    get_otp_by_otp_hash,
    is_otp_expired,
    issue_token,
    delete_token,
    delete_otp
)


@api_view(['POST'])
def register_user(request):
    """
    Register a user and send OTP for verification
    """
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user, is_user_exists_bool = get_user_by_mobile_number(
            serializer.validated_data["mobile_number"])
        is_user_active_bool = is_user_active(user)

        if is_user_exists_bool:
            if is_user_active_bool:
                response = {'msg': 'User exists'}
                return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                # update user firstname and lastname
                user.firstname = serializer.validated_data["firstname"]
                user.lastname = serializer.validated_data["lastname"]
                user.save()

                # send otp verification code
                send_otp_verification_code(user)
        else:
            # create a user
            user = serializer.save()

            # send otp verification code
            send_otp_verification_code(user)

        response = {'msg': 'OTP sent'}
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    """
    Login a user and send OTP for verification
    """
    serializer = LoginUserSerializer(data=request.data)
    if serializer.is_valid():
        user, is_user_exists_bool = get_user_by_mobile_number(
            serializer.validated_data["mobile_number"])
        is_user_active_bool = is_user_active(user)

        if (is_user_exists_bool and is_user_active_bool):
            # send otp verification code
            send_otp_verification_code(user)
            response = {'msg': 'OTP send'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'msg': 'User does not exists'}
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    """
    Verify OTP and create token
    """
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        otp_from_request_body = serializer.validated_data["otp"]
        otp, is_otp_exists_bool = get_otp_by_otp_hash(otp_from_request_body)

        response = {'data': {'msg': 'Invalid OTP'},
                    'status': status.HTTP_400_BAD_REQUEST}
        if is_otp_exists_bool:
            is_otp_expired_bool = is_otp_expired(otp)

            if is_otp_expired_bool:
                response['data']['msg'] = 'OTP expired'
            else:
                user = otp.user
                if not user.is_active:
                    user.is_active = True
                    user.save()
                token = issue_token(user)
                
                delete_otp(user)
            
                response = {
                    'data': {
                        "token": token.key,
                        "user_id": user.username,
                        "firstname": user.firstname,
                        "lastname": user.lastname
                    },
                    'status': status.HTTP_200_OK
                }
        return Response(**response)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
def logout_user(request):
    delete_token(request.user)
    return Response(status=status.HTTP_204_NO_CONTENT)
