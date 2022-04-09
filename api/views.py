from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Post
from django.utils import timezone
from .forms import PostForm

import redis

# Settings for Redis server
SERVER_IP = '127.0.0.1'
SERVER_PORT = '6379'
PASSWORD = ''
DB = 0

def posts(request):
    response = []
    posts = Post.objects.filter().order_by('-datetime')
    for post in posts:
        response.append(
            {
                'datetime': post.datetime,
                'content': post.content,
                'hash': post.hash,
                'txId': post.txId,
                'author': f"{post.user.first_name} {post.user.last_name}",
                'user': post.user.username,
                'unicode': post.unicode,
            }
        )
    return JsonResponse({'response': response})


@login_required
def home(request):
    error = False
    user_email = request.user.email

    # Create connection to the Redis DB
    client = redis.StrictRedis(host=SERVER_IP,
                               port=SERVER_PORT,
                               password=PASSWORD,
                               db=DB,
                               charset="utf-8",
                               decode_responses=True
                               )

    # Client last ip
    last_ip = client.get(user_email)
    # Client current ip
    current_ip = request.META['REMOTE_ADDR']
    if current_ip != last_ip:
        client.set(user_email, current_ip)
        if current_ip != None:
            error = True

    context = {
        'posts': Post.objects.filter().order_by('-datetime'),
        'user': Post.user,
        'datetime': Post.datetime,
        'error': error,
    }
    return render(request, 'api/home.html', context)


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.user = request.user
            post.datetime = timezone.now()


            # it writes the content on th Ropsten
            post.writeOnChain()
            print('content written in Block successfuly')
            post.save()
            return redirect('base-home')
    else:
        form = PostForm()

        context = {
            'form': form
        }

    return render(request, 'api/new_post.html', context)



def articleResearch(request):
    if request.GET:
        post_code = Post.objects.filter(unicode=request.GET['unicode'])
        article = []
        for post in post_code:
            article.append(
                {
                    'datetime': post.datetime,
                    'content': post.content,
                    'hash': post.hash,
                    'txId': post.txId,
                    'author': f"{post.user.first_name} {post.user.last_name}",
                    'user': post.user.username,
                    'unicode': post.unicode,
                }
            )
    return JsonResponse({'article': article})


# Create your views here.