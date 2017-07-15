from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
import random


# honestly not sure if I need this
class RandomManager(models.Manager):
    # Returns a random model instance
    def random(self):
        return self.all()[random.randint(0, self.all().count() - 1)]


# This function returns a path where an Origin instance's image field file will be saved.
# Paths are: "media/origin_images/origin-name.ext"
def origin_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'origin_images/{0}.{1}'.format(slugify(instance.name), ext)


# This model represents the original media characters come from; franchises, universes, movies, TV shows, etc.
class Origin(models.Model):
    # The name of the original media
    name = models.CharField(max_length=200, unique=True)
    # A url linking to more detailed info about the media
    more_info_url = models.URLField()
    # An image representing the original media, optional
    image = models.ImageField(upload_to=origin_image_path, null=True, blank=True)
    # A brief description of the original media, optional
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# This function returns a path where a Character instance's image field will be saved.
# Paths are: "media/character_images/origin-name/character-name.ext"
def character_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'character_images/{0}/{1}.{2}'.format(slugify(instance.origin), slugify(instance.name), ext)


class Character(models.Model):
    # The name of the character, displayed in the battler, in lists, etc.
    name = models.CharField(max_length=200)
    # The original media of the character
    origin = models.ForeignKey(Origin)
    # Image to be displayed in the battler, on detail page, etc.
    image = models.ImageField(upload_to=character_image_path)

    # Only one of the two fields below is required
    # A short description of the character
    bio = models.TextField(null=True, blank=True)
    # A url to an outside page providing more detailed info about the character
    more_info_url = models.URLField(null=True, blank=True)

    # Stats for the character
    # Total wins and losses across all matchups
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    # Total wins and losses in matchups with characters from the same origin
    total_origin_wins = models.IntegerField(default=0)
    total_origin_losses = models.IntegerField(default=0)

    objects = RandomManager()

    class Meta():
        unique_together = ('name', 'origin')

    # override
    def __str__(self):
        return self.name


# This function is called every time a Character model is saved.
# If the instance is new, it creates Matchup instances with the saved Character and every other Character in the
# database (except itself).
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

    def update_wins(self, winner_pk):
        if int(winner_pk) == self.char1.pk:
            winner = self.char1
            loser = self.char2
        else:
            winner = self.char2
            loser = self.char1

        winner.total_wins += 1
        loser.total_losses += 1
        if winner.origin == loser.origin:
            winner.total_origin_wins += 1
            loser.total_origin_losses += 1

        winner.save(update_fields=['total_wins', 'total_losses'])
        loser.save(update_fields=['total_wins', 'total_losses'])

    def __str__(self):
        return '%s vs. %s' % (self.char1.name, self.char2.name)


class Comment(models.Model):
    content = models.TextField()
    post_datetime = models.DateTimeField()
    matchup = models.ForeignKey(Matchup)