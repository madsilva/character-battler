import random

from django.contrib import messages
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views import generic

from .models import Character, Matchup, Origin
from .forms import CustomBattleForm, OriginOptionsForm


def index(request):
    base_matchup = Matchup.objects.filter(first_character__isHidden=False, second_character__isHidden=False)

    origin_options_form_set = formset_factory(OriginOptionsForm, extra=3)

    formset = origin_options_form_set()
    custom_battle_form = CustomBattleForm()
    if request.method == 'POST':
        if 'clear-session' in request.POST:
            # if the user has clicked the "Clear options" button, the session is reset and all custom parameters go away.
            request.session.flush()
            matchup = Matchup.objects.random(base_matchup)
        elif 'action' in request.POST:
            # if the user has submitted the custom battle options form, those options must be processed.
            formset = origin_options_form_set(request.POST)
            custom_battle_form = CustomBattleForm(request.POST)
            if custom_battle_form.is_valid() and formset.is_valid():
                request.session['include_same_origin_matchups'] = custom_battle_form.cleaned_data['include_same_origin_matchups']
                request.session['origins'] = []
                for origin_form in formset:
                    origin_pk = origin_form.cleaned_data.get('origin')
                    request.session['origins'].append(origin_pk.pk)

    if 'origins' in request.session:
        # if the user has custom battle options stored in their session, a matchup is produced that fits those options
        q = Q()

        for origin_pk in request.session['origins']:
            origin = Origin.objects.get(pk=origin_pk)

            if request.session['include_same_origin_matchups'] is True:
                 q.add(Q(first_character__origin=origin, second_character__origin=origin), q.OR)

            for other_pk in request.session['origins']:
                other_origin = Origin.objects.get(pk=other_pk)
                if other_origin.pk != origin.pk:
                    q.add(Q(first_character__origin=origin, second_character__origin=other_origin), q.OR)
                    q.add(Q(first_character__origin=other_origin, second_character__origin=origin), q.OR)

        matchup = Matchup.objects.random(base_matchup.filter(q))
    else:
        matchup = Matchup.objects.random(base_matchup)

    mix_up_val = random.randint(0, 1)
    return render(request, 'charbattler/index.html', context={'matchup': matchup, 'mix_up_val': mix_up_val, 'origin_options_form': formset, 'custom_battle_form': custom_battle_form})


def vote(request):
    '''
    context variables sent by matchup form:
    matchup: the pk of the matchup that's being voted on
    winner: the pk of the character in the matchup that was voted to win
    redirect_url: the name of the url to redirect to after the vote is processed (almost certainly the page that sent the vote request)
    '''
    matchup = Matchup.objects.get(pk=request.POST['matchup'])
    matchup.update_wins(request.POST['winner'])
    messages.add_message(request, messages.INFO, matchup.pk, extra_tags='comment_on_last_matchup')
    return redirect(request.POST['redirect_url'])


def jojo_battler(request):
    origin = Origin.objects.get(name='Jojo\'s Bizarre Adventure')
    matchup = Matchup.objects.random(Matchup.objects.filter(first_character__origin=origin, second_character__origin=origin))
    mix_up_val = random.randint(0, 1)
    return render(request, 'charbattler/jojo_battler.html', context={'matchup': matchup, 'mix_up_val': mix_up_val})


class Top10ListView(generic.ListView):
    model = Character
    queryset = Character.objects.order_by('-total_wins')[:10]
    template_name = 'charbattler/top10_list.html'


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
