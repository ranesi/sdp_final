from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Document, DocumentAnalysis

import django.core.exceptions

@receiver(post_save, sender=Document)
def create_document_analysis(sender, instance, created, **kwargs):
    if created:
        da = DocumentAnalysis.objects.create(document=instance, user=instance.user)
        da.set_indices()
        da.save()

@receiver(post_save, sender=Document)
def save_document(sender, instance, **kwargs):
    try:
        instance.analysis.save()
    except django.core.exceptions.ObjectDoesNotExist:
        pass
