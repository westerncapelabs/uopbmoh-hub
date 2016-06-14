from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^login/', auth_views.login, {
        'template_name': 'hub/login.html'
    }, name='login'),
    url('^quiz/', views.quiz_results, name='quiz-results'),
    url(r'', views.index, name='index'),
]
