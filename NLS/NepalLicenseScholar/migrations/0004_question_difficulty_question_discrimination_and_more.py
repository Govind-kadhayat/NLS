# Generated by Django 5.0.6 on 2024-09-15 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NepalLicenseScholar', '0003_category_question_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='difficulty',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='question',
            name='discrimination',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='question',
            name='guessing',
            field=models.FloatField(default=0.0),
        ),
    ]
