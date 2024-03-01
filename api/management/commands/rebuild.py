from django.core.management.base import BaseCommand, CommandError
from api.models import Song


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("index")

    def handle(self, *args, **options):
        if options["index"] == "songs":
            indexed, added, from_db = Song.rebuild()
            self.stdout.write(f'Indexed: {indexed} | New: {added} | New from database: {from_db}', self.style.SUCCESS)
        else:
            raise CommandError("Invalid index")