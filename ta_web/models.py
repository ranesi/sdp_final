from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

import django.core.exceptions

import json
# import datetime
from . import eq
from .calc import analyze_string
from .topics import textrazor_topics
from .nltk_process import fdist_graph, get_longest_words, tokenize

User._meta.get_field('email')._blank = False  # TODO email validator


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    signup_date = models.DateTimeField()
    description = models.CharField(max_length=200, blank=True, null=True)
    website_url = models.CharField(
        max_length=200, null=True)  # TODO url validator

    def __str__(self):
        return '{}, {}'.format(self.user.username, self.signup_date)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except django.core.exceptions.ObjectDoesNotExist:
        pass


class DocumentAnalysis(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='analysis')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.TextField(blank=True, null=True)
    readability_index = models.FloatField(blank=True, null=True)
    fk_grade_level = models.FloatField(blank=True, null=True)
    ari = models.FloatField(blank=True, null=True)
    smog = models.FloatField(blank=True, null=True)

    def get_topics(self):
        return json.loads(self.topics)

    def set_topics(self, topics):
        self.topics = json.dumps(topics)

    def get_readability_index(self):
        return self.readability_index

    def set_readability_index(self, ri):
        self.readability_index = ri

    def get_fk_grade_level(self):
        return self.fk_grade_level

    def set_fk_grade_level(self, fkgl):
        self.fk_grade_level = fkgl

    def get_ari(self):
        return self.ari

    def set_ari(self, ari):
        self.ari = ari

    def get_smog(self):
        return self.smog

    def set_smog(self, smog):
        self.smog = smog

    def set_indices(self):
        self.topics = textrazor_topics(self.document.text)

        self.sentences, self.words, self.syllables, \
        self.characters, self.poly_syllables = analyze_string(
            self.document.text)

        self.readability_index = eq.fk_re(
            self.words, self.sentences, self.syllables
        )

        self.fk_grade_level = eq.fk_gl(
            self.words, self.sentences, self.syllables
        )
        self.ari = eq.ari(
            self.words, self.sentences, self.characters
        )

        self.smog = eq.smog(self.poly_syllables)

    def __str__(self):
        return 'Analysis of {}'.format(self.document.title)


class Document(models.Model):
    title = models.CharField(max_length=200)
    date_submitted = models.DateTimeField(blank=True, null=True)
    tokens = models.TextField(blank=True, null=True)
    topics = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    sentences = models.IntegerField(blank=True, null=True)
    words = models.IntegerField(blank=True, null=True)
    syllables = models.IntegerField(blank=True, null=True)
    characters = models.IntegerField(blank=True, null=True)
    polysyllables = models.IntegerField(blank=True, null=True)
    readability_index = models.FloatField(blank=True, null=True)
    fk_grade_level = models.FloatField(blank=True, null=True)
    ari = models.FloatField(blank=True, null=True)
    smog = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_date_submitted(self):
        return self.date_submitted

    def get_tokens(self):
        """
            Returns token list, after de-JSONification
        """
        return json.loads(self.text)

    def set_tokens(self, text):
        """
             Using JSON to store tokens within the database
        """
        self.tokens = json.dumps(text)

    def submit(self):
        """
            Process submitted text.
        """
        self.date_submitted = timezone.now()  # django utils
        # self.date_submitted = datetime.datetime.now()
        self.topics = textrazor_topics(self.text)
        self.sentences, self.words, self.syllables, \
        self.characters, self.poly_syllables = analyze_string(
            self.text)

        self.readability_index = eq.fk_re(
            self.words, self.sentences, self.syllables)

        self.fk_grade_level = eq.fk_gl(
            self.words, self.sentences, self.syllables)

        self.ari = eq.ari(self.words, self.sentences, self.characters)

        self.smog = eq.smog(self.poly_syllables)

    def __str__(self):
        return '{}: {}, {}'.format(self.user.username, self.title, self.date_submitted)
