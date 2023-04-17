from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from otp_auth.serializers import RegisterUserSerializer
from otp_auth.user import get_user_by_mobile_number, is_user_active, send_otp_verification_code


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
