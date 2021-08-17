from django.core.management.base import BaseCommand, CommandError
from argparse import ArgumentParser

from customer.models import Customer


class Command(BaseCommand):

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('username', metavar='USERNAME',
                            help="username of user")

    def handle(self, *args, **options):
        username = options['username']

        try:
            customer = Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            raise CommandError(f'username "{username}" does not exist')

        customer.is_active = False
        customer.save()
        print('user deactivate')
