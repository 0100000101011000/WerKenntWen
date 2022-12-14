# Generated by Django 4.1.2 on 2022-11-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wkwapp', '0002_age_gender_image_remove_customuser_username_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_one_id', models.CharField(max_length=3)),
                ('person_two_id', models.CharField(max_length=3)),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Age',
        ),
        migrations.DeleteModel(
            name='Gender',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
