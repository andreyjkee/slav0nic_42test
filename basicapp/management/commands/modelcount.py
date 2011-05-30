#coding: utf-8
from django.core.management.base import BaseCommand
from django.db.models import get_models


class Command(BaseCommand):
    help = u"""
      ticket:9 Command that prints all project models and the
      count of objects in every model
    """
    args = ''
    requires_model_validation = True

    def handle(self, *args, **options):
        for m in get_models():
            data = "%s.%s:\t%i\n" % (m._meta.app_label,
                                                m._meta.module_name.capitalize(),
                                                m.objects.count())
            self.stdout.write(data)
            self.stderr.write("error: " + data)
