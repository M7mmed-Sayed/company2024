from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.db import connections
from django.shortcuts import render, get_object_or_404

# Create your views here.


from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from sqlalchemy.orm import sessionmaker, session

from .auth_backends import SQLAlchemyBackend
from .sqlalchemy_models import UserCustom, engine
from .forms import PostTypeForm, PostForm, ImageForm, CustomUserCreationForm, ProjectForm
from .models import PostType, Image, Post, Project


# Create your views here.
def index(request):
    return render(request, "myapp/lol.html", {})


def home(request):
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # Query the user by username
    # user = session.query(UserCustom).filter_by(username="m7mmed2").first()

    # if not user:
    # User doesn't exist, create and add a sample user
    # sample_user = UserCustom(
    # username="m7mmed2",
    # first_name='John',
    # last_name='Doe',
    # email='john2.doe@example.com'
    # )
    # sample_user.set_password("123")
    # session.add(sample_user)
    # session.commit()
    query = request.GET.get('q')
    posts_with_images = Post.objects.prefetch_related('image_set').all()
    if query:
        posts_with_images = posts_with_images.filter(postSubject__icontains=query)

    media_root = settings.MEDIA_ROOT
    media_path = media_root + '\\'
    context = {
        'posts_with_images': posts_with_images,
        'media_url': media_path,
        'query': query
    }
    return render(request, "myapp/home.html", context)


def post_search(request):
    query = request.GET.get('q')
    posts_with_images = Post.objects.prefetch_related('image_set').all()
    if query:
        posts_with_images = posts_with_images.filter(postSubject__icontains=query)

    media_root = settings.MEDIA_ROOT
    media_path = media_root + '\\'
    context = {
        'posts_with_images': posts_with_images,
        'media_url': media_path,
    }
    return render(request, "myapp/home.html", context)


def add_post_type(request):
    if request.method == 'POST':
        form = PostTypeForm(request.POST)
        if form.is_valid():
            # Check if the name is unique
            name = form.cleaned_data['name']
            if PostType.objects.filter(name=name).exists():
                form.add_error('name', 'A post type with this name already exists.')
            else:
                form.save()
                return redirect('home')  # Redirect to home after successful submission
    else:
        form = PostTypeForm()

    return render(request, 'myapp/add_post_type.html', {'form': form})


def add_post(request):
    post_types = PostType.objects.all()  # Move this line outside of the if statement
    post_projects = Project.objects.all()  # Move this line outside of the if statement
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)  # Create a Post instance but don't save it yet
            post.user = request.user
            post = post_form.save()

            # Save images associated with the post
            for image_file in request.FILES.getlist('postImages[]'):
                Image.objects.create(post=post, image=image_file)

            return redirect('home')  # Redirect to home after successful submission
        else:
            print("not done")
    else:
        post_form = PostForm()

    return render(request, 'myapp/add_post.html',
                  {'post_form': post_form, 'post_types': post_types, 'post_projects': post_projects})


class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'  # Adjust the template path as needed

    def form_valid(self, form):
        # You can access user data using form.cleaned_data

        # Call the parent class method to complete the login process
        response = super().form_valid(form)

        # Redirect the user after successful login
        return response or HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):


        return super().form_invalid(form)


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration (optional)
            return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        form = CustomUserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})


def post_list(request):
    posts_with_images = Post.objects.prefetch_related('image_set').all()
    media_root = settings.MEDIA_ROOT
    media_path = media_root + '\\'
    context = {
        'posts_with_images': posts_with_images,
        'media_url': media_path,
    }
    return render(request, "myapp/post_list.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.prefetch_related('image_set'), pk=pk)
    return render(request, 'myapp/post_detail.html', {'post': post})


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Check if the name is unique
            name = form.cleaned_data['name']
            if Project.objects.filter(name=name).exists():
                form.add_error('name', 'A post type with this name already exists.')
            else:
                project = form.save(commit=False)  # Create a Post instance but don't save it yet
                project.user = request.user
                project = form.save()
                return redirect('home')  # Redirect to home after successful submission
    else:
        form = ProjectForm()

    return render(request, 'myapp/project.html', {'form': form})


def login_view_new(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Get the default database connection
        django_connection = "mssql+pyodbc://DESKTOP-AK9CJ3C/dbcompany2024?driver=ODBC+Driver+17+for+SQL+Server"

        # Authenticate using SQLAlchemyBackend
        user = SQLAlchemyBackend().authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            print("done")
            print(user.is_authenticated)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'myapp/login.html')
