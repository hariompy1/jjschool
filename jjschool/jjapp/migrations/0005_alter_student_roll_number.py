# Generated by Django 5.0.6 on 2024-06-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jjapp", "0004_student_roll_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="roll_number",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
