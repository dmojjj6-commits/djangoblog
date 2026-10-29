from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from .forms import PostForm, RegisterForm
from .models import Post, Category

def home(request):
    posts = Post.objects.filter(status="published").order_by("-pk")
    category = request.GET.get("category")
    if category:
        posts = posts.filter(category__name__iexact=category)
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    categories = Category.objects.all()
    return render(request, "blog/home.html", {"title": "Neon Drive", "page_obj": page_obj, "categories": categories})
   
def about(request):
    return render(request, 'blog/about.html', {'team':'Neon Drive Team'})
def contact(request):
    return render(request, 'blog/contact.html', {'abc':'Neon Drive Contact Information.'})
def custom_403(request, exception=None):
    return render(request, "blog/403.html", status=403)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        messages.success(request, "Post published successfully!")
        return redirect("post_detail", slug=post.slug)

    return render(request, "blog/post_form.html", {"form": form})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post_detail", slug=post.slug)
    return render(request, "blog/post_form.html", {"form": form, "post": post})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "blog/post_confirm_delete.html", {"post": post})

def post_detail(request, slug):
    posts = Post.objects.filter(status="published")
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            Q(status="published") | Q(author=request.user)
        )
    post = get_object_or_404(posts, slug=slug)
    return render(request, "blog/post_detail.html", {"post": post})

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by("-pk")
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/my_posts.html", {"title": "My Posts", "page_obj": page_obj})