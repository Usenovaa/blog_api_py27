from rest_framework import serializers
from .models import Category, Tag, Post, Comment, Rating
from django.contrib.auth import get_user_model
from django.db.models import Avg


User = get_user_model()

serializers.Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('title',)


class PostSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                'Пост с таким заголовком уже существует'
            )
        return title
    

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        try:
            tags = validated_data.pop('tags')
        
            post = Post.objects.create(author=user, **validated_data)
            post.tags.add(*tags)
        except:
            post = Post.objects.create(author=user, **validated_data)

        return post


    

    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['comments'] = CommentCreateSerializer(Comment.objects.filter(post=instance.pk), many=True).data
        representation['likes_count'] = instance.likes.count()
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']

        return representation
    

class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment
    


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Rating
        fields = '__all__'


    def validate_rating(self, rating):
        if rating not in range(1, 11):
            raise serializers.ValidationError(
                'Рейтинг должен быть от 1 до 10'
            )
        return rating

    def create(self, validated_data):
        user = self.context.get('request').user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)