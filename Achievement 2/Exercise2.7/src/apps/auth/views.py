from django.shortcuts import render, redirect          
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm    
from django.contrib.auth.decorators import login_required


def login_view(request):
    error_message = None   
    form = AuthenticationForm()                            

    if request.method == 'POST':       
        #read the data sent by the form via POST request                   
        form = AuthenticationForm(data=request.POST)

        #check if form is valid
        if form.is_valid():                                
            username=form.cleaned_data.get('username')      #read username
            password = form.cleaned_data.get('password')    #read password

            #use Django authenticate function to validate the user
            user=authenticate(username=username, password=password)

            if user is not None:
                login(request, user)                
                return redirect('profile') #& send the user to desired page
       
    #prepare data to send from view to template
    context ={                                             
        'form': form,                                 #send the form data
        'error_message': form.errors.get('__all__')                #and the error_message
    }

    #load the login page using "context" information
    return render(request, 'login.html', context)    

@login_required
def profile_view(request):
    return render(request, 'user_profile.html')  

def logout_view(request):                                  
    logout(request)             
    return redirect('logout_success')  

def logout_success_view(request):
    return render(request, 'success.html')