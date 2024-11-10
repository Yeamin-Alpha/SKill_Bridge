# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from Users.forms import ProfileImageForm
from .models import ProfileImage, SkillOption, profile, Skill, PublicProfile
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def login_page(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            if not User.objects.filter(username=username).exists():
                errors['username_error'] = "Username does not exist."
            else:
                errors['password_error'] = "Incorrect password. Please try again."
    return render(request, 'login.html', {'errors': errors})

def signup_page(request):
    errors = {}
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            errors['username_error'] = "Username already exists. Please choose a different username."
        if User.objects.filter(email=email).exists():
            errors['email_error'] = "An account with this email already exists. Please use a different email."
        if len(pass1) < 4:
            errors['password_error'] = "Password is too short. It must be at least 4 characters long."
        if pass1 != pass2:
            errors['confirm_password_error'] = "Your password and confirm password are not the same!"

        if not errors:
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html', {'errors': errors})

@login_required
def profile_page(request):
    user_profile_instance, created = profile.objects.get_or_create(user=request.user)
    errors = {}  # Dictionary to store any validation errors

    if request.method == 'POST':
        img = request.FILES.get('img')
        bio = request.POST.get('bio')
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        location = request.POST.get('location')

        # Update fields if they have been provided
        if img:
            user_profile_instance.image = img
        if bio:
            user_profile_instance.bio = bio
        if name:
            user_profile_instance.name = name
        if birthday:
            user_profile_instance.birthday = birthday

        # Validate phone number
        if phone:
            if phone.isdigit() and len(phone) == 11:
                user_profile_instance.phone = phone
            else:
                errors['phone_error'] = "Invalid phone number. Please enter an 11-digit number."

        if gender:
            user_profile_instance.gender = gender    
        if location:
            user_profile_instance.location = location
        
        # Save only if there are no errors
        if not errors:
            user_profile_instance.save()
            return redirect('profile')  # Redirect after saving

    return render(request, 'profile.html', {'profile': user_profile_instance, 'user': request.user, 'errors': errors})

def Ulogout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def delete_profile(request):
    if request.method == 'POST':
        
        user = request.user
        user.delete()
        messages.success(request, "Your profile has been deleted successfully.")
        return redirect('signup')  

    return render(request, 'delete_profile.html')

@login_required
def activate_professional_mode(request):
    user_profile_instance = profile.objects.get(user=request.user)
    user_profile_instance.status = "Professional"
    user_profile_instance.save()
    return redirect('profile')



@login_required
def Skills(request):
    skill_options = SkillOption.objects.all()  # Fetch all predefined skills

    if request.method == 'POST':
        skill_name = request.POST.get('skill_name')
        skill_description = request.POST.get('skill_description')
        skill_price = request.POST.get('skill_price')
        
        # Check if the skill already exists for this user
        existing_skill = Skill.objects.filter(user=request.user, name=skill_name).first()
        
        if existing_skill:
            messages.error(request, "You have already registered this skill.")
        else:
            # Fetch the category from SkillOption and create the skill
            skill_option = SkillOption.objects.get(name=skill_name)
            skill_category = skill_option.category

            Skill.objects.create(
                user=request.user,
                name=skill_name,
                category=skill_category,
                description=skill_description,
                price=skill_price
            )
            messages.success(request, "Skill added successfully!")
            return redirect('profile')  # Redirect after adding the skill

    return render(request, 'add_skill.html', {'skill_options': skill_options})


@login_required
def view_skill(request):
    
    user_skills = Skill.objects.filter(user=request.user)
    return render(request, 'view_skills.html', {'skills': user_skills})




def public_profile(request, username):
    # Get the user and the public profile
    user = get_object_or_404(User, username=username)
    user_public_profile, created = PublicProfile.objects.get_or_create(user=user)
    
    # Get skills and images associated with the user
    skills = Skill.objects.filter(user=user)
    images = ProfileImage.objects.filter(user=user)
    
    # Calculate followers and following counts
    followers_count = user_public_profile.followers.count()
    following_count = user_public_profile.following.count() if hasattr(user_public_profile, 'following') else 0
    rating = user_public_profile.rating  # Assuming rating is a field in PublicProfile

    # Check if the logged-in user is following this profile
    is_following = False
    if request.user.is_authenticated:
        is_following = user_public_profile.followers.filter(id=request.user.id).exists()
    
    # Check if the logged-in user is the profile owner
    is_owner = request.user == user

    # Handle image upload if the request is POST and user is the owner
    if request.method == 'POST' and is_owner:
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            profile_image = form.save(commit=False)
            profile_image.user = user  # Associate the uploaded image with the user
            profile_image.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect('public_profile', username=username)
        else:
            messages.error(request, "Failed to upload image.")
    else:
        form = ProfileImageForm()

    # Context for rendering the template
    context = {
        'public_profile': user_public_profile,
        'skills': skills,
        'images': images,
        'followers_count': followers_count,
        'following_count': following_count,
        'rating': rating,
        'is_following': is_following,
        'is_owner': is_owner,
        'form': form,
    }

    return render(request, 'public_profile.html', context)

@login_required
def toggle_follow(request, username):
    public_profile = get_object_or_404(PublicProfile, user__username=username)
    
    # Toggle follow/unfollow
    if public_profile.followers.filter(id=request.user.id).exists():
        public_profile.followers.remove(request.user)
        following = False
    else:
        public_profile.followers.add(request.user)
        following = True
    
    # No need to save as followers are a ManyToManyField, which saves changes automatically
    followers_count = public_profile.followers.count()
    return JsonResponse({'following': following, 'followers_count': followers_count})