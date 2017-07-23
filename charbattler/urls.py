from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^overall_rankings/$', views.overall_rankings, name='overall-rankings'),
    url(r'^characters/$', views.CharacterListView.as_view(), name='character-list'),
    url(r'^characters/(?P<pk>[0-9]+)$', views.CharacterDetailView.as_view(), name='character-detail'),
    url(r'^matchups/(?P<pk>[0-9]+)$', views.MatchupDetailView.as_view(), name='matchup-detail'),
    url(r'^origins/(?P<pk>[0-9]+)$', views.OriginDetailView.as_view(), name="origin-detail"),
    url(r'^origins/$', views.OriginListView.as_view(), name='origin-list'),
    url(r'^about/$', TemplateView.as_view(template_name='charbattler/about.html'), name='about'),
    url(r'^rating_system/$', TemplateView.as_view(template_name='charbattler/obscurity_rating_system.html'), name='rating-system'),
]
