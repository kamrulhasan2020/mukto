from main.models import Board, Post, Comment
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        exclude = ()


class PostSerializer(serializers.ModelSerializer):
    board = serializers.ReadOnlyField(source='board.name')

    class Meta:
        model = Post
        exclude = ()


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.no')
    parent = serializers.SlugRelatedField(slug_field='no', required=False,
                                          queryset=Comment.objects.all())

    class Meta:
        model = Comment
        fields = ['body', 'image', 'no', 'created', 'post', 'parent']