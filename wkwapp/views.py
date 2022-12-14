from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Conections
from postman.models import Message
from django.http import HttpResponse
from django.db.models import Q
from . import myFunc

errormessage = 'Falsche E-Mail oder Passwort'


################################## A S K ####################################
def askUser(request):

    user = request.POST['requester']
    requested = request.POST['requested']

    try:
        request_from_requested_user = Conections.objects.get(person_one_id=requested,person_two_id=user)
        request_from_requested_user.accepted = True
        request_from_requested_user.save()
    except:
        Conections.objects.create(person_one_id=user, person_two_id=requested)

    return HttpResponse('Anfrage abgesendet')


############################ A C C E P T ###############################
def acceptUser(request):

    user = request.POST['requested']
    requester = request.POST['requester']

    to_accept = Conections.objects.get(
        person_two_id=user, person_one_id=requester)
    to_accept.accepted = True
    to_accept.save()
    return HttpResponse('Anfrage akzeptiert')


############################## E V E R Y O N E ###############################
# Stellt sicher dass der Benutzer noch eingeloggt ist
@login_required(login_url='index')
def everyone(request):
    user = request.user

    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    users = myFunc.know_proposel(user)
        

    context = {'users': users, 'user': user}

    return render(request, 'wkwapp/everyone.html', context)


######################## K _ R E Q U E S T S ###############################
# Stellt sicher dass der Benutzer noch eingeloggt ist
@login_required(login_url='index')
def know_requests(request):
    user = request.user
    users = []
    population = 0

    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    requests = Conections.objects.filter(person_two_id=user.id, accepted=False)

    if not requests:
        return home(request)

    for know_request in requests:
        requester_id = know_request.person_one_id
        users.append(CustomUser.objects.get(id=requester_id))
        population += 1

    context = {'users': users, 'user': user, 'population': population}

    return render(request, 'wkwapp/know_requests.html', context)


################################# K N O W ###################################
# Stellt sicher dass der Benutzer noch eingeloggt ist
@login_required(login_url='index')
def know(request):
    user = request.user
    frends = []
    
  

    frends = myFunc.get_user_frends(user.id)

    no_one = len(frends) == 0

    context = {'frends': frends, 'user': user, 'no_one': no_one}

    return render(request, 'wkwapp/know.html', context)


################################ S E N D ##################################
@login_required(login_url='index')
def send_message(request, id):
    user = request.user
    receiver = CustomUser.objects.get(id=id)
    tosend = request.POST.get('tosend')
    subject = request.POST.get('subject')

    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    if type(subject) != str:
        subject = ' '
    if type(tosend) == str:
        if len(tosend) > 0:
            myFunc.sendMessage(
                sender=user.id, receiver=receiver.id, message=tosend, subject=subject)
            messages.error(request, type(tosend))
        # return redirect('home')
    context = {'user': user, 'receiver': receiver}

    return render(request, 'wkwapp/send_message.html', context)


################################## M E ####################################
@login_required(login_url='index')
def me(request):
    user = request.user 
    frends = myFunc.get_user_frends(user.id)

    frends_amount = len(frends)

    if frends_amount > 6:
        limited_frends = frends[0:6]
    else:
        limited_frends = frends

    context = {'user': user, 'limited_frends':limited_frends, 'frends_amount':frends_amount}

    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    return render(request, 'wkwapp/me.html', context)


############################### V I S I T ##################################
@login_required(login_url='index')
def visitedUser(request, id):

    user = request.user
    visitedUser = CustomUser.objects.get(id=id)

    if user.id == visitedUser.id:
        return me(request)

    already_asked = len(Conections.objects.filter(person_one_id=user.id,person_two_id=visitedUser.id, accepted=False)) > 0
    
    vU_frends = myFunc.get_user_frends(visitedUser.id)
    vU_frends_amount = len(vU_frends)

    if vU_frends_amount > 6:
        limited_frends = vU_frends[0:6]
    else:
        limited_frends = vU_frends
        
    middlemans = myFunc.conaction_chain(user,visitedUser) # Sucht Freundschaftsverbindungen
    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    context = {
        'visitedUser': visitedUser,
        'user': user,
        'middlemans': middlemans,
        'vU_frends_amount':vU_frends_amount,
        'limited_frends':limited_frends,
        'vU_frends':vU_frends,
        'already_asked':already_asked
        }

    return render(request, 'wkwapp/visitedUser.html', context)



############################### V I S I T E D _ K N O W S ##################################
@login_required(login_url='index')
def visitedUser_knows(request, id):

    user = request.user
    visitedUser = CustomUser.objects.get(id=id)

    

    vU_frends = myFunc.get_user_frends(visitedUser.id)
    vU_frends_amount = len(vU_frends)
       
    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    context = {
        'visitedUser': visitedUser,
        'user': user,
        'vU_frends_amount':vU_frends_amount,
        'vU_frends':vU_frends,
        }

    return render(request, 'wkwapp/visitedUser_knows.html', context)


############################ M E S S A G E S ################################
@login_required(login_url='index')
def messagesPage(request, id, action):

    user = request.user

    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    # action = 1(Öffnen) oder 2(Antworten) oder 3(Löschen) der Nachricht
    if action == 3:
        todelete = Message.objects.get(id=id)
        todelete.delete()
    user = request.user
    post = []
    received = []

    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    # Durchsucht die Postman-Datenbank nach Nachrichten für den eingeloggten Benutzer

    messages = Message.objects.filter(recipient_id=user.id)
    for i in messages:
        sender = CustomUser.objects.get(id=i.sender_id)
        sender = sender.first_name + ' ' + sender.last_name
        post.append(sender)
        received.append(i)

    postlen = len(post)

    context = {
        'user': user,
        'post': post,
        'postlen': postlen,
        'received': received
    }
    return render(request, 'wkwapp/messagesPage.html', context)


################################ R E A D ####################################
@login_required(login_url='index')
def read_message(request, id, action):

    user = request.user

    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    if action == 3:
        todelete = Message.objects.get(id=id)
        todelete.delete()
    toread = Message.objects.get(id=id).body
    context = {'toread': toread}
    return render(request, 'wkwapp/read_message.html', context)


################################ H O M E ####################################
@login_required(login_url='index')
def home(request):
    user = request.user
    online_users_amount = 0
    online_users = []

    myFunc.set_last_request(user)  # Spechert den Zeitpunkt der Abfrage

    users = myFunc.know_proposel(user) # Vielleicht kennst du

    for i in CustomUser.objects.filter(~Q(id=user.id)): # Wer ist online

        if myFunc.is_user_online(i):
            online_users.append(i)
            online_users_amount += 1

    requests = Conections.objects.filter(person_two_id=user.id, accepted=False)
    len_requests = len(requests)
    requester = None
    if len_requests > 0:
        requester_id = int(requests[0].person_one_id)
        requester = CustomUser.objects.get(id=requester_id)

    userLen = len(users)
    context = {
        'user': user,
        'users': users,
        'userLen': userLen,
        'requester': requester,
        'len_requests': len_requests,
        'online_users_amount': online_users_amount,
        'online_users': online_users
    }

    return render(request, 'wkwapp/home.html', context)


################################ S E A R C H _ U S E R ####################################
@login_required(login_url='index')
def search_user(request):

    user = request.user
    found_users = []
    search_input = request.POST.get('search_field')
    frends = myFunc.get_user_frends(user.id,just_id=True)
    requested = myFunc.get_asked_users(user.id,just_id=True)

    if type(search_input) == str:
        search_list = search_input.split()

        if len(search_input) > 0:        

            if len(search_list) > 1:
                for i in range(len(search_list)-1):
                    look_for_users = CustomUser.objects.filter(first_name__icontains=search_list[i], last_name__icontains=search_list[i+1])
                    for found_user in look_for_users:
                        found_users.append(found_user)

            for name in search_list:
        
                look_for_users = CustomUser.objects.filter(Q(first_name__icontains=name)|Q(last_name__icontains=name))
                for found_user in look_for_users:
                    if found_user not in found_users:
                        found_users.append(found_user)

        else:
            return everyone(request)
    
    else:
        return everyone(request)
        


    context = {'user':user, 'search_input':search_input,'found_users':found_users,'frends':frends,'requested':requested}
   
    return render(request, 'wkwapp/search_user.html', context)




################################ I N D E X ####################################
def index(request):
    logout(request)
    first_name = request.POST.get('first_name')
    usermail = request.POST.get('usermail')
    fails = []

    if type(usermail) == str:
        usermail = usermail.lower()
        userpswrd = request.POST.get('userpswrd')

        if userLogin(request, usermail, userpswrd):
            return redirect('home')
        messages.error(request, errormessage)

    elif type(first_name) == str:
        user = myFunc.createUser(request)
        if type(user) != list:
            login(request, user)
            return redirect('home')
        else:
            fails = user
    
    context = {'fails' : fails}

    return render(request, 'wkwapp/index.html', context)


################################ L O G I N ####################################
def userLogin(request, usermail, userpswrd):

    user = authenticate(request, email=usermail, password=userpswrd)

    if user is not None:
        login(request, user)
        return True
