# Generated by Django 2.1.5 on 2019-01-16 03:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FindMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_match', models.DateTimeField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_match', models.DateTimeField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('find_match_a', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team_a', to='myapp.FindMatch')),
                ('find_match_b', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team_b', to='myapp.FindMatch')),
            ],
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=217)),
                ('price', models.IntegerField()),
                ('bank_num', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StadiumRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_from', models.DateTimeField()),
                ('time_to', models.DateTimeField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('CANCEL', 'Cancel')], default='PENDING', max_length=10)),
                ('total_price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.Stadium')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=30)),
                ('team_profile_image_url', models.CharField(max_length=217, null=True)),
                ('acronym', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.CharField(choices=[('MEMBER', 'Member'), ('CAPTION', 'Caption')], default='MEMBER', max_length=10)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='findmatch',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.Team'),
        ),
        migrations.AlterUniqueTogether(
            name='userteam',
            unique_together={('user', 'team')},
        ),
        migrations.AlterUniqueTogether(
            name='stadiumregister',
            unique_together={('user', 'stadium', 'time_from')},
        ),
        migrations.AlterUniqueTogether(
            name='match',
            unique_together={('find_match_a', 'find_match_b', 'date_match')},
        ),
        migrations.AlterUniqueTogether(
            name='findmatch',
            unique_together={('team', 'date_match')},
        ),
    ]
