from django.contrib import admin
from myapp.models import stadiums, stadium_registers, teams, user_teams, matches, find_matches

admin.register(teams.Team)
admin.register(user_teams.UserTeam)
admin.register(stadiums.Stadium)
admin.register(stadium_registers.StadiumRegister)
admin.register(find_matches.FindMatch)
admin.register(matches.Match)
