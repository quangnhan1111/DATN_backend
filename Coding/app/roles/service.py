from django.contrib.auth.models import Group, User

from roles.repository import RoleRepository


class RoleService():
    def __init__(self):
        self.role_repository = RoleRepository()

    def get_role_by_user(self, pk):
        if User.objects.filter(pk=pk).exists():
            group_name = self.role_repository.get_role_by_user(pk)
            return group_name
        return None

    def get_users_by_role(self, pk):
        if Group.objects.filter(pk=pk).exists():
            users = self.role_repository.get_users_by_role(pk)
            return users
        return None

    def index(self):
        roles = self.role_repository.index()
        return roles

    def store(self, request):
        data = self.role_repository.store(request)
        return data

    def show(self, pk):
        if Group.objects.filter(id=pk).exists():
            return self.role_repository.show(pk)
        return None

    def update(self, request, pk):
        if Group.objects.filter(id=pk).exists():
            roleUpdate = Group.objects.get(pk=pk)
            role = self.role_repository.update(roleUpdate, request)
            return role
        return None

    def destroy(self, pk):
        if Group.objects.filter(id=pk).exists():
            role = self.role_repository.destroy(pk)
            return role
        return None

