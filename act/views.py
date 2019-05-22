from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.dateparse import parse_datetime
from .models import ExtendUser, Activity
from .forms import ExtendUserCreationForm, ActivityCreateForm

# Create your views here.

class UserCreate(generic.CreateView): # pylint: disable=too-many-ancestors
    model = ExtendUser
    form_class = ExtendUserCreationForm
    template_name = "registration/extenduser_form.html"

    def get_success_url(self):
        messages.success(self.request, '帳戶已創立')
        return redirect('/login')

def index(request):
    return redirect('/activity')

def activity_list(request):
    return render(request, 'blog/activityList.html')

def get_activity(request):
    start = parse_datetime(request.GET.get("start"))
    end = parse_datetime(request.GET.get("end"))
    activities = Activity.objects.filter(start__lte=end, end__gte=start)
    json = []
    for activity in activities:
        json.append({
            "start": activity.start,
            "end": activity.end,
            "title": activity.title,
            "url": f"/activity/{activity.id}"
        })
    return JsonResponse(json, safe=False)

def activity_detail(request, aid):
    activity = Activity.objects.get(id=aid)
    return render(request, 'blog/activityDetail.html', {'activity': activity})

@login_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityCreateForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.author = request.user
            activity.save()
            return redirect('/activity')
        return HttpResponse("Error")
    form = ActivityCreateForm()
    return render(request, 'blog/activityCreate.html', {'form': form})

@login_required
def activity_delete(request, aid):
    if request.method == 'GET':
        activity = Activity.objects.get(id=aid)
        if activity.author == request.user:
            activity.delete()
            return redirect('/activity')
        return HttpResponse("Your are not author.")
    return HttpResponse('Method Not Allow.')

@login_required
def activity_edit(request, aid):
    activity = Activity.objects.get(id=aid)
    if activity.author == request.user:
        if request.method == 'POST':
            form = ActivityCreateForm(request.POST, instance=activity)
            if form.is_valid():
                form.save()
                return redirect(activity_detail, id)
            return HttpResponse("Error")
        form = ActivityCreateForm(instance=activity)
        return render(request, 'blog/activityCreate.html', {'form': form})
    return HttpResponse("Your are not author.")
