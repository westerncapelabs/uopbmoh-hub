from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'facilitycode', views.FacilityCodeViewSet)

urlpatterns = [
    url('^login/', auth_views.login, {
        'template_name': 'hub/login.html'
    }, name='login'),
    url('^logout/', auth_views.logout, name='logout'),
    url(r'^api/v1/', include(router.urls)),
    url('^results/$', views.quiz_results, name='quiz-results'),
    url('^result/(?P<tracker_id>[^/]+)/$', views.quiz_results_detail,
        name='quiz-results-detail'),
    url('^quizzes/$', views.quizzes, name='quizzes'),
    url('^results-download/$', views.results_download,
        name='results-download'),
    url('^quiz/(?P<quiz_id>[^/]+)/$', views.quiz_detail,
        name='quiz-detail'),
    url('^quiz/edit/(?P<quiz_id>[^/]+)/$', views.quiz_edit,
        name='quiz-edit'),
    url('^quiz/add-questions/(?P<quiz_id>[^/]+)/$', views.quiz_add_questions,
        name='quiz-add-questions'),
    url('^questions/$', views.questions, name='questions'),
    url('^question/(?P<question_id>[^/]+)/$', views.question_detail,
        name='question-detail'),
    url('^question/edit/(?P<question_id>[^/]+)/$', views.question_edit,
        name='question-edit'),
    url('^users/$', views.users, name='users'),
    url('^user/(?P<user_id>[^/]+)/$', views.user_detail,
        name='user-detail'),
    url('^facilities/$', views.facilities, name='facilities'),
    url('', views.index, name='index'),
]
