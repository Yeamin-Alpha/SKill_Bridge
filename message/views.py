from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User



@login_required
def message_list(request):
    """List messages for the logged-in user."""
    received_messages = Message.objects.filter(receiver=request.user).order_by('-sent_time')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-sent_time')
    return render(request, 'message_list.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })


@login_required
def send_message(request, receiver_id):
    """Send a new message to a user."""
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(sender=request.user, receiver=receiver, message=message_text)
            return redirect('message_list')
    return render(request, 'send_message.html', {'receiver': receiver})


@login_required
def mark_as_read(request, message_id):
    """Mark a message as read."""
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return redirect('message_list')



def chat_interface(request):
    contacts = User.objects.exclude(id=request.user.id)  
    return render(request, 'chat_interface.html', {'contacts': contacts})
