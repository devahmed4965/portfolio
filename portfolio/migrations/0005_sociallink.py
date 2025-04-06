# Generated by Django 5.2 on 2025-04-06 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('linkedin', 'LinkedIn'), ('github', 'GitHub'), ('instagram', 'Instagram'), ('youtube', 'YouTube'), ('whatsapp', 'WhatsApp'), ('telegram', 'Telegram')], max_length=50, unique=True, verbose_name='المنصة')),
                ('url', models.URLField(verbose_name='الرابط (URL)')),
                ('icon_class', models.CharField(blank=True, help_text='اختياري: أدخل فئة Font Awesome (مثل fab fa-linkedin). إذا تركت فارغاً، سيتم استخدام اسم المنصة.', max_length=50, null=True, verbose_name='فئة الأيقونة (مثل fab fa-facebook-f)')),
            ],
            options={
                'verbose_name': 'رابط تواصل اجتماعي',
                'verbose_name_plural': 'روابط التواصل الاجتماعي',
                'ordering': ['platform'],
            },
        ),
    ]
