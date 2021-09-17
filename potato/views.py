import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY

YOUR_DOMAIN = 'http://127.0.0.1:8000'


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
  
class ProductLandingPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)

        context.update({
            "product": Product.objects.get(name="Viazi"),
            
        })
        return context



class CreateCheckoutSessionView(View):
    def post(self, request, *args,**kwargs):

            # product_id = self.kwargs["pk"]
            # product = Product.objects.get(id=product_id)
            product = Product.objects.get(name="Viazi")
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # TODO: replace this with the `price` of the product you want to sell
                        'price': 'price_1JaFM9ImzRzjMCHyQOGMH2SB',
                        'quantity': 1,
                    },
                ],
                payment_method_types=[
                            'card',
                ],

                metadata={
                            "product_id": product.id
                        },

                mode='payment',
                success_url=YOUR_DOMAIN + '/success',
                # success_url=reverse('potato:success'),
                cancel_url=YOUR_DOMAIN + '/cancel',
            )

 

            return redirect(checkout_session.url, code=303)     

@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
   
    event = None
    try:
        event = stripe.Webhook.construct_event(
                    payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
                )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(session)
        # Fulfill the purchase...
        # fulfill_order(session)        

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="tony@test.com"
        )

    # Passed signature verification
    return HttpResponse(status=200)

