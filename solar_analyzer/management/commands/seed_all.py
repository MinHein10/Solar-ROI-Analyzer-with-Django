from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run all seeder files in correct order'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('🚀 Starting full database seeding...\n'))

        try:
            call_command('seed_users')
            call_command('seed_regions')
            call_command('seed_appliances')
            call_command('seed_installations')
            call_command('seed_incentives_programs')
            # call_command('seed_inputs')  

            self.stdout.write(self.style.SUCCESS('\n All seeders executed successfully.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Seeder failed: {str(e)}'))
