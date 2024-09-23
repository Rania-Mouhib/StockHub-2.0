from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import MyUser
from outgoing.models import Article as OutgoingItem
from incoming.models import Article as IncomingItem
from django.utils.dateparse import parse_date
import json
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import slugify




@login_required
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            next_url = request.GET.get('next') or 'index'
            return redirect(next_url)
        else:
            error_message = "Invalid username or password."
            return render(request, 'mgmt/login.html', {'error_message': error_message})
    else:
        next_url = request.GET.get('next', '')
        return render(request, 'mgmt/login.html', {'next': next_url})


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required
def profile(request):
    if request.method == "POST":
        user = request.user
        user.name = request.POST.get('name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'mgmt/profile.html')



def superuser_required(user):
    return user.is_authenticated and user.is_superuser


@login_required
def users(request):
    if not request.user.is_superuser:
        return redirect('index')
    return render(request, 'mgmt/users.html')


@login_required
def user_list(request):
    users = MyUser.objects.all()
    user_data = []

    for user in users:
        user_data.append({
            'name': user.name or user.username,
            'username': user.username,
            'is_superuser': user.is_superuser,
            'email': user.email,
            'avatar': user.avatar or 'https://cdn.jsdelivr.net/gh/LahcenEzzara/stockhub-cdn@main/img/avatars/1.png'
        })

    context = {
        'users': user_data
    }
    return render(request, 'mgmt/users.html', context)


@login_required
def user_detail(request, username):
    user = get_object_or_404(MyUser, username=username)
    return render(request, 'mgmt/user_detail.html', {'user': user})



@login_required
def new_user(request):
    if not request.user.is_superuser:
        return redirect('index')

    if request.method == "POST":
        username = request.POST['username']
        if MyUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('new_user')

        # Create the new user
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']


        new_user = MyUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name,
            is_superuser=(role == 'admin'),
            avatar='avatars/default.png'
        )

        messages.success(request, 'User created successfully.')
        return redirect('users')

    return render(request, 'mgmt/new_user.html')

@login_required
def delete_user(request, username):
    if not request.user.is_superuser:
        return redirect('index')
    
    user = MyUser.objects.get(username=username)
    if user:
        user.delete()
        messages.success(request, 'User deleted successfully.')
    else:
        messages.error(request, 'User not found.')
    
    return redirect('users')


@login_required
def settings(request):
    # Your view logic here
    return render(request, 'mgmt/settings.html')

@login_required
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(current_password):
            messages.error(request, "The current password is incorrect.")
            return redirect('settings')

        if new_password1 != new_password2:
            messages.error(request, "The new passwords do not match.")
            return redirect('settings')

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Keep the user logged in after the password change

        messages.success(request, "Your password has been updated successfully.")
        return redirect('settings')
    return render(request, 'mgmt/settings.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Check if the checkbox is selected
        if request.POST.get('accountActivation'):
            # Delete the user account
            user = request.user
            user.delete()
            messages.success(request, "Your account has been deactivated successfully.")
            return redirect('index')  # Redirect to home or login page after deactivation
        else:
            messages.error(request, "Please confirm account deactivation.")
    return render(request, 'mgmt/settings.html')




from django.db.models import Q

@login_required
def search(request):
    query = request.GET.get('q', '')
    display_table = True  # Assuming you want to display the results in a table

    if query:
        incoming_results = IncomingItem.objects.filter(
            Q(type__name__icontains=query) |  # Search in related Type's name
            Q(model__name__icontains=query) |  # Search in related Model's name
            Q(serial_number__icontains=query) |
            Q(pilot__icontains=query)
        )

        outgoing_results = OutgoingItem.objects.filter(
            Q(type__name__icontains=query) |  # Search in related Type's name
            Q(model__name__icontains=query) |  # Search in related Model's name
            Q(serial_number__icontains=query) |
            Q(pilot__icontains=query)
        )
    else:
        incoming_results = IncomingItem.objects.none()
        outgoing_results = OutgoingItem.objects.none()

    return render(request, 'search_results.html', {
        'query': query,
        'display_table': display_table,
        'incoming_results': incoming_results,
        'outgoing_results': outgoing_results,
    })


@login_required
def ticket(request):
    # Get the last incoming item
    last_incoming_item = IncomingItem.objects.order_by('-date_in', '-id').first()

    # Get the last outgoing item
    last_outgoing_item = OutgoingItem.objects.order_by('-date_out', '-id').first()

    context = {
        'last_incoming_item': last_incoming_item,
        'last_outgoing_item': last_outgoing_item,
    }
    return render(request, 'index.html', context)





@login_required
def index(request):
    # Fetch last incoming and outgoing items
    last_incoming_item = IncomingItem.objects.order_by('-date_in').first()
    last_outgoing_item = OutgoingItem.objects.order_by('-date_out').first()

    # Fetch data for the charts
    incoming_items = IncomingItem.objects.all().order_by('date_in')
    outgoing_items = OutgoingItem.objects.all().order_by('date_out')

    # Convert type instances to their name (string)
    incoming_labels = [item.model.name for item in incoming_items]  # Get the name of the type for labels
    incoming_quantities = [item.quantity for item in incoming_items]

    outgoing_labels = [item.model.name for item in outgoing_items]  # Get the name of the type for labels
    outgoing_quantities = [item.quantity for item in outgoing_items]

    context = {
        'last_incoming_item': last_incoming_item,
        'last_outgoing_item': last_outgoing_item,
        'incoming_labels': json.dumps(incoming_labels),  # Convert to JSON string
        'incoming_quantities': json.dumps(incoming_quantities),  # Convert to JSON string
        'outgoing_labels': json.dumps(outgoing_labels),  # Convert to JSON string
        'outgoing_quantities': json.dumps(outgoing_quantities),  # Convert to JSON string
    }

    return render(request, 'index.html', context)

# def dev(request, number):
#     dev_number = number
#     return render(request, f'mgmt/dev_{dev_number}.html')


# Path: mgmt/urls.py
