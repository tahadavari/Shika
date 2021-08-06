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
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']
