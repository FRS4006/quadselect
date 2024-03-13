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
    sessions = Session.objects.all()
    user_courses = participant.courses.all() if participant else []
    user_ps = ParticipantSession.objects.all() if participant else []
    selected_topics = []
    postable_topics = []
    if request.method == 'GET':
        for session in sessions:
            if session.topics != None:
                for sessiontopic in session.topics.all():
                    selected = topics.filter(pk=sessiontopic.id)
                    selected_topics.append(selected.first().id)
        for topic in topics:
            if topic.id in set(selected_topics):
                print(topic.id)
            else:
                postable_topics.append(topic)
            for ps in user_ps:
                if ps.topic != None:
                    selected_take_2 = topics.filter(name=ps.topic)
                    if selected_take_2.first() in postable_topics:
                        postable_topics.remove(selected_take_2.first())
                    else:
                        print(postable_topics)
    return render(request, 'interactor.html', {'user_courses': user_courses, 'topics': postable_topics, 'topicsselected':user_ps, 'selectedtopics':selected_topics})

@login_required
def one(request):
    participant = Participant.objects.filter(user=request.user).first()
    topics = Topic.objects.all() if Topic else []
    user_courses = participant.courses.all() if participant else []
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
                                    topic = Topic.objects.get(pk = id_list[0]),
                                    completed = False,
                                )
                                ps.save()
                                # save the first participant session
                                print(id_list)
                                return redirect(user_profile)
                                # return the extended page again, so that the 4 columns are reloaded
                    else:
                        # if there are participant sessions already
                        filtered_ps_session = ParticipantSession.objects.filter(session=session.id).first()
                        # filtered_ps_session is equal to the first Participant session where the session id number matches the session.id
                        filtered_ps_topic = ParticipantSession.objects.filter(topic=id_list[0]).first()
                        if filtered_ps_session != None:
                            # if the filtered participant sessions contain a session that matches the current one, print the name of it
                            if len(list(user_ps)) == 4:
                                print("user_ps has 4 elements, attempting to add", id_list)
                                user_ps = ParticipantSession.objects.filter(participant=participant) if participant else []
                                return redirect(user_profile)
                            else:
                                print(filtered_ps_session)
                        else:
                            # if the filtered participant sessions does not contain the session number
                            if filtered_ps_topic != None:
                            # if the filtered topic doesnt exist
                                print(filtered_ps_topic)
                                user_ps = ParticipantSession.objects.filter(participant=participant) if participant else []
                                return redirect(user_profile)
                            else:
                                form = ParticipantSessionForm(request.POST)
                                # set the form
                                if form.is_valid():
                                    cd = form.cleaned_data
                                    ps = ParticipantSession(
                                        session = Session.objects.get(pk= session.id),
                                        participant = Participant.objects.get(pk= participant.id),
                                        topic = Topic.objects.get(pk = id_list[0]),
                                        completed = False,
                                    )
                                    ps.save()
                                    # save the form to the database
                                    print("ps doesnt exist yet", id_list, "session topics", session.topics.all(), "session object",session)
                                    user_ps = ParticipantSession.objects.filter(participant=participant) if participant else []
                                    return redirect(user_profile)
                                    # return the extended page again, so that the 4 columns are reloaded
    else:
        # this would not be needed with a dropdown, but is more necessary with a selection list
        print("id list not one", id_list)
        return redirect(user_profile)

@login_required
def deleteallps(request):
    participant = Participant.objects.filter(user=request.user).first()
    user_ps = ParticipantSession.objects.filter(participant=participant) if participant else []
    user_courses = participant.courses.all() if participant else []
    topics = Topic.objects.all() if Topic else []
    user_ps.delete()
    return redirect(user_profile)
