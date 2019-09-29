from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    context ={
        'posts':posts,
        }
    return render(request, 'main\index.html',context)
