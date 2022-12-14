from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models import Q



# Create your models here.


class Gender():
  CHOICES = (
    ('M', 'Männlich'),
    ('F', 'Weiblich')
  )

class Age():

  def createYears():
      years = ()
      currentYear = datetime.datetime.now().year
      for i in range(1900, currentYear+1):
        year = (str(i), str(i))
        years = (*years, year)
      return years
  
  CHOICES = createYears()
 

class CustomUser(AbstractUser):
  first_name = models.CharField(max_length=50, null =True)
  last_name = models.CharField(max_length=100, null =True)
  email = models.EmailField(unique=True)
  gender = models.CharField(max_length=1, choices=Gender.CHOICES, default='M')
  age = models.CharField(max_length=4, choices=Age.CHOICES, default=16)
  avatar = models.ImageField(null=True, default='maleProfilePicture.png')
  last_online = models.DateTimeField(blank=True, null=True) 
  username = None
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []


class Conections(models.Model):

  person_one_id = models.CharField(max_length=3, null=True)
  person_two_id = models.CharField(max_length=3, null=True)
  accepted = models.BooleanField(default=False)

  def get_conection(p1_id, p2_id=None, list=None, bool=True):
    if p2_id == None:
      if list == None:
        conection = Conections.objects.filter(Q(person_one_id=p1_id,accepted=True)|Q(person_two_id=p1_id,accepted=True))
      else:
        conection = list.filter(Q(person_one_id=p1_id,accepted=True)|Q(person_two_id=p1_id,accepted=True))
    else:
      if list == None:
        conection = Conections.objects.filter(Q(person_one_id=p1_id,person_two_id=p2_id,accepted=True)|Q(person_one_id=p2_id,person_two_id=p1_id,accepted=True))
      else:
        conection = list.filter(Q(person_one_id=p1_id,person_two_id=p2_id,accepted=True)|Q(person_one_id=p2_id,person_two_id=p1_id,accepted=True))
      if bool:
        conection = len(conection) > 0
  
    return conection

# class Blog_entry(models.Model):
#   owner = models.ForeignKey(CustomUser)
#   poster = models.ForeignKey(CustomUser)
#   entry = models.TextField(max_length=10000, null=True)

