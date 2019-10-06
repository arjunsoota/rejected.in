from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import tweepy
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib


auth = tweepy.OAuthHandler('' , '')
auth.set_access_token('', '')
api = tweepy.API(auth)
# Create your views here.
def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    context ={
        'posts':posts
        }
    return render(request, 'main\index.html',context)

def submit(request):
    return render(request, 'main\submit.html',{})




@login_required
def post_new(request):
    user_main = api.get_user(request.user)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.name = user_main.name
            post.profile_image = user_main.profile_image_url_https
            # post.published_date = timezone.now()
            post.save()
            return redirect('submit')
    else:
        data = {'position' : user_main.description }
        form = PostForm(initial=data)  
    return render(request, 'main\post_edit.html', {'form': form , 'user_obj':user_main})

