from django.test import TestCase

# Create your tests here.
from core.models import TestBaseModel, TestUserModel


class BaseModelTest(TestCase):

    def test_1_deleted(self):
        m1 = TestBaseModel.objects.create()
        m1.deleted = True
        m1.save()
        self.assertNotIn(m1, TestBaseModel.objects.all())

    def test_2_archive(self):
        m1 = TestBaseModel.objects.create()
        m1.deleted = True
        m1.save()
        self.assertIn(m1, TestBaseModel.objects.archive())


class UserTestModel(TestCase):

    def test_1_is_superuser(self):
        u1 = TestUserModel.objects.create()
        self.assertFalse(u1.is_superuser)

    def test_2_is_active(self):
        u2 = TestUserModel.objects.create()
        self.assertTrue(u2.is_active)
