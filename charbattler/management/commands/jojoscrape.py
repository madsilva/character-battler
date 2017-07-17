import requests
import urllib
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from charbattler.models import Character, Origin, character_image_path


class Command(BaseCommand):
    help = 'help'

    def handle(self, *args, **options):
        response = requests.get('http://jojo.wikia.com/wiki/Category:Characters')
        html = BeautifulSoup(response.content, 'html.parser')
        characters = html.find_all(class_='image image-thumbnail link-internal')
        origin = Origin.objects.get(name='Jojo\'s Bizarre Adventure')
        for character in characters:

            char_name = character['title']
            if not Character.objects.filter(name=char_name, origin=origin).exists():
                url = 'http://jojo.wikia.com' + character['href']
                new_character = Character(name=char_name, more_info_url=url, origin=origin)
                path = character_image_path(new_character, 'char.png')
                fullpath = 'media/' + path
                if character.contents[0].has_attr('data-src'):

                    urllib.request.urlretrieve(character.contents[0]['data-src'], fullpath)
                else:

                    urllib.request.urlretrieve(character.contents[0]['src'], fullpath)
                new_character.image = path
                new_character.save()
            else:
                print('error caused by: ' + char_name)
