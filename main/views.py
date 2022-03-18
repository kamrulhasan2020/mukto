from django.db.models import Count
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, reverse
from .models import Board, Post
from .forms import PostCreationForm


class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Recent_Posts"] = Post.objects.annotate(Count("comments")).order_by('-last_activity')[:12]
        return context


class BoardView(ListView):
    model = Post
    paginate_by = 12
    template_name = "main/board.html"
    context_object_name = "Posts"

    def get_queryset(self):
        board_name = self.kwargs["board"]
        self.board = get_object_or_404(Board, name=board_name)
        return self.board.posts.annotate(Count("comments")).order_by('-last_activity')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = self.board
        return context


class PostView(DetailView):
    model = Post
    context_object_name = "Post"
    template_name = "main/post.html"

    def get_object(self):
        board = get_object_or_404(Board, name=self.kwargs["board"])
        self.post = get_object_or_404(Post, no=self.kwargs["no"], board=board)
        return self.post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Comments"] = self.post.comments.all()
        return context


class PostCreationView(CreateView):
    model = Post
    template_name = "main/create-post.html"
    form_class = PostCreationForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        board = get_object_or_404(Board, name=self.kwargs['board'])
        obj.board = board
        obj.save()
        return HttpResponseRedirect(reverse('main:board',
                                            args=[self.kwargs['board']]))