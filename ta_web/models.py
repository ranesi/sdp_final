from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# import datetime
from . import eq
from .calc import analyze_string
from .topics import get_topics

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


class Document(models.Model):
    title = models.CharField(max_length=200)
    date_submitted = models.DateTimeField(blank=True, null=True)
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

    def submit(self):
        """
            Process submitted text.
        """
        self.date_submitted = timezone.now() # django utils
        # self.date_submitted = datetime.datetime.now()
        self.topics = get_topics(self.text)
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
        return '{}, {}'.format(self.title, self.date_submitted)
