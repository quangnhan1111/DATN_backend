from posts.models import Post
from posts.repository import PostRepository


class PostService:
    def __init__(self):
        self.post_repository = PostRepository()
    def get_list_no_page(self):
        posts = self.post_repository.get_list_no_page()
        return posts

    def index(self):
        posts = self.post_repository.index()
        return posts

    def store(self, request):
        data = self.post_repository.store(request)
        return data

    def show(self, pk):
        if Post.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Post.objects.filter(deleted_at=False, id=pk).exists():
            return self.post_repository.show(pk)
        return None

    def update(self, request, pk):
        if Post.objects.filter(deleted_at=False, id=pk).exists():
            postUpdate = Post.objects.get(id=pk)
            return self.post_repository.update(postUpdate, request)
        return None

    def destroy(self, request, pk):
        if Post.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Post.objects.filter(deleted_at=False, id=pk).exists():
            return self.post_repository.destroy(request, pk)
        return None

    def activate(self, pk):
        if Post.objects.filter(deleted_at=False, id=pk).exists():
            userUpdate = Post.objects.get(id=pk)
            user = self.post_repository.activate(userUpdate)
            return user
        return None

