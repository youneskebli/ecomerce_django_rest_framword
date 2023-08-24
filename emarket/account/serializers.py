from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],min_length=8)
    class Meta:
        model= User
        fields= ('first_name','last_name','email','password')

        extra_kwargs= {
            'first_name':{'required':True,'allow_blank':False},
            'last_name':{'required':True,'allow_blank':False}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'username')

