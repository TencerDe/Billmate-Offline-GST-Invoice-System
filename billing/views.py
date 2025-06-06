from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Product, Invoice, InvoiceItem
import json
from reportlab.pdfgen import canvas
from io import BytesIO

@csrf_exempt
def add_customer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            required_fields = ['name', 'phone', 'address']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)

            customer = Customer.objects.create(
                name=data['name'],
                email=data.get('email', ''),
                phone=data['phone'],
                address=data['address'],
                gstin=data.get('gstin', '')
            )
            return JsonResponse({'message': 'Customer added', 'id': customer.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed. Use POST.'}, status=405)

@csrf_exempt
def delete_customer(request, customer_id):
    if request.method == 'DELETE':
        try:
            customer = Customer.objects.filter(id=customer_id)
            if not customer.exists():
                return JsonResponse({'error': 'Customer not found'}, status=404)
            customer.delete()
            return JsonResponse({'message': 'Customer deleted'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed. Use DELETE.'}, status=405)

def get_customers(request):
    customers = list(Customer.objects.values())
    return JsonResponse(customers, safe=False)

def get_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'gstin': customer.gstin,
        }
        return JsonResponse(data)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            required_fields = ['name', 'hsn_code', 'price', 'gst_rate']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)

            product = Product.objects.create(
                name=data['name'],
                description=data.get('description', ''),
                hsn_code=data['hsn_code'],
                price=data['price'],
                gst_rate=data['gst_rate']
            )
            return JsonResponse({'message': 'Product added', 'id': product.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed. Use POST.'}, status=405)

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = Product.objects.filter(id=product_id)
            if not product.exists():
                return JsonResponse({'error': 'Product not found'}, status=404)
            product.delete()
            return JsonResponse({'message': 'Product deleted'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed. Use DELETE.'}, status=405)

def get_products(request):
    if request.method == 'GET':
        products = Product.objects.all().values('id','name','description','hsn_code','price','gst_rate')
        return JsonResponse(list(products), safe=False)

@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            required_fields = ['customer_id', 'invoice_number', 'items']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)

            invoice = Invoice.objects.create(
                customer_id=data['customer_id'],
                invoice_number=data['invoice_number'],
                total_amount=0,
                total_tax=0
            )

            total_amount = 0
            total_tax = 0

            for item in data['items']:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                rate = product.price
                tax_percent = product.gst_rate

                subtotal = rate * quantity
                tax = (subtotal * tax_percent) / 100
                total = subtotal + tax

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity,
                    rate=rate,
                    tax_percent=tax_percent,
                    total=total
                )

                total_amount += subtotal
                total_tax += tax

            invoice.total_amount = total_amount + total_tax
            invoice.total_tax = total_tax
            invoice.save()

            return JsonResponse({'message': 'Invoice created', 'id': invoice.id}, status=201)

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed. Use POST.'}, status=405)

@csrf_exempt
def get_all_invoices(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all().order_by('-created_at')
        data = []

        for invoices in invoices:
            items = InvoiceItem.objects.filter(invoice=Invoice)
            item_list = []

            for item in items:
                item_list.append({
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'rate': item.rate,
                    'tax_percent': item.tax_percent,
                    'total': item.total,
                })

            data.append({
                'invoice_id': Invoice.id,
                'invoice_number': Invoice.invoice_number,
                'customer_name': Invoice.customer.name,
                'created_at': Invoice.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'total_amount': Invoice.total_amount,
                'total_tax': Invoice.total_tax,
                'items': item_list
            })

        return JsonResponse({'invoices': data})

def download_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        items = InvoiceItem.objects.filter(invoice=invoice)

        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, 800, f"Invoice #{invoice.invoice_number}")

        # Customer Info
        p.setFont("Helvetica", 12)
        p.drawString(50, 770, f"Customer: {invoice.customer.name}")
        p.drawString(50, 750, f"Phone: {invoice.customer.phone}")
        p.drawString(50, 730, f"Email: {invoice.customer.email or 'N/A'}")
        p.drawString(50, 710, f"Address: {invoice.customer.address}")

        # Items Header
        y = 680
        p.drawString(50, y, "Product")
        p.drawString(200, y, "Qty")
        p.drawString(250, y, "Rate")
        p.drawString(320, y, "Tax%")
        p.drawString(390, y, "Total")

        y -= 20

        for item in items:
            p.drawString(50, y, item.product.name)
            p.drawString(200, y, str(item.quantity))
            p.drawString(250, y, f"{item.rate:.2f}")
            p.drawString(320, y, f"{item.tax_percent:.2f}")
            p.drawString(390, y, f"{item.total:.2f}")
            y -= 20

        # Totals
        p.drawString(50, y - 10, f"Total Tax: ₹{invoice.total_tax:.2f}")
        p.drawString(50, y - 30, f"Total Amount: ₹{invoice.total_amount:.2f}")

        # Finalize
        p.showPage()
        p.save()
        buffer.seek(0)

        return HttpResponse(buffer, content_type='application/pdf')

    except Invoice.DoesNotExist:
        return JsonResponse({'error': 'Invoice not found'}, status=404)

