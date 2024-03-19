from django.core.management.base import BaseCommand, CommandError

from api.index import rebuild


class Command(BaseCommand):
    help = "Rebuilds the specified index for searching"

    def add_arguments(self, parser):
        parser.add_argument("index")

    def handle(self, *args, **options):
        if options["index"] == "songs":
            indexed, added, from_db = rebuild()
            self.stdout.write(f'Indexed: {indexed} | New: {added} | New from database: {from_db}', self.style.SUCCESS)
        else:
            raise CommandError("Invalid index")