from django.shortcuts import render, get_object_or_404
from .models import Invoice
from django.template.defaulttags import register

# Create your views here.

@register.filter
def multiply(value, arg):
    return float(value) * float(arg)

def invoice_print(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    context = {
        'invoice': invoice,
        'days_overdue': invoice.get_days_overdue(),
    }
    return render(request, 'store/invoice_print.html', context)
