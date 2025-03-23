from django.db import models
from django.db.models import Sum, F

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.sku})"

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]
    
    vendor = models.CharField(max_length=200)
    order_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    products = models.ManyToManyField(Product, through='PurchaseOrderLineItem')

    def __str__(self):
        return f"PO-{self.id} - {self.vendor}"

class PurchaseOrderLineItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]
    
    customer = models.CharField(max_length=200)
    invoice_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    products = models.ManyToManyField(Product, through='InvoiceLineItem')

    def __str__(self):
        return f"INV-{self.id} - {self.customer}"

    def get_total(self):
        return self.invoicelineitem_set.annotate(
            line_total=F('quantity') * F('price_each')
        ).aggregate(
            total=Sum('line_total')
        )['total'] or 0

class InvoiceLineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_each = models.DecimalField(max_digits=10, decimal_places=2)
