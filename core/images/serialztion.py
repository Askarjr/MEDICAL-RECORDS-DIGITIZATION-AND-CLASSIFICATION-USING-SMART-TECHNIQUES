from unicodedata import category
from rest_framework import serializers
from .models import Item

class ImagesofItem(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields='__all__'

