from django import forms

class CronjobForm(forms.ModelForm):
    class Meta:
        labels = {
            'job_path_view': 'job path (*)',
            'job_schedule_view': 'job schedule (*)',
        }