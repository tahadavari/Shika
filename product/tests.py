from django.test import TestCase

# Create your tests here.
from product.models import Category, Product, Discount, Size


class CategoryModelTest(TestCase):

    # without child
    def test_1_product_count(self):
        cat1 = Category.objects.create(
            name='cat',
        )
        p1 = Product.objects.create(
            category=cat1
        )
        p2 = Product.objects.create(
            category=cat1
        )
        p3 = Product.objects.create(
            category=cat1
        )
        self.assertEqual(cat1.get_product_count(), 3)

    # with child
    def test_2_product_count(self):
        cat1 = Category.objects.create(
            name='cat',
        )
        cat2_sub = Category.objects.create(
            name='sub_cat',
            parent=cat1
        )
        p1 = Product.objects.create(
            category=cat1
        )
        p2 = Product.objects.create(
            category=cat2_sub
        )
        p3 = Product.objects.create(
            category=cat1
        )
        self.assertEqual(cat1.get_product_count(), 2 + 1)
        self.assertEqual(cat2_sub.get_product_count(), 1)


class ProductModelTest(TestCase):

    def test_1_final_price(self):
        d1 = Discount.objects.create(
            type='PR',
            percent=20
        )
        p1 = Product.objects.create(
            discount=d1,
            price=2000
        )
        self.assertEqual(p1.final_price(), 1600)

    def test_2_availability(self):
        p1 = Product.objects.create(
            price=2000
        )
        s1 = Size.objects.create(
            product=p1,
            quantity=5,
            size=41
        )
        s2 = Size.objects.create(
            product=p1,
            quantity=3,
            size=42
        )
        self.assertTrue(p1.availability_product())
        self.assertEqual(p1.availability_product(), 8)