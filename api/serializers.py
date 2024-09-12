from django.contrib.auth.models import User
from rest_framework import serializers

from api.models.note import Note

class UserSerianizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","password"]
        extra_kwarsd = {"password":{"write_only":True}}
        
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id","title","content","created_at","author"]
        extra_kwargs = {"author":{"read_only":True}}

