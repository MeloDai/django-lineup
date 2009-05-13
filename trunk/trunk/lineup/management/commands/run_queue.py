from django.core.management.base import BaseCommand
from lineup.worker import run

class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        run()
		
        