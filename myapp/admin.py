from django.contrib import admin
from myapp.models import stadiums, stadium_registers, teams, user_teams, matches, find_matches, cronjob
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.conf.urls import url
from django.http import HttpResponseRedirect
import time
from django.contrib.auth import get_permission_codename
from threading import Thread
import os
from .forms import CronjobForm
admin.register(teams.Team)
admin.register(user_teams.UserTeam)
admin.register(stadiums.Stadium)
admin.register(stadium_registers.StadiumRegister)
admin.register(find_matches.FindMatch)
admin.register(matches.Match)

def call_docker_cron_cmd(sub_cmd, job_identifier):
    cmd = f'docker exec -i dp-world-tour_cronjob_1 python manage.py cus_crontab {sub_cmd} {job_identifier} --settings=myproject.settings_cronjob'
    os.system(cmd)

class CronjobAdmin(admin.ModelAdmin):
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('job_schedule', 'job_path', 'job_name'),
    }), )
    
    search_fields = ('job_path', 'job_name')
    model = cronjob.CronjobModel
    list_display = ['id', 'job_hash', 'job_schedule', 'job_path', 'cronjob_actions', 'deleted_at']
    readonly_fields = ['job_path_view', 'job_schedule_view']
    form = CronjobForm

    def job_schedule_view(self, obj):
        return format_html(
            '{}<a style="color:blue;padding-left:10px;font-size:smaller;">(You can edit this field if job have already removed from crontab)</a>', obj.job_schedule
        )
    
    def job_path_view(self, obj):
        return format_html(
            '{}<a style="color:blue;padding-left:10px;font-size:smaller;">(You can edit this field if job have already removed from crontab)</a>', obj.job_path
        )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        detail_schedule = obj.job_schedule.replace(' ', '_')
        if obj.job_hash:
            return (
                (None, {
                    'fields': ('job_name', 'job_hash')
                }),
                (_('Job Detail'), {
                    'fields': ('job_schedule_view', 'job_path_view', 'status'),
                    'description': f'<div class="help">See detail job schedule in <a href = "https://crontab.guru/#{detail_schedule}"> https://crontab.guru/</a> </div>'
                }),
                (_('Important dates'), {
                    'fields': ('last_run_at', )
                }),
            )
        return (
                (None, {
                    'fields': ('job_name', 'job_hash')
                }),
                (_('Job Detail'), {
                    'fields': ('job_schedule', 'job_path', 'status'),
                    'description': f'<div class="help">See detail job schedule in <a href = "https://crontab.guru/#{detail_schedule}"> https://crontab.guru/</a> </div>'
                }),
                (_('Important dates'), {
                    'fields': ('last_run_at', )
                }),
            )
    def run_now(self, request, job_hash):
        try:
            job = cronjob.CronjobModel.objects.get(job_hash=job_hash)
        except cronjob.CronjobModel.DoesNotExist:
            return HttpResponseRedirect('/admin/myapp/cronjobmodel/')
        if job.status != 1 and not job.deleted_at:
            t2 = Thread(target=call_docker_cron_cmd, kwargs=dict(sub_cmd='run', job_identifier=job_hash))
            t2.start()
        return HttpResponseRedirect('/admin/myapp/cronjobmodel/')
    def add_to_crontab(self, request, job_id):
        call_docker_cron_cmd(sub_cmd='add_one', job_identifier=job_id)
        return HttpResponseRedirect('/admin/myapp/cronjobmodel/')
    def remove_from_crontab(self, request, job_hash):
        call_docker_cron_cmd(sub_cmd='remove_one', job_identifier=job_hash)           
        return HttpResponseRedirect('/admin/myapp/cronjobmodel/')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<job_hash>.+)/run_now/$',
                self.admin_site.admin_view(self.run_now),
                name='run-now',
            ),
            url(
                r'^(?P<job_hash>.+)/remove_from_crontab/$',
                self.admin_site.admin_view(self.remove_from_crontab),
                name='remove-from-crontab',
            ),
            url(
                r'^(?P<job_id>.+)/add_to_crontab/$',
                self.admin_site.admin_view(self.add_to_crontab),
                name='add-to-crontab',
            ),
        ]
        return custom_urls + urls
    def cronjob_actions(self, obj):
        tag_run = tag_add = tag_remove = True
        run = add = remove = ''
        if obj.deleted_at:
            tag_add = tag_run = False
            run = add = 'disabled'            
        elif obj.job_hash:
            tag_add = False
            add = 'disabled'
        if obj.status == 1 or not obj.job_hash:
            tag_run = tag_remove = False
            run = remove = 'disabled'
        return format_html(
            '<a class="button" {} onclick="return {};" href="{}">Run now</a>&nbsp;'
            '<a class="button" {} onclick="return {};" href="{}">Add crontab</a>&nbsp;'
            '<a class="button" {} onclick="return {};" href="{}">Remove crontab</a>',
            run, tag_run,
            reverse('admin:run-now', args=[obj.job_hash]),
            add, tag_add,
            reverse('admin:add-to-crontab', args=[obj.id]),
            remove, tag_remove,
            reverse('admin:remove-from-crontab', args=[obj.job_hash]),
        )
    
    def has_delete_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('delete', opts)
        extra_condition = True
        if obj:
            extra_condition = not obj.job_hash
        return request.user.has_perm("%s.%s" % (opts.app_label, codename)) and extra_condition

admin.site.register(cronjob.CronjobModel, CronjobAdmin)
