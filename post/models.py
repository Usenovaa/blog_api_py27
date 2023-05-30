from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, primary_key=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Tag(models.Model):
    title = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, primary_key=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    title = models.CharField(max_length=120)
    body = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.author.name } -> {self.title}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.author.name}  to  {self.post.title}'



class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f'{self.rating} - {self.post} '
    


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'Liked {self.post} by {self.author.name}'
    
    

