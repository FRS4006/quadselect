from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    #session = models.ForeignKey('Session', related_name='session_videos', null=True, blank=True,on_delete=models.CASCADE)
    # session = models.ManyToManyField('Session', related_name='session_videos', blank=True,)

    def __str__(self):
        return self.name


class Session(models.Model):
    WEEK_CHOICES = [(i, f'Week {i}') for i in range(1, 10)]
    SESSION_TYPE=[(1,'Custom'),(2,'Core')]
    name = models.CharField(max_length=100)
    week = models.IntegerField(choices=WEEK_CHOICES, default=1)
    type = models.IntegerField(choices=SESSION_TYPE)
    # this should probably be renamed
    topics = models.ManyToManyField(Topic, related_name='sessions', blank=True)
    videos = models.ManyToManyField(Video, related_name='sessions', blank=True)
    course = models.ForeignKey('Course', related_name='sessions', null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.get_week_display()}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    # sessions = models.ManyToManyField(Session, related_name='session_courses', blank=True)
    # sessions = models.ManyToManyField(Session, related_name='session_courses', blank=True)
    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    #This means the Partcipant model has to be as same as the User model, this is optional
    #Since we want to make this database general, if we change the required info, no need to change the 'trunk'
    name = models.CharField(max_length=100)
    studyID = models.CharField(max_length=100,null=True)
    courses = models.ManyToManyField(Course, related_name='participants', blank=True)

    def __str__(self):
        return self.name


class ParticipantSession(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    completed = models.BooleanField()

    @classmethod
    def create(cls, session, participant, topic):
        participantsession = cls(session = session, participant = participant, topic = topic)

    def __str__(self):
        return f"{self.participant} session number: {self.session}"