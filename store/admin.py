from django.contrib import admin
from django.db.models import Sum, F
from django.utils.html import format_html
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Product, PurchaseOrder, PurchaseOrderLineItem, Invoice, InvoiceLineItem

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'unit_price')
    search_fields = ('name', 'sku')

class PurchaseOrderLineItemInline(admin.TabularInline):
    model = PurchaseOrderLineItem
    extra = 1

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'order_date', 'status', 'total_cost')
    list_filter = ('status', 'order_date')
    inlines = [PurchaseOrderLineItemInline]

    def total_cost(self, obj):
        total = obj.purchaseorderlineitem_set.annotate(
            line_total=F('quantity') * F('cost')
        ).aggregate(total=Sum('line_total'))['total']
        return total or 0
    total_cost.short_description = 'Total Cost'

class InvoiceLineItemInline(admin.TabularInline):
    model = InvoiceLineItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'invoice_date', 'due_date', 'status', 'total', 'days_overdue_display', 'colored_status', 'print_button')
    list_filter = ('status', 'invoice_date')
    inlines = [InvoiceLineItemInline]
    actions = ['mark_as_paid', 'export_to_excel']
    readonly_fields = ('days_overdue_display', 'print_button')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            total_amount=Sum(F('invoicelineitem__quantity') * F('invoicelineitem__price_each'))
        )

    def total(self, obj):
        return obj.get_total()
    total.short_description = 'Total Amount'

    def days_overdue_display(self, obj):
        days = obj.get_days_overdue()
        if days > 0:
            return format_html(
                '<span style="color: red; font-weight: bold;">{} days</span>',
                days
            )
        return "Not overdue"
    days_overdue_display.short_description = 'Days Overdue'

    def colored_status(self, obj):
        colors = {
            'OVERDUE': 'red',
            'PAID': 'green',
            'UNPAID': 'orange'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'

    def print_button(self, obj):
        if obj.id:
            return mark_safe(f'<a class="button" href="{obj.get_absolute_url()}" target="_blank">Print Invoice</a>')
        return ""
    print_button.short_description = 'Print'

    def export_to_excel(self, request, queryset):
        for invoice in queryset:
            filename = invoice.export_to_excel()
            messages.success(request, f'Successfully exported invoice {invoice.id} to {filename}')
    export_to_excel.short_description = "Export selected invoices to Excel"

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status='PAID')
        self.message_user(request, f'{updated} invoice(s) marked as paid.')
    mark_as_paid.short_description = "Mark selected invoices as paid"
