from rest_framework import viewsets
from io import BytesIO
from .serialayzers import StockSerializer, InventoryItemSerializer, InventoryDocumentSerializer, SupplierSerializer
from ..models import Stock, InventoryItem, InventoryDocument, Supplier
from config.services import create_object_for_user_space
from rest_framework.decorators import action
from openpyxl import Workbook
from django.http import HttpResponse
from rest_framework.response import Response


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all() 
    serializer_class = StockSerializer

    def perform_create(self, serializer):
        create_object_for_user_space(Stock, self.request.user, serializer.validated_data)

    @action(methods=['post' ,'get'], detail=False, url_path='exel-export')
    def exelbuk(self, request, *args, **kwargs,):
        wb = Workbook()
        ws = wb.active
        ws.title = 'остатки склада'

        headers = ['лекарство', 'партия', 'количество', 'цена', 'дата привозки товара', 'дата изготовленя', 'срок одности']

        date_from = request.query_params.get('date_from')
        date_to  = request.query_params.get('date_to')
        ws.append(headers)
        stocks = Stock.objects.select_related('recept').all()

        if date_from and date_to:
            stocks = stocks.filter(delivery_date__range = [date_from, date_to])
        elif date_from:
            stocks = stocks.filter(delivery_date__gte=date_from)
        elif date_to:
            stocks = stocks.filter(delivery_date__lte=date_to)


        for stock in stocks:
            row = [
                stock.recept.name if stock.recept else 'Нет названия',
                stock.bathch_number,
                stock.quantity,
                stock.price,
                stock.delivery_date,
                stock.manufactary_date, 
                stock.expire_date
            ]
            ws.append(row)

        file_stream =BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        response = HttpResponse(
            file_stream.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="stock_report.xlsx"'
    
        return response
           
class InventoryDocumentViewSet(viewsets.ModelViewSet):
    queryset = InventoryDocument.objects.all()
    serializer_class = InventoryDocumentSerializer

    def perform_create(self, serializer):
        create_object_for_user_space(InventoryDocument, self.request.user, serializer.validated_data)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def perform_create(self, serializer):
        create_object_for_user_space(Supplier, self.request.user, serializer.validated_data)

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

 