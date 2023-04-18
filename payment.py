import os
import json
import uuid
from django.http import HttpResponseRedirect
import requests
import rest_framework.exceptions as rest_exceptions
from rest_framework.permissions import AllowAny
from patterns import settings
from users.permissions import IsSelf, IsUser
from requests import Response
from shop.models import Order, Cart
from rest_framework.views import APIView
from yookassa import Configuration, Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (WebhookNotificationEventType,
                                          WebhookNotificationFactory)

from shop.models import Product


Configuration.account_id = os.environ.get('YOOKASSA_ID', '214892')
Configuration.secret_key = os.environ.get('YOOKASSA_SECRET', 'test_ujQrb-bkh00VZ_2H_vXpKU07L56K9x8g3m8hLhodx9U')


class YookassaPayment(APIView):

    permission_classes = (AllowAny)

        
    def payment_get(self, request, order_id):
        user = request.user
        product= Product.objects.get(id=order_id)
        idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
        "amount": {
            "value": "2.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "receipt": {
            "customer": {
                "full_name": user.username,
                "email": user.email,
                "phone": user.phone_number},
        },
        "confirmation": {
            "type": "redirect",
            "return_url": settings.FRONTEND_HOST
        },
        "items": [
             {
            "description": "Покупка товара",
            "quantity": "1.00",
            "amount": {
            "value": 300,
            "currency": "RUB"},},
            ]},
        {
             "description": product.name
         }, idempotence_key)
        
    # get confirmation url
        print(payment)
        # return HttpResponseRedirect(payment.confirmation.confirmation_url)

    













    # def payment_get(self, request, order_id):
    #     user = request.user
    #     product= Product.objects.get(id=order_id)


    #     payment = Payment.create({
    #     "amount": {
    #     "value": "2.00",
    #     "currency": "RUB"
    #     },
    #     "payment_method_data": {
    #     "type": "bank_card"
    #     },
    #     "confirmation": {
    #     "type": "redirect",
    #     "return_url": settings.FRONTEND_HOST
    #     },
    #     "description": "Заказ №{id}"
    # }, )
        
    # # get confirmation url
        
    #     return Response({'redirect_url':payment.confirmation.confirmation_url}, status=200)





























        # res = Payment.create(
        #     {"amount": {
        #         "value": 100,
        #         "currency": "RUB"}, 

        #     "confirmation": {
        #         "type": "redirect",
        #         "return_url": settings.FRONTEND_HOST},

        #     "capture": True,
        #         "description": Product.name ,
                
        #     "receipt": {
        #         "customer": {
        #             "email": user.email},

        #     "items":
        #         [  
        #             {
        #                 "description": Product.name,
        #                 "quantity": "100",
        #                 "amount": {
        #                     "value": Product.price,
        #                     "currency": "RUB"}
        #                 }
        #             ]
        #         },
        #     })
        # Order.objects.create(stats=product, 
        #                           user=user,
        #                           payment_id=res.id)                    
        # return Response({'redirect_url':res.confirmation.confirmation_url}, status=200)
        

# class YookassaStatus(APIView):
#     permission_classes = (IsSelf, )

#     def get(self, request, order_id):
#         try:
#             user = request.user
#             product = Order.objects.get(id=order_id)
#             amount = int(product.total_price * 100)
#             description = product.display_sizes()
#             payment = {
#                 "userName": settings.MERCHANT_NAME,
#                 "password": settings.MERCHANT_PASS,
#                 "orderNumber": product.id,
#                 "amount": amount,
#                 "returnUrl": settings.FRONTEND_HOST,
#                 "email": user.email,
#                 "phone": user.phone_number,
#                 "description": description
#             }
#             res = requests.post(f"{'YOOKASSA_ID'}", params=payment)
#             res_url = res.json()
#             url_for_payment = res_url.get('formUrl')
#             error_code = res_url.get('errorMessage')
#             if url_for_payment:
#                 product.url_for_payment=url_for_payment
#                 product.save()
#             elif error_code:
#                 return Response({'result': f"{error_code}"}, status=400)
#             return Response(res.text, status=200)
#         except Exception as e:
#             if hasattr(e, 'messages'):
#                 errors = e.messages
#             else:
#                 errors = e.__repr__()
#             raise rest_exceptions.NotFound(f"{errors}")

    # def status_pay(request):

        # data = request.data
        # subscription = Product.objects.get(payment_id=data['name']['id'])
        # subscription.status = data['event']
        # subscription.is_active = subscription.status == 'orderStatus'
        # subscription.save()



        