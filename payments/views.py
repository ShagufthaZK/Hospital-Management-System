from multiprocessing import context
from django.shortcuts import render, redirect
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from accounts.models import InsuranceClaim

RAZOR_KEY_ID = "rzp_test_ndVWQPFQ1d2N1H"
RAZOR_KEY_SECRET = "XkhQdi3x6IeOuitCK3oZViGh"

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))


def homepage(request):
	currency = 'INR'
	amount = float(request.GET['amount'])*100 # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = RAZOR_KEY_ID
	context['razorpay_amount'] = float(request.GET['amount'])
	context['currency'] = currency
	context['callback_url'] = callback_url

	return render(request, 'payments/payment.html', context=context)

def claim(request):
    if request.method == 'GET':
        return render(request, 'payments/claim_html.html')
    else:
        res = request.POST
        print(res['claim'])
        item = InsuranceClaim(user=1, amount=float(res['claim']))
        item.save()
        return render(request, 'payments/claim_html.html')


@csrf_exempt
def paymenthandler(request):
    # amount = float(request.GET['amount'])*100 # Rs. 200
    print(request.POST.get('razorpay_payment_id', ''))
    print(request.POST.get('razorpay_payment_id'))
    print(request.POST.get('razorpay_signature'))
    payment_id=request.POST.get('razorpay_payment_id', '')
    # amount=amount
    # razorpay_client.payment.capture(payment_id, amount)
    return render(request, 'payments/payment_success.html')


    return HttpResponseBadRequest()
    
	# if request.method == "POST":
	# 	try:
		    
	# 		# get the required parameters from post request.
	# 		payment_id = request.POST.get('razorpay_payment_id', '')
       
	# 		razorpay_order_id = request.POST.get('razorpay_order_id', '')
	# 		signature = request.POST.get('razorpay_signature', '')
	# 		params_dict = {
	# 			'razorpay_order_id': razorpay_order_id,
	# 			'razorpay_payment_id': payment_id,
	# 			'razorpay_signature': signature
	# 		}

	# 		# verify the payment signature.
	# 		result = razorpay_client.utility.verify_payment_signature(
	# 			params_dict)
	# 		if result is not None:
	# 		  # Rs. 200
	# 			try:

	# 				# capture the payemt
	# 				razorpay_client.payment.capture(payment_id, amount)

	# 				# render success page on successful caputre of payment
	# 				return render(request, 'paymentsuccess.html')
	# 			except:

	# 				# if there is an error while capturing payment.
	# 				return render(request, 'paymentfail.html')
	# 		else:

	# 			# if signature verification fails.
	# 			return render(request, 'paymentfail.html')
	# 	except:

	# 		# if we don't find the required parameters in POST data
	# 		return HttpResponseBadRequest()
	# else:
	# # if other than POST request is made.
	# return HttpResponseBadRequest()


def get_insurance(request):
    print(request.POST)
    unclaimed = InsuranceClaim.objects.filter(claimed=False)
    context = {}
    context['unclaimed'] = unclaimed
    return render(request, 'insurance_claim.html', context)


def insurance_claimed(request):
    if request.method == 'GET':
        return redirect('get_insurance')
    else:
        res = request.POST
        unclaimed = InsuranceClaim.objects.get(id=res['claim_id'])
        unclaimed.claimed = True
        unclaimed.save()
        return render(request, 'payments/claim_successful.html')
    