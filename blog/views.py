from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Posts

# def home(request):
#     context = {
#         'posts' : Posts.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

# you can use top function or below(class based view) to make a view and render template, either way you can do 

class PostListView(ListView):
    model = Posts               # <model>_detail.html= default template it will look for , posts_list.html
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5  # no of post you want to show on one page (how many records you want to paginate)

class UserPostListView(ListView):
    model = Posts               # <model>_detail.html= default template it will look for , posts_list.html
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5  # no of post you want to show on one page (how many records you want to paginate)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Posts                # <model>_detail.html= default template it will look for, i.e., posts_detail.html

# always add "LoginRequiredMixin" as first argumnet 
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts                # <model>_form.html= default template it will look for is _form same for update also, i.e., posts_form.html
    fields = ['title','content']

    # if we have used a user in field and added from form while posting, then no ned to write below function
    # this below function is for overwritting that author column of model with current user before posting data
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# "UserPassesTestMixin" is for authorizing that the peron who is accessing update passes a test which is defined in test_func()
# in test_func() we will check if person who is updating is auther of that post or not?
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts                # <model>_form.html= default template it will look for is _form same for update also, i.e., posts_form.html
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()             # method of UpdateView
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts                # <model>_confirm_delete.html= default template it will look for, i.e., posts_confirm_delete.html
    success_url = '/'

    def test_func(self):
        post = self.get_object()             # method of UpdateView
        if self.request.user == post.author:
            return True
        return False

def about(request):
    context = {
        'title' : 'Blog About'
    }
    return render(request, 'blog/about.html', context)

# Create your views here.
