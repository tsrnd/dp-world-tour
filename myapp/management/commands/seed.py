import logging
from django.core.management.base import BaseCommand, CommandError
from myapp.models.stadiums import Stadium
from myapp.models.teams import Team
from myapp.models.user_teams import UserTeam
from myapp.models.stadium_registers import StadiumRegister
from myapp.models.find_matches import FindMatch
from myapp.models.matches import Match
from django.contrib.auth import get_user_model
logger = logging.getLogger(__name__)
User = get_user_model()

MODE_CLEAR = 'clear'
MODE_REFRESH = 'refresh'
MODE_SUPERUSER = 'superuser'
DEFAULT_RECORD = 10

order_create = ['stadium', 'team', 'user', 'user_team', 'stadium_register', 'find_match', 'match']
reverse_clear = ['match', 'find_match', 'stadium_register', 'user_team', 'user', 'team', 'stadium']

models = {
    'stadium': Stadium,
    'team': Team,
    'user': User,
    'user_team': UserTeam,
    'stadium_register': StadiumRegister,
    'find_match': FindMatch,
    'match': Match,
}

class Command(BaseCommand):
    help = 'Seed data'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")
        parser.add_argument('--model', type=str, help="Model")
        parser.add_argument('--number', type=int, help="Number")


    def handle(self, *args, **options):
        self.stdout.write('Running all seeding scripts...')
        mode = options['mode']
        model = options['model']
        number = options['number']
        if number is None:
            number = DEFAULT_RECORD
        if mode == MODE_CLEAR:
            logger.info("Run seeding with mode: " + MODE_CLEAR)
            clear_data(model)
        elif mode == MODE_SUPERUSER:
            logger.info("Run seeding with mode: " + MODE_SUPERUSER)
            from myapp.seeds import user
            user.create_superuser()
        elif mode == MODE_REFRESH:
            logger.info("Run seeding with mode: " + MODE_REFRESH)
            clear_data(model)
            create_data(model, number)
        else:
            logger.info("This mode is not support, run default mode to insert new data")
            create_data(model, number)
        
        self.stdout.write('Seeding has finished...')

def create_data(model_name=None, record=DEFAULT_RECORD):
    from django_seed import Seed
    seeder = Seed.seeder()
    custom_column = {
        'deleted_at': lambda x: None,
    }
    if model_name is None:
        for model in order_create:
            logger.info("Add model to seeder process: " + model)
            if hasattr(models[model], 'deleted_at'):
                seeder.add_entity(models[model], record, custom_column)
            else:
                seeder.add_entity(models[model], record)
    else:
        logger.info("Add model to seeder process: " + model_name)
        if hasattr(models[model_name], 'deleted_at'):
            seeder.add_entity(models[model_name], record, custom_column)
        else:
            seeder.add_entity(models[model_name], record)
    seeder.execute()
    return None

def clear_data(model_name=None):
    if model_name is None:
        for model in reverse_clear:
            logger.info("Clear data of model: " + model)
            models[model].objects.all().delete()
    else:
        logger.info("Clear data of model: " + model_name)
        models[model_name].objects.all().delete()
