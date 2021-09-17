from django.urls import path
from . import views

app_name = 'potato'

from .views import (
    CreateCheckoutSessionView,
    ProductLandingPageView,
    SuccessView,
    CancelView,
    stripe_webhook,
    )

urlpatterns = [
            
            path('', ProductLandingPageView.as_view(), name='landing-page'),
            path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
            path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
            path('cancel/', CancelView.as_view(), name='cancel'),
            path('success/', SuccessView.as_view(), name='success'),
]