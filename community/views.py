from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import Post
from django.contrib import messages

@login_required
def Posts(request):
    if request.method == 'POST':
        post = request.POST.get('post')

        Post.objects.create(
                user=request.user,
                post=post,
                num_comments=0,
                num_upvotes=0
        )
        messages.success(request, "Post added successfully!")
        return redirect('profile')  # Redirect after adding the skill

    return render(request, 'add_post.html', {'message': messages})

