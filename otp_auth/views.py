from rest_framework import status, authentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from otp_auth.serializers import (
    RegisterUserSerializer, 
    LoginUserSerializer, 
    VerifyOTPSerializer,
    ValidateMobileNumberSerializer
)
from otp_auth.user import (
    get_user_by_mobile_number,
    is_user_active,
    send_otp_verification_code,
    get_otp_by_otp_hash,
    is_otp_expired,
    issue_token,
    delete_token,
    delete_otp,
    delete_user
)


@api_view(['POST'])
def register_user(request):
    """
    Register a user and send OTP for verification
    """
    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mobile_number = serializer.validated_data["mobile_number"]
    user, is_user_exists_bool = get_user_by_mobile_number(mobile_number)

    if is_user_exists_bool:
        if is_user_active(user):
            response_data = {'msg': 'User already exists and is active'}
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        else:
            # update user firstname and lastname
            user.firstname = serializer.validated_data["firstname"]
            user.lastname = serializer.validated_data["lastname"]
            user.save()
    else:
        # create a user
        user = serializer.save()

    # send OTP verification code
    send_otp_verification_code(user)

    response_data = {'msg': 'OTP sent'}
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    """
    Login a user and send OTP for verification
    """
    serializer = LoginUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mobile_number = serializer.validated_data["mobile_number"]
    user, is_user_exists_bool = get_user_by_mobile_number(mobile_number)

    if not is_user_exists_bool:
        return Response({'msg': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

    if not is_user_active(user):
        return Response({'msg': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)

    # send OTP verification code
    send_otp_verification_code(user)
    response_data = {'msg': 'OTP sent'}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_otp(request):
    """
    Verify OTP and create token
    """
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    otp_from_request_body = serializer.validated_data["otp"]
    otp, is_otp_exists_bool = get_otp_by_otp_hash(otp_from_request_body)

    if not is_otp_exists_bool:
        return Response({'data': {'msg': 'Invalid OTP'}, 'status': status.HTTP_400_BAD_REQUEST})

    if is_otp_expired(otp):
        return Response({'data': {'msg': 'OTP expired'}, 'status': status.HTTP_400_BAD_REQUEST})

    user = otp.user
    if not user.is_active:
        user.is_active = True
        user.save()

    token = issue_token(user)
    delete_otp(user)

    response_data = {
        'data': {
            "token": token.key,
            "user_id": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname
        },
        'status': status.HTTP_200_OK
    }
    return Response(**response_data)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
def logout_user(request):
    delete_token(request.user)
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def validate_mobile_number(request):
    serializer = ValidateMobileNumberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mobile_number = serializer.validated_data["mobile_number"]
    _, is_user_exists_bool = get_user_by_mobile_number(mobile_number)
    response_data = {'is_valid_mobile_number': is_user_exists_bool}
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
def delete_user_account(request):
    delete_user(request.user)
    return Response(status=status.HTTP_204_NO_CONTENT)