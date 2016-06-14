from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.context_processors import csrf


@login_required(login_url='/login/')
def index(request):
    return render(request, 'hub/index.html')


@login_required(login_url='/login/')
def quiz_results(request):
    context = {}
    results = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": "86bef8d3-721c-4134-a73a-ea4391c3ad28",
                "identity": "1e2ca132-029b-4f3a-b97d-527fd8ac65d6",
                "quiz": "a2698c62-6116-48f0-abe0-70801a230ab9",
                "complete": True,
                "metadata": None,
                "started_at": "2016-05-18T23:44:38.264734Z",
                "created_by": 2,
                "completed_at": "2016-05-19T00:02:02Z",
                "updated_by": 2
            },
            {
                "id": "6b7ace3f-475c-46da-a006-7726e64076b5",
                "identity": "b6386fc5-ed52-41f0-b5af-89d93290a8a9",
                "quiz": "a2698c62-6116-48f0-abe0-70801a230ab9",
                "complete": True,
                "metadata": None,
                "started_at": "2016-05-19T02:00:38.680478Z",
                "created_by": 2,
                "completed_at": "2016-05-19T02:01:13Z",
                "updated_by": 2
            }
        ]
    }
    context.update({
        "results": results
    })
    context.update(csrf(request))
    return render_to_response("hub/quiz-results.html",
                              context,
                              context_instance=RequestContext(request))
