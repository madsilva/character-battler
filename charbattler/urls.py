from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^characters/$', views.CharacterListView.as_view(), name='character-list'),
    url(r'^characters/(?P<pk>[0-9]+)$', views.CharacterDetailView.as_view(), name='character-detail'),
    url(r'^matchups/(?P<pk>[0-9]+)$', views.MatchupDetailView.as_view(), name='matchup-detail'),
    url(r'^origin/(?P<pk>[0-9]+)$', views.OriginDetailView.as_view(), name="origin-detail"),
    url(r'^origin/$', views.OriginListView.as_view(), name='origin-list'),
]
