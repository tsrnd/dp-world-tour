from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Seed data'

    def handle(self, *args, **options):
        self.stdout.write('Running all seeding scripts...')
        from myapp.seeds import user
        user.create_superuser()

        from myapp.models.stadiums import Stadium
        from myapp.models.teams import Team
        from myapp.models.user_teams import UserTeam
        from myapp.models.stadium_registers import StadiumRegister
        from myapp.models.find_matches import FindMatch
        from myapp.models.matches import Match
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from django_seed import Seed
        seeder = Seed.seeder()
        seeder.add_entity(Stadium, 100)
        seeder.add_entity(Team, 100)
        seeder.add_entity(User, 100)
        seeder.add_entity(UserTeam, 100)
        seeder.add_entity(StadiumRegister, 100)
        seeder.add_entity(FindMatch, 100)
        seeder.add_entity(Match, 100)
        seeder.execute()
