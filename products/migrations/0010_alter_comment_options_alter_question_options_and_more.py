# Generated by Django 4.1.7 on 2023-06-10 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_question_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='suggestion',
            field=models.PositiveSmallIntegerField(choices=[(0, 'None'), (1, 'I suggest'), (2, "I don't suggest"), (3, "I'm not sure")], default=0, verbose_name='Suggestion'),
        ),
    ]
