# Generated by Django 4.1.7 on 2023-03-18 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_app', '0005_student_classes_tutor_classes'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorClasses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('complete', models.BooleanField()),
                ('tutorclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauth_app.tutorclasses')),
            ],
        ),
    ]
