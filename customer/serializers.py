from rest_framework import serializers

# class QuestionSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True, required=False)
#     question_text = serializers.CharField(required=True, allow_null=True)
#     pub_datetime = serializers.DateTimeField(read_only=True, required=False)
#     qtype = serializers.ChoiceField([
#         ('CN', 'Canceled'),
#         ('DL', 'Deleted'),
#         ('CR', 'Created'),
#     ], default='CR')
#     image = serializers.FileField(required=False, default=None, allow_null=True)
#
#     def update(self, instance, validated_data):
#         pass
#
#     def create(self, validated_data):
#         return Question.objects.create(**validated_data)
from customer.models import Address, Customer
from product.models import Product


class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['id']


class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'title', 'state', 'city', 'address', 'postal_code', 'no', 'customer']
        read_only_fields = ['id']


class CustomerDetailSerializer(serializers.ModelSerializer):
    addresses = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Customer
        exclude = ['password']
        read_only_fields = ['id']


class CustomerListSerializer(serializers.ModelSerializer):
    addresses = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'username', 'phone', 'email', 'addresses']
        read_only_fields = ['id']
