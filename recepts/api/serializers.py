
from rest_framework.serializers import ModelSerializer
from ..models import Category, Manufacturer, Recepts, Barcode



class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        redonly_fields = ['id']

class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'description', 'country']
        redonly_fields = ['id']

class BarcodeSerializer(ModelSerializer):
    class Meta:
        model = Barcode
        fields = ['code', 'volume', 'unitmeas']




class ReceptSerializer(ModelSerializer):
    barcode = BarcodeSerializer(many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Recepts
        fields = ['name', 'description', 'image', 'is_prescription_required', 'barcode', 'category', 'manufacturer']

    def create(self, validated_data):
        barcodes_data = validated_data.pop('barcode')
        category_data = validated_data.pop('category')
        manufacturer_data = validated_data.pop('manufacturer')

        category_obj = Category.objects.get(id=category_data['id'])
        manufacturer_obj = Manufacturer.objects.get(id=manufacturer_data['id'])

        recept = Recepts.objects.create(
            category=category_obj,
            manufacturer=manufacturer_obj,
            **validated_data
        )

        for b_data in barcodes_data: 
            Barcode.objects.create(recept=recept, **b_data)
            
        return recept