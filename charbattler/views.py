from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from .models import Character, Matchup
import random


# Todo: add "comment on last matchup" link
def index(request):
    matchup = Matchup.objects.random()
    mix_up_val = random.randint(0, 1)
    return render(request, 'charbattler/index.html', context={'matchup': matchup, 'mix_up_val': mix_up_val})


def vote(request):
    matchup = Matchup.objects.get(pk=request.POST['matchup'])
    matchup.update_wins(request.POST['winner'])
    messages.add_message(request, messages.INFO, matchup.pk)
    return HttpResponseRedirect(reverse('index'))


class CharacterListView(generic.ListView):
    model = Character
    queryset = Character.objects.order_by('name')


class CharacterDetailView(generic.DetailView):
    model = Character


class MatchupDetailView(generic.DetailView):
    model = Matchup