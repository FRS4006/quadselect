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
    # needs to be changed to topics that are not currently attatched to sessions
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
    user_courses = participant.courses.all() if participant else []
    # this will have to change when I am testing with more than one person
    user_topics = participant.topics.all() if participant else []
    # this will have to change when I am testing with more than one person
    id_list = request.POST.getlist('checkboxes')
    user_ps = ParticipantSession.objects.filter(participant=participant) if participant else []
    sessions = Session.objects.all()
    if len(id_list) == 1:
        # if the total selected number is 1 (the first step of checking, the 1 could be any number)
        for id in id_list:
            # For each of the ids contained in that array (in this case it should be just 1)
            for session in sessions:
                # for each session
                if session.type == 1:
                    # if the session is an elective week
                    if user_ps.first() == None:
                        # if there are no participant sessions (this should only be the first time)
                            form = ParticipantSessionForm(request.POST)
                            # set the form
                            if form.is_valid():
                                cd = form.cleaned_data
                                ps = ParticipantSession(
                                    session = Session.objects.get(pk= session.id),
                                    participant = Participant.objects.get(pk= participant.id),
                                    completed = False,
                                )
                                ps.save()
                                # save the first participant session
                                return render(request, 'interactor.html', {'user_courses': user_courses,'user_topics': user_topics, 'topics': topics, 'topicsselected':user_ps})
                                # return the extended page again, so that the 4 columns are reloaded
                    else:
                        # if there are participant sessions already
                        filtered_ps = ParticipantSession.objects.filter(session=session.id).first()
                        # filtered is equal to the first Participant session where the session id number matches the session.id
                        if filtered_ps != None:
                            # if the filtered participant sessions contain a session that matches the current one, print the name of it
                            print(filtered_ps)
                        else:
                            # if the filtered participant sessions does not contain the session number
                            form = ParticipantSessionForm(request.POST)
                            # set the form
                            if form.is_valid():
                                cd = form.cleaned_data
                                ps = ParticipantSession(
                                    session = Session.objects.get(pk= session.id),
                                    participant = Participant.objects.get(pk= participant.id),
                                    completed = False,
                                )
                                ps.save()
                                # save the form to the database
                                print(ps, 'valid', user_ps)
                                return render(request, 'interactor.html', {'user_courses': user_courses,'user_topics': user_topics, 'topics': topics, 'topicsselected':user_ps})
                                # return the extended page again, so that the 4 columns are reloaded
    else:
        print(id_list)
    return redirect("user_profile")

















# @login_required
# def two(request):
#     participant = Participant.objects.filter(user=request.user).first()
#     topics = Topic.objects.all() if Topic else []
#     id_list = request.POST.getlist('checkboxes')
#     selected = []
#     if len(id_list) == 1:
#         sessions = Session.objects.all()
#         for session in sessions:
#             if session.type == 1:
#                 for id in id_list:
#                     if len(selected) < 1:
#                         selected.append(topics.get(pk=id)) 
#                         print("success", selected, participant.id, session.id)
#                         form = ParticipantSessionForm(request.POST)
#                         if form.is_valid():
#                             cd = form.cleaned_data
#                             ps = ParticipantSession(
#                                 session = Session.objects.get(pk= session.id),
#                                 participant = Participant.objects.get(pk= participant.id),
#                                 completed = False,
#                             )
#                             print('form is valid')
#                             if len(list(user_ps)) < 2:
#                                 # ps.save()
#                                 print(ps, 'valid')
#                                 return render(request, 'interactor.html', {'user_courses': user_courses,'user_topics': user_topics, 'topics': topics, 'topicsselected':selected})
                            
#                             else:
#                                 print('not valid')

#     elif len(id_list) < 1:
#         print("Please select an option")

#     elif len(id_list) > 1:
#         print("Please select one option")

#     else:
#         print(id_list)
        
#     print("two hit")
#     return redirect("user_profile")

# @login_required
# def three(request):
#     participant = Participant.objects.filter(user=request.user).first()
#     topics = Topic.objects.all() if Topic else []
#     id_list = request.POST.getlist('checkboxes')
#     selected = []
#     if len(id_list) == 1:
#         sessions = Session.objects.all()
#         for session in sessions:
#             if session.type == 1:
#                 for id in id_list:
#                     if len(selected) < 1:
#                         selected.append(topics.get(pk=id)) 
#                         print("success", selected, participant.id, session.id)
#                         form = ParticipantSessionForm(request.POST)
#                         if form.is_valid():
#                             cd = form.cleaned_data
#                             ps = ParticipantSession(
#                                 session = Session.objects.get(pk= session.id),
#                                 participant = Participant.objects.get(pk= participant.id),
#                                 completed = False,
#                             )
#                             print('form is valid')
#                             if len(list(user_ps)) < 2:
#                                 # ps.save()
#                                 print(ps, 'valid')
#                                 return render(request, 'interactor.html', {'user_courses': user_courses,'user_topics': user_topics, 'topics': topics, 'topicsselected':selected})
                            
#                             else:
#                                 print('not valid')

#     elif len(id_list) < 1:
#         print("Please select an option")

#     elif len(id_list) > 1:
#         print("Please select one option")

#     else:
#         print(id_list)

#     print("three hit")
#     return redirect("user_profile")

# @login_required
# def four(request):
#     participant = Participant.objects.filter(user=request.user).first()
#     topics = Topic.objects.all() if Topic else []
#     id_list = request.POST.getlist('checkboxes')
#     selected = []
#     if len(id_list) == 1:
#         sessions = Session.objects.all()
#         for session in sessions:
#             if session.type == 1:
#                 for id in id_list:
#                     if len(selected) < 1:
#                         selected.append(topics.get(pk=id)) 
#                         print("success", selected, participant.id, session.id)
#                         form = ParticipantSessionForm(request.POST)
#                         if form.is_valid():
#                             cd = form.cleaned_data
#                             ps = ParticipantSession(
#                                 session = Session.objects.get(pk= session.id),
#                                 participant = Participant.objects.get(pk= participant.id),
#                                 completed = False,
#                             )
#                             print('form is valid')
#                             if len(list(user_ps)) < 2:
#                                 # ps.save()
#                                 print(ps, 'valid')
#                                 return render(request, 'interactor.html', {'user_courses': user_courses,'user_topics': user_topics, 'topics': topics, 'topicsselected':selected})
                            
#                             else:
#                                 print('not valid')

#     elif len(id_list) < 1:
#         print("Please select an option")

#     elif len(id_list) > 1:
#         print("Please select one option")

#     else:
#         print(id_list)

#     return redirect("user_profile")
