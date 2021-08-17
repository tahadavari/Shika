from customer.models import Customer


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            customer = Customer.objects.get(id=request.user.id)
            setattr(request, 'cart', customer.get_pending_order())
        response = self.get_response(request)

        return response
