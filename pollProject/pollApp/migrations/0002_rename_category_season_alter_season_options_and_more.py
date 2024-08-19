# Generated by Django 4.2.6 on 2023-12-03 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Season',
        ),
        migrations.AlterModelOptions(
            name='season',
            options={'verbose_name_plural': 'Seasons'},
        ),
        migrations.RenameField(
            model_name='question',
            old_name='categories',
            new_name='seasons',
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='category',
            new_name='season',
        ),
    ]
