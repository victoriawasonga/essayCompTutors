# Generated by Django 3.1.2 on 2020-10-21 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essaycomp', '0003_auto_20201021_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='paidorders',
            name='order_progress',
            field=models.CharField(choices=[('recieved', 'Recieved'), ('ongoing', 'ongoing'), ('done', 'Done')], default='recieved', max_length=50, null=True),
        ),
    ]