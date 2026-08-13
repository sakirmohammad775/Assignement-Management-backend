from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
        ]

        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

from academics.models import StudentClass


class AdminStudentSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(
        source="student_class.class_group.name",
        read_only=True,
        default=None,
    )

    class_code = serializers.CharField(
        source="student_class.class_group.code",
        read_only=True,
        default=None,
    )

    class_id = serializers.IntegerField(
        source="student_class.class_group.id",
        read_only=True,
        default=None,
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "class_id",
            "class_name",
            "class_code",
        ]