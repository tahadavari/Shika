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
from product.models import Product, Category, ProductImage, Brand


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'product_id', 'main']
        read_only_fields = ['id']


class ProductDetailSerializer(serializers.ModelSerializer):
     # main_image = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'view', 'material', 'features',
                  'specialized_features', 'score', 'brand', 'category', 'final_price', 'main_image', 'images']
        read_only_fields = ['id']


class ProductBriefSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField(
        read_only=True, method_name="get_main_image")

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'final_price', 'main_image', 'get_url']
        read_only_fields = ['id']

    def get_main_image(self, obj):
        """ self referral field """
        serializer = ProductImageSerializer(
            instance=obj.images.filter(main=True).first()
        )
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(
        read_only=True, method_name="get_child_categories")

    product_count = serializers.SerializerMethodField(method_name='get_product_count')

    class Meta:
        model = Category
        fields = [
            'name',
            'image',
            'icon',
            'id',
            'product_count',
            'subcategories',
            'get_url'
        ]

    def get_product_count(self, obj):
        product_sub = len(obj.categories.all())
        product_parent = 0
        for i in obj.subcategory.all():
            product_parent += len(i.categories.all())
        return product_sub + product_parent

    def get_child_categories(self, obj):
        serializer = CategorySerializer(
            instance=obj.subcategory.all(),
            many=True
        )
        return serializer.data


class BrandSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField(method_name='get_product_count')

    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'product_count'
        ]
        read_only_fields = ['id']

    def get_product_count(self, obj):
        product = len(obj.brands.all())
        return product


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id', 'size', 'product'
        ]
        read_only_fields = ['id']
