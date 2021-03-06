# Generated by Django 3.0.3 on 2020-04-13 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0002_score_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge_name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('STARTED', 'STARTED'), ('FINISHED', 'FINISHED')], default='FINISHED', max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='score',
            name='challenge_name',
        ),
        migrations.RemoveField(
            model_name='score',
            name='run_id',
        ),
        migrations.AddField(
            model_name='score',
            name='round',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='scores.Round'),
        ),
    ]
