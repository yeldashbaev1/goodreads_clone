# Generated by Django 4.0.1 on 2024-01-13 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_cover_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_picture',
            field=models.ImageField(default='bookq.jpg', upload_to=''),
        ),
    ]
