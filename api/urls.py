"""api2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from scores.views import ScoreView, ScoreTableView, PrimeChallengeView, ParticipationView, ScoreDetailView, RoundView, \
    RoundDetailView
from django.conf.urls.static import static

urlpatterns = [
                  path('challenges/<str:challenge_name>/rounds/<str:id>', RoundDetailView.as_view()),
                  path('challenges/<str:challenge_name>/rounds', RoundView.as_view()),
                  path('scores/<int:score_id>', ScoreDetailView.as_view()),
                  path('scores', ScoreView.as_view()),
                  path('challenges/prime', PrimeChallengeView.as_view()),
                  path('participation', ParticipationView.as_view()),
                  path('', ScoreTableView.as_view()),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
