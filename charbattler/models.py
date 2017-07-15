import random

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


# Todo: look into different options for getting random model instances
class RandomManager(models.Manager):
    def random(self):
        """Return a random model instance."""
        return self.all()[random.randint(0, self.all().count() - 1)]


def origin_image_path(instance, filename):
    """Return a path where an Origin instance's image field file will be saved.

    Args:
        instance: the Origin instance that the image belongs to
        filename: the original filename of the uploaded image
    Returns:
        a string in the format: "origin_images/origin-name.ext"
    """
    return 'origin_images/{0}.{1}'.format(slugify(instance.name), filename.split('.')[-1])


class Origin(models.Model):

    """The original media characters come from; franchises, universes, movies, TV shows, etc.

    Model fields:
        name: The name of the original media
        more_info_url: A url linking to more detailed info about the media
        image: An image representing the original media, optional
        description: A brief description of the original media, optional
    """

    name = models.CharField(max_length=200, unique=True)
    more_info_url = models.URLField()
    image = models.ImageField(upload_to=origin_image_path, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


def character_image_path(instance, filename):
    """Return a path where a Character instance's image field file will be saved.

    Args:
        instance: the Character instance that the image belongs to
        filename: the original filename of the uploaded image
    Returns:
         a string in the format: "character_images/origin-name/character-name.ext"
    """
    return 'character_images/{0}/{1}.{2}'.format(slugify(instance.origin), slugify(instance.name), filename.split('.')[-1])


class Character(models.Model):
    """A Character from some outside media.

    Model fields:
        The two fields below must be unique together:
        name: The name of the character, displayed in the battler, in lists, etc.
        origin: An Origin instance representing the original media the Character is from

        image: Image to be displayed in the battler, on detail page, etc.

        Only one of the two fields below is required:
        bio: A short description of the character
        more_info_url: A url to an outside page providing more detailed info about the character

        Statistics (all start from 0):
        total_wins: Total wins across all matchups
        total_losses: Total losses across all matchups
        total_origin_wins: Total wins in matchups against Characters from the same Origin
        total_origin_losses: Total losses in matchups against Characters from the same Origin
    """

    name = models.CharField(max_length=200)
    origin = models.ForeignKey(Origin)

    image = models.ImageField(upload_to=character_image_path)

    bio = models.TextField(null=True, blank=True)
    more_info_url = models.URLField(null=True, blank=True)

    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    total_origin_wins = models.IntegerField(default=0)
    total_origin_losses = models.IntegerField(default=0)

    objects = RandomManager()

    class Meta():
        unique_together = ('name', 'origin')

    def __str__(self):
        return self.name


# TODO: add validation to ensure duplicates are not created
class Matchup(models.Model):

    """Stores pairs of 2 Characters.

    Fields:
        first_character: One Character of the pair.
        second_character: One Character of the pair.
        first_character_wins: The number of times first_character has won against second_character.
        second_character_wins: The number of times second_character has won against first_character.
    """

    first_character = models.ForeignKey(Character, related_name='first_character')
    second_character = models.ForeignKey(Character, related_name='second_character')
    first_character_wins = models.IntegerField(default=0)
    second_character_wins = models.IntegerField(default=0)

    objects = RandomManager()

    def __str__(self):
        return '{} vs. {}'.format(self.first_character.name, self.second_character.name)

    def update_wins(self, winner_pk):
        if int(winner_pk) == self.first_character.pk:
            winner = self.first_character
            loser = self.second_character
        else:
            winner = self.second_character
            loser = self.first_character

        winner.total_wins += 1
        loser.total_losses += 1
        if winner.origin == loser.origin:
            winner.total_origin_wins += 1
            loser.total_origin_losses += 1

        winner.save(update_fields=['total_wins', 'total_losses'])
        loser.save(update_fields=['total_wins', 'total_losses'])


@receiver(post_save, sender=Character)
def create_matchups(sender, instance, created, **kwargs):
    # This function is called every time a Character model is saved.
    # If the instance is new, it creates Matchup instances with the saved Character and every other Character in the
    # database (except itself).
    if created:
        for char in Character.objects.all():
            if char != instance:
                match = Matchup(first_character=instance, second_character=char)
                match.save()


# Todo: add documentation
class Comment(models.Model):
    content = models.TextField()
    post_datetime = models.DateTimeField()
    matchup = models.ForeignKey(Matchup)