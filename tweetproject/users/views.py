from django.shortcuts import render ,redirect
from django.shortcuts import HttpResponse
from .forms import ProfileUpdateForm,UserUpdateForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def profile_update(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST, instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            profile_form.save()
            update_session_auth_hash(request,user) #this will keep the current user logged in
            return redirect('tweet_list')

    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.profile)
    
    return render(request,"registration/profile.html",{'user_form':user_form,"profile_form":profile_form})