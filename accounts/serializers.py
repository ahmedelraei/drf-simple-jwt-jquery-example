from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField()
        
    def create(self, validated_data):
        commercial_num = validated_data['commercial_registration_num']
        password = validated_data['password']
        email=validated_data['email']
        change_pass_url = self.context['request'].build_absolute_uri('/')[:-1] + reverse('change_password')

        user = UserModel.objects.create_user(
            commercial_num=commercial_num,
            password=password,
            email=email
        )

        msg = f'''
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
        fields = ("id", "commercial_registration_num","email","password")


class ChangePasswordSerializer(serializers.Serializer):
    model = UserModel
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class RequestChangePasswordSerializer(serializers.Serializer):
    model = UserModel
    email = serializers.CharField(required=True)