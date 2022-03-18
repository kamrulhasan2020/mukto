from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import CommentSerializer
from main.models import Board, Post, Comment


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        board = get_object_or_404(Board, name=self.kwargs["board"])
        post = get_object_or_404(Post, no=self.kwargs["no"], board=board)
        return post.comments.all()

    def perform_create(self, serializer):
        board = get_object_or_404(Board, name=self.kwargs["board"])
        post = get_object_or_404(Post, no=self.kwargs["no"], board=board)
        serializer.save(post=post)


class LatestComment(generics.RetrieveAPIView):
    serializer_class = CommentSerializer

    def get_object(self, **kwargs):
        board = get_object_or_404(Board, name=self.kwargs["board"])
        post = get_object_or_404(Post, board=board, no=self.kwargs["no"])
        return post.comments.latest()