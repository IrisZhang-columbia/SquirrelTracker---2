import csv

from django.core.management.base import BaseCommand, CommandError
from tracker.models import Sighting


class Command(BaseCommand):
    help = 'EExport the data from the 2018 census file.'

    all_attnames = list(map(lambda x: x.get_attname(), Sighting._meta.fields))

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        try:
            with open(options['file_path'], 'w') as of:
                headers = []
                for field in Sighting._meta.fields:
                    attname = field.get_attname()
                    if attname == 'longitude':
                        headers.append('X')
                    elif attname == 'latitude':
                        headers.append('Y')
                    else:
                        headers.append(' '.join(map(lambda x: x.capitalize(), attname.split('_'))))
                writer = csv.DictWriter(of, headers)
                writer.writeheader()
                for sighting in Sighting.objects.all():
                    d = {}
                    for k, v in sighting.__dict__.items():
                        if k == '_state':
                            continue
                        elif k == 'longitude':
                            d['X'] = v
                        elif k == 'latitude':
                            d['Y'] = v
                        else:
                            d[' '.join(map(lambda x: x.capitalize(), k.split('_')))] = v
                    writer.writerow(d)
            self.stdout.write(self.style.SUCCESS('Successfully export sightings to {}'.format(options['file_path'])))
        except FileNotFoundError:
            self.stderr.write('File not found {}'.format(options['file_path']))
            return
