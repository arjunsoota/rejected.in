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


auth = tweepy.OAuthHandler('Pl6bj5U8uP0QcZvR2R7iQ5XEd' , 'RZTXsYNk3lggQnVZGFUg3ZRJLkh8N39AkyIfgmS4Vr8B2vfTp4')
auth.set_access_token('1630734300-TKDnPMLH4SRriUDcbouSDPtQAdgwbXW2h7DiV66', 'x0l48tZqGxRddgN6jyvdguwlk4LTPAka27tsiSqURcLnY')
api = tweepy.API(auth)
# Create your views here.
def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    context ={
        'posts':posts,
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
            
            image_url = user_main.profile_image_url_https
            img_temp = NamedTemporaryFile()
            img_temp.write(urllib.request.urlopen(image_url).read())
            img_temp.flush()

            post.profile_image.save("image_%s" %post.pk, File(img_temp))
            # post.published_date = timezone.now()
            post.save()
            return redirect('submit')
    else:
        form = PostForm()
    return render(request, 'main\post_edit.html', {'form': form})

