from django.db import transaction
from .models import HeaderCheck, CheckItem
from invertory.models import Stock
from django.core.exceptions import ValidationError
import redis
import os
from datetime import datetime

redis_url = os.environ.get('REDIS_URL')

redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

def create_check(space, branch, number_kassa, items):

    current_date_str = datetime.now().strftime('%Y%m%d')

    redis_key = f'check:couter:branch:{branch.id}:date:{current_date_str}'
    next_number = redis_client.incr(redis_key)
    if next_number == 1:
        redis_client.expire(redis_key, 129600)
    
    formatted_number = str(next_number).zfill(4)
    final_check_number = f'CH-{current_date_str} - {formatted_number}'

    with transaction.atomic():
        header_check = HeaderCheck.objects.create(
            space = space,
            branch = branch,
            number = final_check_number,
            number_kassa = number_kassa,
            total_amount = 0 
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

                
                current_price = stock_item.price 
                stock_item.quantity -= quantity
                stock_item.save()

               
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
