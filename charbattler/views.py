from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from .models import Character, Matchup, Origin
import random


def index(request):
    matchup = Matchup.objects.random()
    mix_up_val = random.randint(0, 1)
    return render(request, 'charbattler/index.html', context={'matchup': matchup, 'mix_up_val': mix_up_val})


def about(request):
    return render(request, 'charbattler/about.html')


def vote(request):
    matchup = Matchup.objects.get(pk=request.POST['matchup'])
    matchup.update_wins(request.POST['winner'])
    messages.add_message(request, messages.INFO, matchup.pk)
    return HttpResponseRedirect(reverse('index'))


def overall_rankings(request):
    top10 = Character.objects.order_by('total_wins')[:10]
    return render(request, 'charbattler/overall_rankings.html', context={'top10': top10})


class CharacterListView(generic.ListView):
    model = Character
    queryset = Character.objects.order_by('name')


class CharacterDetailView(generic.DetailView):
    model = Character


class OriginListView(generic.ListView):
    model = Origin


class OriginDetailView(generic.DetailView):
    model = Origin


class MatchupDetailView(generic.DetailView):
    model = Matchup


