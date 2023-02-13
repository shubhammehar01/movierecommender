from http.client import HTTPResponse
from django.shortcuts import render,redirect
import requests
from copyreg import pickle
import pandas as pd
import pickle as pk
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.Shubham@05
def home(request):
    name = 'India'
    #return render(request,'home.html')
    movie_dict = pk.load(open('movie_dict.pkl','rb'))
    movies = pd.DataFrame(movie_dict)
    result={}

    listname={}
    if request.method=='POST':
        name = request.POST.get('movie_name')
        similar = pk.load(open('similar.pkl','rb'))
        
        data = [] 
        poster =[]  
        def fetch(movie_id):  
            response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1c28161e325733b2cbc131577612f3ee&language=en-US'.format(movie_id))
            data = response.json()
            return 'https://image.tmdb.org/t/p/w500'+ data['poster_path']
            
        #check that it is valid movie name of not
        
        
        a = name in movies['title'].values
        if a==False:
            name='Kingdom of Heaven'

        
        def recommend(movie):
            movie_index = movies[movies['title']==movie].index[0]
            distances = similar[movie_index]
            movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
            
            for i in movies_list:
                movie_id = movies.iloc[i[0]].movie_id
                data.append(movies.iloc[i[0]].title)
                poster.append(fetch(movie_id))
        
        recommend(name)
        if len(data)>4 and len(poster)>4:
            for i in range(len(data)):
                result[data[i]]=poster[i]
    n=movies['title'].values
    #re['name']=name
    fname = 'shubham mehra'
    user = request.user
    if user.is_authenticated:
        fname = user.first_name
    for i in range(len(n)):
        listname[n[i]]=i
    return render(request,'home.html',{'result':result,'listname':listname,'fname':fname})
def index(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html') 
def contact(request):
    return render(request,'contact.html') 

def signin(request):
    
    if request.method == 'POST':
        username=request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username,password=pass1)
        
        if user is not None:
            login(request,user)
            fname = user.first_name
            def forname():
                return fname

            return render(request,'home.html',{'fname':fname})
        else:
            messages.error(request,"bad credentials")
            return redirect('home')
    return render(request,'signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')   
def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        name=request.POST['name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"username already exits please try some others")
            return redirect('home')

        if User.objects.filter(email=email).exists():
           messages.error(request, "Email Already Registered!!")
           return redirect('home')

        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = name
        # myuser.is_active=False
        myuser.save()
        messages.success(request,"your account created successfully")
        
        return render(request,'signin.html')
    return render(request,'signup.html')
