# Generated by Django 5.0.6 on 2024-07-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NepalLicenseScholar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=122)),
                ('email', models.CharField(max_length=122)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=122)),
                ('password', models.CharField(max_length=112)),
                ('date', models.DateField()),
            ],
        ),
    ]
