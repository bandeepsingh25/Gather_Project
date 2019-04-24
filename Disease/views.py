import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from disease.forms import DForm
from twilio.rest import Client
from twilio.twiml.messaging_response import  MessagingResponse,Message
from django.views.decorators.csrf import csrf_exempt
from djongo.database import connect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from collections import Counter
from disease.data import get_country
from disease.messages import response


# Create your views here.
def home(request):
    if request.method == 'GET':
        return render( request, "home.html" ,context={'auth':request.user})
    elif request.method == 'POST':
        value = request.POST
        if value['req'] == 'logout':
            logout(request)
            return redirect('home')
        elif value['req'] == 'login':
            return redirect('login')


def submit(request):
    if request.method == 'POST':
        form = DForm( request.POST )
        if form.is_valid():
            db = connect()
            dis = db['gather-djongo-db']

            dis.disease_datamodel.insert(form.cleaned_data)

            return redirect('thanks')
    else:
        form = DForm()
    return render( request, 'trial.html', {'form': form} )



def thanks(request):
    return render( request, 'thanks.html' )


@csrf_exempt
def sms(request):
    if request.method == 'POST':
        #print(request.POST)

        value = request.POST

        data = value['Body']
        email = value['From']
        country = value['FromCountry']
        zipcode = value['FromZip']
        address = value['FromState'] +' '+ value['FromCity']

        country = get_country(country)

        db = connect()
        dis = db['gather-djongo-db']
        

        mess = MessagingResponse()
        
        mess.message(response(value))

        return HttpResponse(mess)



def loginid(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
    else:
        return render( request, 'login.html' )
    return render(request,'login.html')


def view_data(request):
    """
    if request.user.is_authenticated:
        db = connect()

        dis = db['gather-djongo-db']

        a = dis.disease_datamodel.find()

        a = list(a)
        for i in a:
            i['email'] = "XXX-XXX-"+i['email'][-4:]


        return render(request,'messages.html',context={'message':a})

    else:
        return redirect('login')
    """

    if request.user.is_authenticated:
        db = connect()
        dis = db['gather-djongo-db']
        if request.method == 'POST':
            country_name = request.POST['country_name']
            if country_name == '':
                a = dis.disease_datamodel.find()
            else:

                a= dis.disease_datamodel.find({'country':{'$in':country_name.split(',')}})


        else:
            a=dis.disease_datamodel.find()
        a= list(a)
        cn = Counter()
        for i in a:
            cn[i['country']] += 1

        if request.method == 'GET':
            cn = dict(cn)
            return render(request,'data.html',context={'data':cn},)
        elif request.method == 'POST':

            val = request.POST['cases']
            try:
                int(val)
            except:
                val =0
            cn= dict( [(i, j) for i, j in cn.items() if j > int(val)] )
            return render(request,'data.html',context={'data':cn},)

    else:
        return redirect('login')



def register(request):
    if request.method == 'POST':
        value = request.POST

        username = value['username']
        password = value['password']
        emailId = value['email']
        member = value['member_level']
        try:
            present=User.objects.get(username=username)
        except:
            present = None
        if present is None:
            user = User.objects.create_user(username,emailId,password)
        else:
            return render(request,'signup.html',context={'error':True})

        user.first_name = value['first_name']
        user.last_name = value['last_name']
        user.save()
        client = connect()
        db = client['gather-djongo-db']
        collection = db.auth_user
        collection.update({'username':username},{'$set':{'member':member}})


        return redirect('/')

    else:
        return render(request,'signup.html',context={'error':False})


def chat(request):
    if request.method == 'POST':

        text = request.POST['text']
        return render( request, 'chat.html' ,context={'message':text})
    else:
        return render(request,'chat.html')
