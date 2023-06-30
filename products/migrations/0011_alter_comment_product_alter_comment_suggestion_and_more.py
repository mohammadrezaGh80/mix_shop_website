# Generated by Django 4.1.7 on 2023-06-12 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0010_alter_comment_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='suggestion',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'None'), (1, 'I suggest'), (2, "I don't suggest"), (3, "I'm not sure")], default=0, verbose_name='Suggestion'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='question',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='products.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
