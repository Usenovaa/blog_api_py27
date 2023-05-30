from django.contrib.auth import get_user_model
from .models import Post, Tag, Category
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from .views import PostViewSet

User = get_user_model()


class PostTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(title="cat1")
        tag = Tag.objects.create(title="tag1")
        self.tags = (tag,)
        user = User.objects.create_user(
            email="user@gmail.com", password="12345", is_active=True, name="test"
        )
        self.token = "12345"
        posts = [
            Post(author=user, body="new post", title="post1", category=self.category),
            Post(author=user, body="new post 2", title="post2", category=self.category),
        ]
        Post.objects.bulk_create(posts)

    def test_list(self):
        request = self.factory.get("api/v1/posts/")
        view = PostViewSet.as_view({"get": "list"})
        response = view(request)

        # print(response.data)

        assert response.status_code == 200

    def test_retrieve(self):
        id = Post.objects.all()[0].id
        request = self.factory.get(f"/posts/{id}/")
        view = PostViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=id)
        # print(response.data)

        assert response.status_code == 200

    def test_create(self):
        user = User.objects.all()[0]
        data = {
            "body": "test",
            "title": "post11",
            "category": "cat1",
        }
        request = self.factory.post("/posts/", data, format="json")
        force_authenticate(request, user=user, token=self.token)
        view = PostViewSet.as_view({"post": "create"})
        response = view(request)
        print(user)

        assert response.status_code == 201

    def test_update(self):
        user = User.objects.all()[0]
        data = {"body": "updated body"}
        post = Post.objects.all()[1]
        request = self.factory.patch(f"/posts/{post.id}/", data, format="json")
        force_authenticate(request, user=user)
        view = PostViewSet.as_view({"patch": "partial_update"})
        response = view(request, pk=post.id)
        print(response.data)

        assert Post.objects.get(id=post.id).body == data["body"]

    def test_delete(self):
        user = User.objects.all()[0]
        post = Post.objects.all()[0]
        request = self.factory.delete(f"/posts/{post.id}/")
        force_authenticate(request, user)
        view = PostViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=post.id)
        print(response.status_code)

        assert response.status_code == 204
        assert not Post.objects.filter(id=post.id).exists()
