# Generated by Django 4.1.7 on 2023-07-01 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0011_alter_comment_product_alter_comment_suggestion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='number_of_dislikes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='number_of_likes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='number_of_dislikes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='number_of_likes',
        ),
        migrations.CreateModel(
            name='QuestionLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='Modified datetime')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='products.question', verbose_name='Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_likes', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='Modified datetime')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='products.question', verbose_name='Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_dislikes', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='Modified datetime')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='products.comment', verbose_name='Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='CommentDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='Modified datetime')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='products.comment', verbose_name='Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
