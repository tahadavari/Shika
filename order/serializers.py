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
from order.models import Order, OrderItem
from product.models import Product


class OrderDetailSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    address = serializers.StringRelatedField(read_only=True)
    items = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'address', 'items']
        read_only_fields = ['id']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'size', 'quantity', 'total']
        read_only_fields = ['id']
