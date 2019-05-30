from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
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
        return '/login'

def user_in_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()

def index(request):
    return redirect('/activity')

def activity_list(request):
    return render(request, 'act/activityList.html')

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
    admin_group = Group.objects.get(name='admin')
    activity = Activity.objects.get(id=aid)
    is_admin = admin_group in request.user.groups.all()
    return render(request, 'act/activityDetail.html', {'activity': activity, 'is_admin': is_admin})

@login_required
@permission_required('act.add_activity')
def activity_create(request):
    if request.method == 'POST':
        form = ActivityCreateForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.author = request.user
            activity.save()
            return redirect('/activity')
        return render(request, 'act/error.html', {'message': '表單發生錯誤'}, status=400)
    form = ActivityCreateForm()
    return render(request, 'act/activityCreate.html', {'form': form})

@login_required
@permission_required('act.delete_activity')
def activity_delete(request, aid):
    if request.method == 'GET':
        activity = Activity.objects.get(id=aid)
        if activity.author == request.user or user_in_group(request.user, 'admin'):
            activity.delete()
            return redirect('/activity')
        return render(request, 'act/error.html', {'message': '僅限作者刪除'}, status=403)
    return render(request, 'act/error.html', {'message': 'Method not allow'}, status=405)

@login_required
@permission_required('act.change_activity')
def activity_edit(request, aid):
    activity = Activity.objects.get(id=aid)
    if request.method == 'POST':
        if activity.author == request.user or user_in_group(request.user, 'admin'):
            form = ActivityCreateForm(request.POST, request.FILES, instance=activity)
            if form.is_valid():
                form.save()
                return redirect(f"/activity/{aid}")
            return render(request, 'act/error.html', {'message': '表單發生錯誤'}, status=400)
        return render(request, 'act/error.html', {'message': '僅限作者修改'}, status=403)
    if activity.author == request.user or user_in_group(request.user, 'admin'):
        form = ActivityCreateForm(instance=activity)
        return render(request, 'act/activityCreate.html', {'form': form})
    return render(request, 'act/error.html', {'message': '僅限作者修改'}, status=403)
