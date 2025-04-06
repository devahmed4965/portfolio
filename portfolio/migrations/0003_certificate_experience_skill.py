# Generated by Django 5.2 on 2025-04-06 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_podcastepisode_videoproject_delete_project_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Certificate Title')),
                ('issuing_organization', models.CharField(blank=True, max_length=100, verbose_name='Issuing Organization')),
                ('image', models.ImageField(upload_to='certificates/', verbose_name='Certificate Image/Screenshot')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Verification Link (Optional)')),
                ('date_issued', models.DateField(blank=True, null=True, verbose_name='Date Issued (Optional)')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active?')),
            ],
            options={
                'verbose_name': 'Certificate',
                'verbose_name_plural': 'Certificates',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Title / Position')),
                ('company_or_institution', models.CharField(max_length=100, verbose_name='Company / Institution')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date (Leave blank if current)')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_education', models.BooleanField(default=False, verbose_name='Is this education?')),
                ('order', models.IntegerField(default=0, verbose_name='Order (Recent first)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active?')),
            ],
            options={
                'verbose_name': 'Experience/Education',
                'verbose_name_plural': 'Experience/Education',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Skill Name')),
                ('icon_class', models.CharField(blank=True, max_length=50, verbose_name="Font Awesome Icon Class (e.g., 'fab fa-python')")),
                ('icon_image', models.ImageField(blank=True, null=True, upload_to='skill_icons/', verbose_name='Icon Image (alternative)')),
                ('color', models.CharField(blank=True, help_text='Hex color code (e.g., #3776ab)', max_length=7, verbose_name='Icon Color')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active?')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'ordering': ['order'],
            },
        ),
    ]
