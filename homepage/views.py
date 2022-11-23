from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User , auth, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . templates import decorators
import datetime
import numpy as np
import os

# Create your views here.
def homepage(requests):
    return render(requests,'homepage.html')

def getPredictions(sample):
    import pickle
    model = pickle.load(open(os.getcwd()+'/football_model.sav', "rb"))
    prediction = model.predict(np.array(sample).reshape(1, -1))
    
    if prediction == 'A':
        return 'AWAY WINS'
    elif prediction == 'H':
        return "HOME WINS"
    else:
        return "DRAW"

@login_required(login_url='/login')
def predict(requests):
    teams=['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford','Brighton',
    'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Leeds',
    'Leicester', 'Liverpool', 'Man City', 'Man United', 'Newcastle',
    'Norwich', 'Sheffield United', 'Southampton', 'Tottenham', 'Watford',
    'West Brom', 'West Ham', 'Wolves']
    if requests.method=='POST':
        b365h=requests.POST['b365h']
        b365a=requests.POST['b365a']
        b365d=requests.POST['b365d']
        b365o25=requests.POST['b365o25']
        b365u25=requests.POST['b365u25']

        team_={}

        for team in teams:
            if requests.POST['teamh']==team:
                team_[team+'h']=1
            else:
                team_[team+'h']=0

        for team in teams:
            if requests.POST['teama']==team:
                team_[team+'a']=1
            else:
                team_[team+'a']=0

        df=[b365h,b365a,b365d,b365o25,b365u25]+list(team_.values())
        res=getPredictions(df)
        if res=='HOME WINS':
            rteam=requests.POST['teamh']
        elif res=='AWAY WINS':
            rteam=requests.POST['teama']
        else:
            rteam='NO WINNER'
        return render(requests, 'prediction_result.html',{'result':res,'team':rteam})

    else:
        return render(requests, 'prediction.html',{'teams':teams})

def nav(requests):
    if requests.method=='POST':
        if requests.POST['options']=='2':
            return redirect('/predict')
        elif requests.POST['options']=='1':
            return HttpResponse('only EPL is available at this point in time')
        else:
            return HttpResponse('My name is KING and i believe Messi is the greatest player of all time')
    else:
        return HttpResponse('My name is KING and i believe Messi is the greatest player of all time')

@decorators.unauthenticated_user
def register(requests):
    if requests.method == 'POST':
        username=requests.POST['username']
        first_name=requests.POST['first name']
        last_name=requests.POST['last name']
        email=requests.POST['email']
        password1=requests.POST['password1']
        password2=requests.POST['password2']

        if password1 != password2:
            return render(requests,'register.html',{'print':'password mismatch'})
        else:
            if (User.objects.filter(email=email).exists()==False) & (User.objects.filter(username=username).exists()==False):
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
                user.save();
                print('crated')
                #group=Group.objects.get(name='student')
                #user.groups.add(group)
                messages.success(requests ,'succesfully created an account')
                return redirect('/login',)
            else:
                return render(requests,'register.html', {'print':'username or email already exists'})


    else:
        return render(requests,'register.html')


@decorators.unauthenticated_user
def login(requests):
    if requests.method=='POST':
        username=requests.POST['username']
        password=requests.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(requests,user)
            messages.success(requests ,'welcome'+username)
            return redirect('/')
        else:
            messages.info(requests, 'username or password is incorrect')
            return render (requests, 'login.html')
    else:
        return render (requests, 'login.html')



def logout(requests):
    auth.logout(requests)
    return redirect('/')
