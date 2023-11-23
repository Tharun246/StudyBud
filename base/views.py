from django.shortcuts import render,redirect
from .forms import RoomForm,UserForm
from .models import Room,Message,topic as Topic
from django.db.models import Q
from django.contrib.auth.models import auth,User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
# Create your views here.


def home(request): 
    q=request.GET.get('q') if request.GET.get('q') !=None  else ''
    rooms=Room.objects.filter  (
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)| 
        Q(description__icontains=q)
    )
    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()

    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={
    'rooms':rooms,'topics':topics,'room_count':room_count,
    'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk): 
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method=='POST': 
        message=Message.objects.create(user=request.user,
        body=request.POST.get('q'),
        room=room)
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
        

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context) 


def userprofile(request,pk):
    user=User.objects.get(id=pk) 
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url="login/")
def createRoom(request): 
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST': 
        topic_name=request.POST.get('topic')
        topic,created =Topic.objects.get_or_create(name=topic_name)
       
        Room.objects.create(
        host=request.user,
        topic=topic,
        name=request.POST.get('name'),
        description=request.POST.get('description')
       )
       
        # form=RoomForm(request.POST)
        # if form.is_valid: 
        #     room= form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect('home')

    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url="login/")
def UpdateRoom(request,pk): 

    room=Room.objects.get(id=pk)
    topics=Topic.objects.all()
    form=RoomForm(instance=room)

    if request.user !=room.host: 
        return HttpResponse("you are not allowed here")

    if request.method=='POST': 
        topic_name=request.POST.get('topic')
        topic,created =Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url="login/")
def delRoom(request,pk): 
    room=Room.objects.get(id=pk)

    if request.method=='POST': 
        room.delete()
        return redirect('home')

    return render(request,'base/delete.html',{'obj':room})


def loginpage(request): 
    page='login'

    if request.user.is_authenticated: 
        return redirect('home')

    if request.method=='POST': 
        username=request.POST.get('uname','').lower()
        password=request.POST.get('pwd','')
        user=auth.authenticate(request,username=username,password=password)

        if user: 
            auth.login(request,user)
            messages.success(request,'Login is successful')
            return redirect('home')
        else: 
            messages.error(request,'User credentials doesnt match')
            return redirect('login')
        
    context={'page':page}
    return render(request,'base/login_register.html',context)
    
def logoutuser(request):

    auth.logout(request)
    return redirect('home')


def registeruser(request): 
    form=UserCreationForm()

    if request.method=='POST': 
        
        form=UserCreationForm(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request,"registration is successful")
            return redirect('login')
        else: 
            messages.error(request,"detaila are inaccurate ")
            #return redirect("/")
    context={'form':form}
    return render(request,'base/login_register.html',context)

@login_required(login_url='login/')
def delmessage(request,pk): 

    message=Message.objects.get(id=pk)

    if request.user != message.user: 
        return HttpResponse("you are not allowed !!")

    if request.method =='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})

@login_required(login_url='login')
def updateuser(request): 
    user=request.user
    form=UserForm(instance=user)

    if request.method=='POST': 
        form=UserForm(request.POST,instance=user)
        if form.is_valid(): 
            form.save()
            return redirect('user-profile',pk=user.id)
    context={'form':form}
    return render(request,'base/update-user.html',context)

def topicspage(request): 
    q=request.GET.get('q') if request.GET.get('q') !=None  else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(request,'base/topics.html',context)

def activitypage(request): 
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(request,'base/activity.html',context)