from django.test import TestCase

# Create your tests here.
from customer.models import Address, Customer
from order.models import Order, OrderItem
from product.models import Product


class OrderModelTest(TestCase):
    def test1(self):
        c1 = Customer.objects.create()
        a1 = Address.objects.create(
            customer=c1
        )
        p1 = Product.objects.create()
        o1 = Order.objects.create(
            customer=c1,
            status='CO',
            total_amount=0
        )
        oi1 = OrderItem.objects.create(
            order=o1,
            product=p1,
            quantity=2,
            total=2000
        )
        o1.save()
        self.assertIn(oi1, o1.items.all())


# class OrderItem(TestCase):
#     p1 = Product.objects.create()
#     o1 = Order.objects.create(
#         customer=c1,
#         status='CO',
#         total_amount=0
#     )
#     oi1 = OrderItem.objects.create(
#         order=o1,
#         product=p1,
#         quantity=2,
#         total=2000
#     )
#     oi1.save()

