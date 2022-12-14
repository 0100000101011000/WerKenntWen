from random import randint

def emailGen():

  sinces = 'abcdefghijklmnopqrstuvwxyz1234567890'
  providers = ['@web.de','@gmail.com','@gmx.com','@yahoo.com','@t-online.de']
  

  while True:
    x = input('Generieren')
    if type(x) == str:
      maillen = randint(6,15)
      email = ''
      for i in range(maillen):
        ranlet = sinces[randint(0, len(sinces)-1)]
        email += ranlet
      email += providers[randint(0,4)]
      print(email)



emailGen() 