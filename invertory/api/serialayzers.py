from rest_framework import serializers
from ..models import InventoryItem, Stock, Supplier, InventoryDocument
from django.db import transaction

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        read_only_fields = ['space']
       

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'
       

class InventoryDocumentSerializer(serializers.ModelSerializer):
    inventoryItems = InventoryItemSerializer(many=True)
    class Meta:
        model = InventoryDocument
        fields = ('id',  'inventoryItems', 'doc_type', 'supplier', 'number', 'date', 'is_posted')
        read_only_fields = ['space']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        with transaction.atomic():
           document = InventoryDocument.objects.create(**validated_data)

           for item_data in items_data:
               InventoryItem.objects.create(document=document, **item_data)

        return document
    
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['space']