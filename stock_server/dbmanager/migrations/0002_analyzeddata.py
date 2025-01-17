# Generated by Django 3.0.5 on 2020-04-22 00:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyzedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('continuous_days', models.IntegerField()),
                ('last_fluctuation', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbmanager.Stock')),
            ],
        ),
    ]
