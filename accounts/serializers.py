from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        print(type(validated_data['commercial_registration_num']))
        user = UserModel.objects.create_user(
            commercial_num=validated_data['commercial_registration_num'],
            password=validated_data['password'],
            email=validated_data['email']
        )

        return user

    class Meta:
        model = UserModel
        fields = ("id", "commercial_registration_num", "password","email")


class ChangePasswordSerializer(serializers.Serializer):
    model = UserModel
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)