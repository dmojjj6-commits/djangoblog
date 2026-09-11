from django.http import HttpResponse
from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, "blog/home.html", {"title": "DjangoBlog", "posts": posts})
   
def about(request):
    return render(request, 'blog/about.html', {'team':'DjangoBlog Team'})
def contact(request):
    return render(request, 'blog/contact.html', {'abc':'Djangoblog Contact Information.'})