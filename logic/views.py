from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Participant, Topic, Session, ParticipantSession
from .forms import ParticipantSessionForm
from django.views.decorators.http import require_POST



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_profile(request):
    topics = Topic.objects.all() if Topic else []
    participant = Participant.objects.filter(user=request.user).first()
    user_courses = participant.courses.all() if participant else []
    user_topics = participant.topics.all() if participant else []
    user_ps = ParticipantSession.objects.all() if participant else []
    if request.method == 'GET':
        return render(request, 'interactor.html', {'user_courses': user_courses,'user_topics': user_topics, 'topics': topics})
    # return render(request, 'user_profile.html', {'user_courses': user_courses,'user_topics': user_topics, 'topics': topics})

@login_required
def one(request):
    participant = Participant.objects.filter(user=request.user).first()
    topics = Topic.objects.all() if Topic else []
    id_list = request.POST.getlist('checkboxes')
    selected = []
    if len(id_list) == 1:
        sessions = Session.objects.all()
        for session in sessions:
            if session.type == 1:
                for id in id_list:
                    if len(selected) < 1:
                        selected.append(topics.get(pk=id)) 
                        print("success", selected, participant.id, session.id)

    elif len(id_list) < 1:
        print("Please select an option")

    elif len(id_list) > 1:
        print("Please only select one option")

    else:
        print(id_list)
        
    print("one hit")
    return redirect("user_profile")

@login_required
def two(request):
    participant = Participant.objects.filter(user=request.user).first()
    topics = Topic.objects.all() if Topic else []
    id_list = request.POST.getlist('checkboxes')
    selected = []
    if len(id_list) == 1:
        sessions = Session.objects.all()
        for session in sessions:
            if session.type == 1:
                for id in id_list:
                    if len(selected) < 1:
                        selected.append(topics.get(pk=id)) 
                        print("success", selected, participant.id)

    elif len(id_list) < 1:
        print("Please select an option")

    elif len(id_list) > 1:
        print("Please select one option")

    else:
        print(id_list)
        
    print("two hit")
    return redirect("user_profile")

@login_required
def three(request):
    participant = Participant.objects.filter(user=request.user).first()
    topics = Topic.objects.all() if Topic else []
    id_list = request.POST.getlist('checkboxes')
    selected = []
    if len(id_list) == 1:
        sessions = Session.objects.all()
        for session in sessions:
            if session.type == 1:
                for id in id_list:
                    if len(selected) < 1:
                        selected.append(topics.get(pk=id)) 
                        print("success", selected, participant.id)

    elif len(id_list) < 1:
        print("Please select an option")

    elif len(id_list) > 1:
        print("Please select one option")

    else:
        print(id_list)

    print("three hit")
    return redirect("user_profile")

@login_required
def four(request):
    participant = Participant.objects.filter(user=request.user).first()
    topics = Topic.objects.all() if Topic else []
    id_list = request.POST.getlist('checkboxes')
    selected = []
    if len(id_list) == 1:
        sessions = Session.objects.all()
        for session in sessions:
            if session.type == 1:
                for id in id_list:
                    if len(selected) < 1:
                        selected.append(topics.get(pk=id)) 
                        print("success", selected, participant.id)

    elif len(id_list) < 1:
        print("Please select an option")

    elif len(id_list) > 1:
        print("Please select one option")

    else:
        print(id_list)

    return redirect("user_profile")
