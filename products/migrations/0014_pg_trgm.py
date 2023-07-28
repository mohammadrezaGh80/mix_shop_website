from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_answer_answerdislike_answerlike_and_more'),
    ]

    operations = [
        TrigramExtension()
    ]
