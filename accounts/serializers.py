from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import get_tokens_for_user

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    ''' Serializing User Instance '''
        
    def create(self, validated_data):
        commercial_num = validated_data['commercial_registration_num']
        password = UserModel.objects.make_random_password()
        email=validated_data['email']

        user = UserModel.objects.create_user(
            commercial_num=commercial_num,
            password=password,
            email=email
        )

        tokens = get_tokens_for_user(user)
        change_pass_url = (self.context['request'].build_absolute_uri('/')[:-1] 
                    + reverse('change_password') + '?access=' + tokens['access'])

        msg = f'''
        Welcome!\n
        Commercial Number: {commercial_num}\n
        Password: {password}\n
        Change password => {change_pass_url}
        '''
        try:
            send_mail(
                'Login Info',
                msg,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
        except Exception as e:
            print(e)


        return user

    class Meta:
        model = UserModel
        fields = ("id", "commercial_registration_num","email")


class ChangePasswordSerializer(serializers.Serializer):
    ''' Serializing old & new passwords '''
    model = UserModel
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class RequestChangePasswordSerializer(serializers.Serializer):
    ''' Serializing User Email '''
    model = UserModel
    email = serializers.CharField(required=True)
    
class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        response = super().validate(attrs)
        refresh = self.get_token(self.user)
        response['refresh'] = str(refresh)
        response['access'] = str(refresh.access_token)
        response['commercial_registration_num'] = self.user.commercial_registration_num
        response['email'] = self.user.email
        return response