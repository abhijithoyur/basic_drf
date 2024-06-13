from rest_framework import serializers
from home.models import *
from django.contrib.auth.models import User

class TeamSerializers(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('team_name',)

class PersonSerializers(serializers.ModelSerializer):
    team = TeamSerializers()
    class Meta:
        model = Person
        fields = '__all__'
        depth = 1 # It will show all fields of a model in JSON Response.

    #serializer validations
    def validate(self, data):
        special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError("Name should not have any special characters")
        if data['age'] < 18 :
            raise serializers.ValidationError("Age should be greater than 18")
        if data['location'] == 'TVM':
            raise serializers.ValidationError("Location cannot be Trivandrum")
        return data

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        if data['username']:
            if User.objects.filter(username= data['username']).exists():
                raise serializers.ValidationError("Username already exists")
        
        if data['email']:
            if User.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError("Email already exists")
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    