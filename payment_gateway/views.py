from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
from core.models import Booking

def pay(request):
    return render(request, 'payment_gateway/index.html')

# def payment_link_view(request):
#     payment_link_html = """
#         <span>Pay with Yene Pay</span>
#         <a id="yenepayLogo" href="https://yenepay.com/checkout/Home/Process/?ItemName=Ticket&ItemId=&UnitPrice=900&Quantity=1&Process=Express&ExpiresAfter=&DeliveryFee=&HandlingFee=&Tax1=&Tax2=&Discount=&SuccessUrl=&IPNUrl=&MerchantId=33431">
#             <img style="width:100px" src="https://yenepayprod.blob.core.windows.net/images/logo.png">
#         </a>
#         <span> ይግዙ</span>
#     """

#     return render(request, 'payment_gateway/pay.html', {'payment_link_html': payment_link_html})

@csrf_exempt
def ipn(request):
    if request.method == 'POST':
        verification_url = 'https://yenepay.com/api/verify/ipn/'
        verification_payload = {}

        verification_response = requests.post(verification_url, data=verification_payload)
        if verification_response.status_code == 200:
            return HttpResponse(status=200)
    return HttpResponse(status=400)

def success(request):
    verification_url = 'https://yenepay.com/api/verify/pdt/'
    total = request.GET.get('TotalAmount')
    status = request.GET.get('Status') 
    verification_payload = {}
    verification_response = requests.post(verification_url, data=verification_payload)
    # booking = request.session.get('pending_booking', {}).get('booking_id')
    booking_id = request.session.get('pending_booking_id')
    booking = get_object_or_404(Booking, pk=booking_id)
    if verification_response.status_code == 200:
        booking.payment_status = True
        booking.save()
        return redirect('core:scheduled')
    else:
        booking.delete()
    return HttpResponse(status=400)
