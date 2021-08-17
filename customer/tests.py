from django.test import TestCase

# Create your tests here.
from customer.models import Customer,Address
from order.models import Order


class CustomerModelTest(TestCase):

    def test_1(self):
        c1 = Customer.objects.create(
            phone='09123456789'
        )
        c1.save()
        self.assertIn(c1, Customer.objects.all())

    def test_2_pending_order(self):
        c1 = Customer.objects.create(
            phone='09123456789'
        )
        o1 = Order.objects.create(
            customer = c1,
            status='PE',
            total_amount=0
        )
        self.assertEqual(o1, c1.get_pending_order())


class AddressModelTest(TestCase):

    def test_1(self):
        c1 = Customer.objects.create(
            phone='09123456789'
        )
        a1 = Address.objects.create(
            customer = c1,

        )
        self.assertIn(a1, Address.objects.all())
