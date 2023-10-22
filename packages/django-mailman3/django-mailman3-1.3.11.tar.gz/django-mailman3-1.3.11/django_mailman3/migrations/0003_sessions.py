# -*- coding: utf-8 -*-


from django.contrib.sessions.models import Session
from django.db import migrations


def clear_session(app, schema_editor):
    Session.objects.all().delete()

def undo(app, schema_editor):
    # In case we need to back it out. We can't really restore the table so
    # just pass.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('django_mailman3', '0002_maildomain'),
    ]

    operations = [
        migrations.RunPython(clear_session, undo),
    ]
