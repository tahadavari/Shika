from customer.models import Customer


class CustomerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            customer = Customer.objects.get(id=request.user.id)
            setattr(request, 'customer', customer)
        response = self.get_response(request)

        return response
