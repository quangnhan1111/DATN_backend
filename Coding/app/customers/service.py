from customers.repository import UserRepository
from .models import Customer as CustomerModel


class CustomerService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_list_no_paginate(self):
        users = self.user_repository.get_list_no_paginate()
        return users

    def index(self):
        users = self.user_repository.index()
        return users

    def store(self, request):
        data = self.user_repository.store(request)
        return data

    def show(self, pk):
        if CustomerModel.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if CustomerModel.objects.filter(deleted_at=False, id=pk).exists():
            return self.user_repository.show(pk)
        return None

    def update(self, request, pk):
        if CustomerModel.objects.filter(deleted_at=False, id=pk).exists():
            userUpdate = CustomerModel.objects.get(id=pk)
            user = self.user_repository.update(userUpdate, request)
            return user
        return None

    def destroy(self, request, pk):
        # print(CustomerModel.objects.get(user__username='test_user').id)
        if CustomerModel.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if CustomerModel.objects.filter(deleted_at=False, id=pk).exists():
            return self.user_repository.destroy(request, pk)
        return None

    def activate(self, pk):
        if CustomerModel.objects.filter(deleted_at=False, id=pk).exists():
            userUpdate = CustomerModel.objects.get(id=pk)
            user = self.user_repository.activate(userUpdate)
            return user
        return None

    def change_password(self, request, pk):
        if CustomerModel.objects.filter(deleted_at=False, id=pk).exists():
            userUpdate = CustomerModel.objects.get(id=pk)
            user = self.user_repository.change_password(request, userUpdate.user)
            return user
        return None
