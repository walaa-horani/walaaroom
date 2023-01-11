from django.shortcuts import render, redirect

from .models import Room,Topic,Message,UserProfile
from .forms import RoomForm, UserForm,User,UserProfileForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

# Create your views here.
def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
       
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages= Message.objects.filter(Q(room__name__icontains=q))
    
    return render(request,'home.html',{'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages})




def room(request,id):
    room = Room.objects.get(id=id)
    room_message = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        messages = Message.objects.create(
            user = request.user,
            room = room,
            body= request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id=room.id)
    return render(request,'room.html',{'room':room,'room_message':room_message,'participants':participants})    


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
           room=  form.save(commit=False)
           room.host = request.user
           room.save()
           return redirect('home')


    return render(request,'room_form.html',{'form':form})    

@login_required(login_url='login')
def updateRoom(request,id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('your are not allowed here')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request,'room_form.html',{'form':form})    


def deleteRoom(request,id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse('your are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':room})    


def deleteMessage(request,id):
    message = Message.objects.get(id=id)
    if request.method == 'POST':
        if message.user == request.user:
         message.delete()
         return redirect('home')
        else:
           return HttpResponse('your are not allowed here')

    return render(request,'delete_message.html')        



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'user dose not exist')

        user = authenticate(request,username=username,password=password)    


        if user is not None:
            login(request,user)
            return redirect('home')




    return render(request,'login_register.html',{'page':page})    


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'an error has occurred')
    return render(request,'login_register.html',{'form':form})    




def userProfile(request,id):
    user= User.objects.get(id=id)
    rooms=user.room_set.all()
    user_messages = user.message_set.all()
    topics= Topic.objects.all()
    
    return render(request,'profile.html',{'user':user,'rooms':rooms,'user_messages':user_messages,'topics':topics})    



@login_required(login_url='login')
def updateUser(request):
    userProfile = request.user.userprofile
    user = request.user
    form = UserForm(instance=user)
    form_user = UserProfileForm(instance=userProfile)

    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        form_user = UserProfileForm(request.POST,request.FILES,instance=userProfile,)

        if form.is_valid():
            form.save()
        if form_user.is_valid:  
            form_user.save()  
            return redirect('userprofile', id=user.id)





    return render(request,'update-user.html',{'form':form,'form_user':form_user})


class CreateProfilePageView(CreateView):
    model = UserProfile
    template_name = 'create-user.html'
    form_class = UserProfileForm
   


    def form_valid(self, form):
        form.instance.user= self.request.user
        return super().form_valid(form)

     
