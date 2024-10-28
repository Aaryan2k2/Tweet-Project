from django.shortcuts import render,redirect 
from django.http import HttpResponse
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm,UserUpdateForm,PasswordChangeForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,'index.html')

#to list all tweets
def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

#create tweet
@login_required
def tweet_create(request):
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False) #commit false means form will be saved but will not saved to database  
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})

#tweet edit
@login_required      
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,id=tweet_id,user=request.user)
    if request.method=='POST':  #this is working as The <form> element in your template has the method="post" attribute, which means when the form is submitted, it will send a POST request to the same URL that rendered the form mtlb jis url se get request se hum yha aaye the same url post request dega
         form=TweetForm(request.POST,request.FILES,instance=tweet)
         if form.is_valid():
             tweet=form.save(commit=False)
             tweet.user=request.user #meaning each tweet is associated with a specific user.
             #This assigns the currently logged-in user to the user field of the Tweet instance. Essentially, it links the tweet to the user who created or is editing it.
             tweet.save()
             return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)
    return render(request,"tweet_form.html",{'form':form})

#tweet delete
@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,id=tweet_id,user=request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,"tweet_confirm_delete.html")
 
#For new user registration 
def register(request): #registration ke templates humko project ke bhar vale templates me rakhne hai app ke andr vale templates me nahi kyuki authentication ka kaam django project ka hai
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form=UserRegistrationForm()
    return render(request,"registration/register.html",{'form':form})

#Tweet Search
def searched_tweet(request):
    searched_text=request.GET.get('search_text')
    if searched_text:
        tweets=Tweet.objects.filter(text__icontains=searched_text)
        return render(request,"search_tweet.html",{'tweets':tweets})
    else:
        return redirect('tweet_list')