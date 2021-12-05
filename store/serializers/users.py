from django.utils.functional import empty
from rest_framework import serializers
from ..models import  Address, User
from django.contrib.auth.hashers import make_password,check_password

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.filter(email=email).first()
        if not user:
            errors = {
                'email':["this email id does not exists"]
            }
        elif not check_password(password,user.password):
            errors = {
                "password":["password does not match"]
            }
        else:
            return validated_data
        raise serializers.ValidationError(errors)

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    serializers.ModelSerializer

class LogoutSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class UserRegisterSerializer(serializers.Serializer):
    gender_choices = [
        ('male','Male'),
        ('female','Female')
    ]

    full_name = serializers.CharField(min_length=10,max_length=100)
    email = serializers.EmailField(max_length=100)
    contact_no = serializers.CharField(min_length=10,max_length=15)
    password = serializers.CharField(min_length=8,max_length=100)
    re_password = serializers.CharField(min_length=8,max_length=100)
    gender = serializers.ChoiceField(choices=gender_choices)
    
    def validate(self,validated_data):
        password = validated_data.get('password')
        re_password = validated_data.get('re_password')
        contact_no = validated_data.get('contact_no')
        email = validated_data.get('email')
        gender = validated_data.get('gender')
        if User.objects.filter(email=email).first():
            errors = {
                'email':[f"{email} email id is already exists"]
            }
        elif User.objects.filter(contact_no=contact_no).first():
            errors = {
                'contact_no':[f"this contact number is already exists"]
            }
        elif not contact_no.isdigit():
            errors = {
                'contact_no':['contact number field only numeric values']
            }
        elif password.isdigit():
            errors = {
                "password":["only numeric values are not allowed!!"]
            }
        elif len(password)<8:
            errors = {
                "password":["at least eight charecters are required"]
            }
        elif password != re_password:
            errors = {
                're_password':["both password does not match"]
            }
        elif gender not in ['male','female']:
            errors = {
                'gender':["gender should be male or female"]
            }
        else:
            validated_data['password'] = make_password(validated_data['password'])
            
            return validated_data
        raise serializers.ValidationError(errors)



class MyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','full_name','birth_date','avatar']
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=8,max_length=100)
    re_password = serializers.CharField(min_length=8,max_length=100)

    def validate(self, validated_data):
        
        password = validated_data.get('password')
        re_password = validated_data.get('re_password')
        if password.isdigit():
            errors = {
                'password':["only numeric values are not allowed"]
            }
        elif password != re_password:
            errors = {
                're_password':["both password doesnot match"]
            }
        else:
            validated_data['password'] = make_password(validated_data['password'])
            return validated_data
        raise serializers.ValidationError(errors)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        exclude = ['password','user_permissions','groups']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ['id',"user"]

    

    def create(self,validated_data,user_id=None):
        if user_id:
            address= Address.objects.create({**validated_data,'user':user_id})
            return address
        else:
            return super().create(validated_data)

