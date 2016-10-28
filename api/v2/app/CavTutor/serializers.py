from . import models
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    # Create and Update method overriding from http://stackoverflow.com/a/27586289
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.password = make_password(password)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.password = make_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = models.User
        fields = ('id', 'username', 'f_name', 'l_name', 'password', 'email')
#        extra_kwargs = {'password': {'write_only': True}, }

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institution
        fields = ('id', 'name', 'abbr', 'address')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ('id', 'institution', 'name', 'abbr', )

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tutor
        fields = ('id', 'user', 'course', 'adv_rate', )

class TuteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tutee
        fields = ('id', 'user', 'course', 'tutor')


class AuthenticatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Authenticator
        fields = ('id', 'token', 'user', 'expiry_date')
