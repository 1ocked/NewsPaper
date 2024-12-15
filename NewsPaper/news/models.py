from django.db import models
from django.contrib.auth.models import User



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Получаем все посты автора
        posts = Post.objects.filter(author=self)

        # Рассчитываем рейтинг на основе постов
        post_rating = sum(post.rating * 3 for post in posts)

        # Рассчитываем рейтинг комментариев автора
        comments = Comment.objects.filter(user=self.user)
        comment_rating = sum(comment.rating for comment in comments)

        # Рассчитываем рейтинг комментариев к постам автора
        post_comments = Comment.objects.filter(post__in=posts)
        post_comment_rating = sum(comment.rating for comment in post_comments)

        # Итоговый рейтинг
        self.rating = post_rating + comment_rating + post_comment_rating

        # Сохраняем обновлённый рейтинг
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):  #Видео author_post_create_2024-12-11_16-08-12
        return self.name


class Post(models.Model):
    article = 'a'
    news = 'n'

    POST_TYPE = [
        (article, "Статья"),
        (news, "Новость")
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=POST_TYPE, default=article)
    created = models.DateTimeField(auto_now_add=True)
    cats = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        size = 124 if len(self.text) > 124 else len(self.text)
        return self.text[:size] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.user.username