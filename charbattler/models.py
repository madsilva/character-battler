from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import random


class RandomManager(models.Manager):
    # Returns a random model instance
    def random(self):
        return self.all()[random.randint(0, self.all().count() - 1)]


# TODO: add image file field
class Character(models.Model):

    name = models.CharField(max_length=200)
    bio = models.TextField()
    origin = models.ForeignKey(Origin)
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    #image = models.ImageField()

    objects = RandomManager()

    def __str__(self):
        return self.name


# This function is called every time a Character model is saved
@receiver(post_save, sender=Character)
def create_matchups(sender, instance, created, **kwargs):
    if created:
        for char in Character.objects.all():
            if char != instance:
                match = Matchup(char1=instance, char2=char)
                match.save()


# TODO: add validation to ensure duplicates are not created
class Matchup(models.Model):

    char1 = models.ForeignKey(Character, related_name='char1')
    char2 = models.ForeignKey(Character, related_name='char2')
    char1_wins = models.IntegerField(default=0)
    char2_wins = models.IntegerField(default=0)

    objects = RandomManager()

    def update_wins(self, winner):
        if int(winner) == self.char1.pk:
            self.char1.total_wins += 1
            self.char1_wins += 1
            self.char2.total_losses += 1
        else:
            self.char2.total_wins += 1
            self.char2_wins += 1
            self.char1.total_losses += 1
        self.char1.save()
        self.char2.save()

    def __str__(self):
        return '%s vs. %s' % (self.char1.name, self.char2.name)


class Origin(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Comment(models.Model):
    content = models.TextField()
    post_datetime = models.DateTimeField()
    matchup = models.ForeignKey(Matchup)