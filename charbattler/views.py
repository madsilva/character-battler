import random

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Character, Matchup, Origin


def index(request):
    matchup = Matchup.objects.random(Matchup.objects.filter(obscurity_rating__lte=1, first_character__isHidden=False, second_character__isHidden=False))
    mix_up_val = random.randint(0, 1)
    return render(request, 'charbattler/index.html', context={'matchup': matchup, 'mix_up_val': mix_up_val})


def vote(request):
    '''
    context variables sent by matchup form:
    matchup: the pk of the matchup that's being voted on
    winner: the pk of the character in the matchup that was voted to win
    redirect: the name of the url to redirect to after the vote is processed (almost certainly the page that sent the vote request)
    '''
    matchup = Matchup.objects.get(pk=request.POST['matchup'])
    matchup.update_wins(request.POST['winner'])
    messages.add_message(request, messages.INFO, matchup.pk)
    return HttpResponseRedirect(reverse(request.POST['redirect']))


def jojo_battler(request):
    origin = Origin.objects.get(name='Jojo\'s Bizarre Adventure')
    matchup = Matchup.objects.random(Matchup.objects.filter(first_character__origin=origin, second_character__origin=origin))
    mix_up_val = random.randint(0, 1)
    return render(request, 'charbattler/jojo_battler.html', context={'matchup': matchup, 'mix_up_val': mix_up_val})


def overall_rankings(request):
    top10 = Character.objects.order_by('-total_wins')[:10]
    return render(request, 'charbattler/overall_rankings.html', context={'top10': top10})


class OriginListView(generic.ListView):
    model = Origin


class OriginDetailView(generic.DetailView):
    model = Origin


class CharacterListView(generic.ListView):
    model = Character
    queryset = Character.objects.filter(isHidden=False).order_by('name')


class CharacterDetailView(generic.DetailView):
    model = Character


class MatchupDetailView(generic.DetailView):
    model = Matchup
