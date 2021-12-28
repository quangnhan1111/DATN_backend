from .models import Staff
from .repository import StaffRepository


class StaffService():
    def __init__(self):
        self.staff_repository = StaffRepository()

    def get_list_admin_and_staff(self):
        staffs = self.staff_repository.get_list_admin_and_staff()
        return staffs

    def index(self):
        staffs = self.staff_repository.index()
        return staffs

    def store(self, request):
        data = self.staff_repository.store(request)
        return data

    def show(self, pk):
        if Staff.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Staff.objects.filter(deleted_at=False, id=pk).exists():
            return self.staff_repository.show(pk)
        return None

    def update(self, request, pk):
        # print(Staff.objects.all())
        if Staff.objects.filter(deleted_at=False, id=pk).exists():
            userUpdate = Staff.objects.get(pk=pk)
            user = self.staff_repository.update(userUpdate, request)
            return user
        return None

    def destroy(self, request, pk):
        if Staff.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Staff.objects.filter(deleted_at=False, id=pk).exists():
            return self.staff_repository.destroy(request, pk)
        return None

    def activate(self, pk):
        # print(Staff.objects.all())
        if Staff.objects.filter(deleted_at=False, id=pk).exists():
            userUpdate = Staff.objects.get(pk=pk)
            user = self.staff_repository.activate(userUpdate)
            return user
        return None

    def change_password(self, request, pk):
        # print(Staff.objects.all())
        if Staff.objects.filter(deleted_at=False, id=pk).exists():
            userUpdate = Staff.objects.get(pk=pk)
            user = self.staff_repository.change_password(request, userUpdate.user)
            return user
        return None
