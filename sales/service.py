from django.db import transaction
from .models import HeaderCheck, CheckItem
from invertory.models import Stock
from django.core.exceptions import ValidationError

def create_check(space, branch, number, number_kassa, items):
    with transaction.atomic():
        header_check = HeaderCheck.objects.create(
            space=space,
            branch=branch,
            number=number,
            number_kassa=number_kassa,
            total_amount=0 # Инициализируем нулем
        )
        
        total_amount = 0
        
        for item in items:
            recept_id = item['recept_id'] 
            quantity = item['quantity']
            
            try:
                
                stock_item = Stock.objects.select_for_update().get(
                    branch=branch, 
                    recept_id=recept_id
                )
                
                if stock_item.quantity < quantity:
                    raise ValidationError(f"Недостаточно товара {stock_item.recept.name}")

                # 2. Берем цену из базы, а не из запроса!
                current_price = stock_item.price 

                stock_item.quantity -= quantity
                stock_item.save()

                # 3. Создаем позицию
                check_item = CheckItem.objects.create(
                    header_check=header_check,
                    recept=stock_item.recept,
                    quantity=quantity,
                    price=current_price
                   
                )
                
                total_amount += check_item.total_price

            except Stock.DoesNotExist:
                raise ValidationError("Товар отсутствует на складе данного филиала.")
        
        header_check.total_amount = total_amount
        header_check.save()
        
        return header_check
