from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = serializers.SlugRelatedField(slug_field='id',
                                         queryset=Group.objects.all(),
                                         allow_null=True,
                                         required=False)

    class Meta:
        fields = 'id', 'author', 'text', 'pub_date', 'image', 'group'
        model = Post

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        return post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('author', 'post')
        model = Comment

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        comment = Comment.objects.create(**validated_data)
        return comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message="Вы уже подписаны на этого пользователя!"
            )
        ]

    def validate(self, data):
        user = self.context['request'].user
        if user == data['following']:
            raise ValidationError("Нельзя подписаться на самого себя!")
        return data
