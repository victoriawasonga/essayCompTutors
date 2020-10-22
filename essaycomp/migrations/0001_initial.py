# Generated by Django 3.1.2 on 2020-10-20 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import essaycomp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=19)),
                ('academic_level', models.CharField(choices=[('highschool', 'High School'), ('undergraduate', 'Undergraduate'), ('masters', 'Masters'), ('doctrate', 'Doctrate')], max_length=50, null=True)),
                ('type_of_paper', models.CharField(choices=[('custom_essay', 'Custom Essay'), ('research_paper', 'Research Paper'), ('presentation', 'Presentation'), ('thesis', 'Thesis'), ('doctrate', 'Doctrate')], max_length=50, null=True)),
                ('topic', models.CharField(max_length=500, null=True)),
                ('instructions', models.CharField(max_length=500, null=True)),
                ('attachements', models.FilePathField(null=True, path=essaycomp.models.images_path)),
                ('reference', models.CharField(choices=[('apa', 'APA'), ('mla', 'MLA'), ('chicago', 'Chicago'), ('others', 'Others')], max_length=50, null=True)),
                ('deadline', models.CharField(choices=[('1wk', '1 Week'), ('3days', '3 Days'), ('1day', '1 Day'), ('24hours', '24 Hours'), ('12hours', '12 hours')], max_length=50, null=True)),
                ('sources', models.IntegerField(default=1)),
                ('pages', models.IntegerField(default=1)),
                ('spacing', models.CharField(choices=[('single', 'Single'), ('double', 'Double ')], max_length=50, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]