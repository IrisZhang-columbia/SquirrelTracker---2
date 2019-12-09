import csv

from django.core.management.base import BaseCommand, CommandError
from tracker.models import Sighting


class Command(BaseCommand):
    help = 'Import the data from the 2018 census file.'

    all_attnames = list(map(lambda x: x.get_attname(), Sighting._meta.fields))

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        try:
            with open(options['file_path']) as f:
                reader = csv.DictReader(f)
                Sighting.objects.all().delete()
                for line in reader:
                    d = {}
                    for k, v in line.items():
                        if k == 'X':
                            d['longitude'] = v
                        elif k == 'Y':
                            d['latitude'] = v
                        elif '_'.join(k.lower().split(' ')) in self.all_attnames:
                            if v.lower() == 'false':
                                v = False
                            elif v.lower() == 'true':
                                v = True
                            d['_'.join(k.lower().split(' '))] = v
                    if Sighting.objects.filter(pk=d['unique_squirrel_id']).exists():
                        self.stderr.write(self.style.WARNING('Duplicated unique_squirrel_id found: {}'.format(
                            d['unique_squirrel_id'])))
                        continue
                    Sighting.objects.create(**d)
            self.stdout.write(self.style.SUCCESS('Successfully import sightings from {}'.format(options['file_path'])))
        except FileNotFoundError:
            self.stderr.write('File not found {}'.format(options['file_path']))
            return
