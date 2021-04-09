from rest_framework import serializers
from rest_framework import fields
from .models import movie_details

class movie_detailsSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = movie_details
        fields = '__all__'