from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('invoice/<int:pk>/print/', views.invoice_print, name='invoice_print'),
]
