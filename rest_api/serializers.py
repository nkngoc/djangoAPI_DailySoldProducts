from rest_framework import serializers
from .models import productSold

class rest_api_serializer(serializers.ModelSerializer):
    class Meta:
        model = productSold
        fields = ('id','salesdate', 'pid', 'total_qty')
        # for Django 3.3
        #fields = '__all__'