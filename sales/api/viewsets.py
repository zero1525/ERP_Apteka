from rest_framework.viewsets import ModelViewSet
from config.services import create_object_for_user_space
from .serialayzers import HeaderCheckSerializer, CheckItemSerializer
from ..models import HeaderCheck, CheckItem
from io import BytesIO
from openpyxl import Workbook
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from recepts.models import Recepts
from recepts.api.serializers import ReceptSerializer
from ..service import get_product_by_barcode
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class ChecItemViewSets(ModelViewSet):
    queryset = CheckItem.objects.all()
    serializer_class = CheckItemSerializer

    def perform_create(self, serializer):
        create_object_for_user_space(CheckItem, self.request.user, serializer.validated_data)


    @action(methods = ['post', 'get'], detail = False, url_path = 'exel-export')
    def exelbuk(self, request, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        ws.title = 'шапка чека'

        headers = ['филиал', 'название товара', 'цена товара', 'общая цена', 'номер кассы', 'дата продажи']
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        ws.append(headers)
        checks = CheckItem.objects.select_related('header_check', 'recept',).all()

        if date_from and date_to:
            checks = checks.filter(header_check__date__range = [date_from, date_to])
                
        elif date_from:
            checks = checks.filter(header_check__date__gte=date_from)
                
        elif date_to:
            checks = checks.filter(header_check__date__lte=date_to)

        
        for check_item in checks:
            row = [
            check_item.header_check.branch.name,
            check_item.header_check.number,
            check_item.header_check.number_kassa,
            check_item.recept.name, 
            check_item.quantity,
            check_item.price,
            check_item.total_price,
            check_item.header_check.date
        ]
   
            ws.append(row)
        file_stream =BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        response = HttpResponse(
            file_stream.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="check_report.xlsx"'
        return response
    
    def find_by_barcode(self, request):
        barcode_str = request.data.get('barcode')
        
        try:
            product = get_product_by_barcode(barcode_str)
            serializer = ReceptSerializer(product, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        except ObjectDoesNotExist:
            return Response(
                {'error': f'Товар со штрихкодом {barcode_str} не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class HeaderCheckViewSets(ModelViewSet):
    queryset = HeaderCheck.objects.all()
    serializer_class = HeaderCheckSerializer

    def perform_create(self, serializer):
        create_object_for_user_space(HeaderCheck, self.request.user, serializer.validated_data)


