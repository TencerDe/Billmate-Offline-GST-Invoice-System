from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Product, Invoice, InvoiceItem
import json

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