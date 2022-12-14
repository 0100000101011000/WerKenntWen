from .models import CustomUser, Conections
from django.contrib.auth.hashers import make_password
import re
from postman.models import Message
from django.utils import timezone
from django.db.models import Q


def createUser(request):


  first_name = request.POST.get('first_name')
  last_name = request.POST.get('last_name')
  email = request.POST.get('email')
  password = request.POST.get('password1')
  pswrd_repeat = request.POST.get('password2')
  gender = request.POST.get('switch')
  age = request.POST.get('birthYear')
  agb = request.POST.get('agb')
  fail_collection = [0,0,0,0,0,0,0,0,0]
  failed = False

  if len(first_name) == 0:
    fail_collection[0] = 1
    failed = True
  if len(last_name) == 0:
    fail_collection[1] = 1
    failed = True
  if gender == None:
    fail_collection[2] = 1
    failed = True
  if check(email) == 'bad':
    fail_collection[3] = 1
    failed = True
  if check(email) == 'used':
    fail_collection[4] = 1
    failed = True
  if len(password) < 6:
    fail_collection[5] = 1
    failed = True
  if pswrd_repeat != password:
    fail_collection[6] = 1
    failed = True
  if age == 'value':
    fail_collection[7] = 1
    failed = True
  if agb != 'accepted':
    fail_collection[8] = 1
    failed = True

  if not failed:

    password = make_password(password)
    email = email.lower()

    try:
      avatar = request.FILES['upload']

    except:
      avatar = 'maleProfilePicture.png'
      if gender == 'F':
        avatar = 'femaleProfilePicture.png'

    user = CustomUser.objects.create(last_name=last_name, first_name=first_name,
                                     email=email, password=password, age=age, gender=gender, avatar=avatar)

    return user
  
  return fail_collection


def check(email):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (re.fullmatch(regex, email)):
      if len(CustomUser.objects.filter(email=email)) == 0:
        return 'okay'

      return 'used'

    return 'bad'


def sendMessage(sender, receiver, message, subject):
    newMessage = Message.objects.create(
        sender_id=sender, recipient_id=receiver, body=message, subject=subject)


def set_last_request(user):
  user.last_online = timezone.now()
  user.save()


def is_user_online(user):
  try:
    if (timezone.now() - user.last_online) < timezone.timedelta(minutes=5):
      return True
    return False
  except:
    return False


def conaction_chain(user1,user2):

  middlemans = None
  middlemans_id = []
  conection_chain = False

  if Conections.get_conection(p1_id=user1.id, p2_id=user2.id):
    middlemans = False

  else:

      your_frendchips = Conections.get_conection(p1_id=user2.id,bool=False)

      if len(your_frendchips) > 0:

          my_frendchips = Conections.get_conection(p1_id=user1.id,bool=False)           
          if len(my_frendchips) > 0:

              my_frend_id_list = []

              for my_frendchip in my_frendchips:
                  if my_frendchip.person_one_id == str(user1.id):
                      my_frend_id = my_frendchip.person_two_id
                  else:
                      my_frend_id = my_frendchip.person_one_id

                  my_frend_id_list.append(my_frend_id)                                      
                  if Conections.get_conection(p1_id=my_frend_id,list=your_frendchips):
                      conection_chain = True
                      break

              if conection_chain:
                  middlemans_id.append(my_frend_id) 

              else:

                  for my_frend_id in my_frend_id_list:

                      for your_frendchip in your_frendchips:
                          if your_frendchip.person_one_id == str(user2.id):
                              your_frend_id = your_frendchip.person_two_id
                          else:
                              your_frend_id = your_frendchip.person_one_id

                          if Conections.get_conection(p1_id=my_frend_id,p2_id=your_frend_id):
                              middlemans_id = [my_frend_id,your_frend_id]
                              break
                          

                      if len(middlemans_id) > 0:
                          break

  if len(middlemans_id) > 0:
      middlemans = []
      for middleman_id in middlemans_id:
          middlemans.append(CustomUser.objects.get(id=middleman_id))

  return middlemans

def know_proposel(user):
  
    users = []
    already_asked = Conections.objects.filter(person_one_id=user.id)

    other_users = CustomUser.objects.filter(~Q(id=user.id))
    other_users = other_users.filter(is_superuser=False)
    for asked_user in already_asked:
        other_users = other_users.filter(~Q(id=asked_user.person_two_id))
    no_conections = []

    for other_user in other_users:
        middlemans = conaction_chain(user,other_user)
        if middlemans != False:
            if middlemans == None:
                no_conections.append(other_user)
            elif len(middlemans) == 1:
                users.insert(0,other_user)
            elif len(middlemans) == 2:
                users.append(other_user)
    
    users += no_conections

    return users

def get_user_frends(user_id,just_id=False):
  frends = []
  connections = Conections.objects.filter(Q(person_one_id=user_id,accepted=True)|Q(person_two_id=user_id,accepted=True))

  for con in connections:
    if con.person_one_id == str(user_id):
      frend_id = con.person_two_id
    else:
      frend_id = con.person_one_id

    

    frend = CustomUser.objects.get(id=frend_id)
    if just_id:
      frend = frend.id
    frends.append(frend)

  return frends

def get_asked_users(user_id,just_id=False):
  asked = []
  all_reqs = Conections.objects.filter(Q(person_one_id=user_id))

  for req in all_reqs:
   
    requested_id = req.person_two_id
  
    requested = CustomUser.objects.get(id=requested_id)
    if just_id:
      requested = requested.id
    asked.append(requested)

  return asked