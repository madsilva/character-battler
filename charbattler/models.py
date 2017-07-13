from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
import random


class Origin(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_name_slug(self):
        return slugify(self.name)

class RandomManager(models.Manager):
    # Returns a random model instance
    def random(self):
        return self.all()[random.randint(0, self.all().count() - 1)]

def character_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'character_images/{0}/{1}.{2}'.format(slugify(instance.origin), slugify(instance.name), ext)

# TODO: override validation method
# TODO: name and origin unique together
class Character(models.Model):
    def get_name_slug(self):
        return slugify(self.name)

    # the name of the character, displayed in the battler, in lists, etc.
    name = models.CharField(max_length=200)
    # the original media of the character
    origin = models.ForeignKey(Origin)
    # image to be displayed in the battler, on detail page, etc.
    # stored with the name "name_origin"
    image = models.ImageField(upload_to=character_image_path)

    # only one of the two fields below is required
    # a short description of the character
    bio = models.TextField(null=True, blank=True)
    # a url to an outside page providing more detailed info about the character
    more_info_url = models.URLField(null=True, blank=True)

    # stats for the character
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)

    objects = RandomManager()

    # override
    def clean(self):
        if self.bio is None and self.more_info_url is None:
            raise ValidationError('Character must have bio and/or info link.')

    # override
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


class Comment(models.Model):
    content = models.TextField()
    post_datetime = models.DateTimeField()
    matchup = models.ForeignKey(Matchup)