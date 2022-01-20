# DATN_backend
1.	Tác nhân:
Tác nhân	Mô tả
Quản trị viên (Admin)	-	Có các quyền tương tự như Moderator.
-	Có quyền phân quyền cho user.
-	Có quyền xem thống kê doanh thu của cửa hàng theo tháng hoặc doanh thu của từng nhân viên
-	Có quyền quản lí các roles và users theo role

Nhân viên (Employee)	- Có quyền xem, sửa thông tin của cá nhân
- Có quyền xem, tạo, sửa, xóa, search, paginate các sản phẩm
- Có quyền xem, tạo, sửa, xóa, search, paginate các brand, danh mục, bài đăng
- Có quyền tạo, sửa, xóa các khách hàng
- Có quyền xem, sửa trạng thái đơn hàng, hủy (xóa mềm) đơn hàng
- Có quyền tạo các hóa đơn thanh toán ứng với đơn hàng của khách hàng.
Khách hàng (Customer)	- Có quyền xem, sửa thông tin cá nhân của bản thân.
- Có quyền xem các thông báo từ việc thanh toán thành công.
- Có quyền tạo đơn hàng và chờ xử lý từ các nhân viên bên hệ thống quản lý.
- Có quyền tạo thông tin thanh toán của chính mình để thực hiện giao dịch.
- Có quyền đăng ký và đăng nhập là một khách hàng.
- Có quyền tìm kiếm, xem sản phẩm, brand, danh mục, các bài đăng và đánh giá của sản phẩm

Các chức năng chính của hệ thống:

1) Authentication: sử dụng jwt trong TokenAuthentication DRF và Permission:
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
Sử dụng:
class ColorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    ...
hoặc:
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_details(request, pk):

-Tạo token trong signal.py:
@receiver(post_save, sender=Staff)
def create_auth_token_profile(sender, instance, created, **kwargs):
    print(sender)
    # Model.User
    print(instance)
    # testUser
    print(created)
    # true or false
    user = User.objects.get(id=instance.user_id)
    if created:
        Token.objects.create(user=user)
        
-Tạo và kiểm soát Permission:
https://viblo.asia/p/cau-chuyen-kiem-soat-truy-cap-trong-django-Qbq5QaDm5D8
https://django-role-permissions.readthedocs.io/en/stable/roles.html#roles-file


I)Customer and Staff:
1)Register:
-Sau khi lấy data:
+Kiểm tra username đó đã có trong hệ thông hay đã bị deleted_at hay chưa
+Kiểm tra  đó đã có trong hệ thông hay đã bị deleted_at hay chưa
-Nếu Ổn: Tạo auth_token = str(uuid.uuid4()) còn is_verify và status mặc định là False và lưu cùng vs các dữ liệu khác trong bảng 
-send_mail_after_registration(email, auth_token): gửi một cái  http://127.0.0.1:8000/api/v1/verify/{auth_token} tới email đó
-Return ...
2)Verify Email:
-Từ auth_token truyền vào tìm ra Customer chứa auth_token qua filter ( Nếu ko tìm ra ==> ERROR )
-Kiểm tra xem is_verify của Customer đó đã True hay False
+True: return về
+False: set is_verify = True và save lại rồi return về

3)Login:
a)Customer:
-Model Customer kế thừa từ Base( Abstract). Trong Base có: created_at, updated_at, deleted_at
-Sau khi lấy data:
+kiểm tra xem customer có đúng username và password ko
+kiểm tra customer is not verified check your mail
+kiểm tra xem customer có active 
-Nếu Ổn: Tạo Token cho customer đó và trả về data gồm: token, group_name và các dữ liẹu cá nhân của customer
b)Staff: (Làm tương tự)

4)CRUD Customer:
a)get-list:
-get current_page ==> tinh ra start = (current_page-1)*per_page, end = current_page*per_page, per_page=10
-Kiem tra Permission:  if has_permission(user, 'view_customer'):
-Nếu Ổn: Trả về data.
==>ORM: .annotate(full_name=Concat('user__first_name', Value(' '), 'user__last_name'): nối field
b)post: (nếu lưu customer bởi admin thì tài khoản được tự động kích hoạt )
-Kiểm tra Permission:   if has_permission(user, 'add_customer')
-Nếu Ổn:
+Kiểm tra Username đã tồn tại hoăc đã bị deleted_at chưa
+Kiểm tra  đã tồn tại hoăc đã bị deleted_at chưa
+Store user và trả về mess thành 
c)Update:
-Kiểm tra Permission:  if has_permission(request.user, 'change_customer') or request.user.id == User.objects.get(customer=pk).id:
-Update và trả về Customer mới.( nếu không có hoặc đã deleted_at trả về ERROR )
d)Delete:
-Kiểm tra Permission: if has_permission(user, 'delete_customer'):
-Delete và trả về Customer đã bị delete(xóa mềm).( nếu không có hoặc đã deleted_at trả về ERROR )
e)get-detail:
-Kiểm tra Permission: if has_permission(user, 'view_customer') or request.user.id == User.objects.get(customer=pk).id:
-Get detail và trả về Customer chi tiết.( nếu không có hoặc đã deleted_at trả về ERROR )
f)activate:
-Kiểm tra Permission: if has_permission(user, 'change_customer') or request.user.id == User.objects.get(customer=pk).id:
-Đổi và lưu lại status mới( nếu không có hoặc đã deleted_at trả về ERROR )
g)change_password trong Customer:
-Kiểm tra Permission: if has_permission(user, 'change_customer') or request.user.id == User.objects.get(customer=pk).id:
-Update password và trả về Customer có password ( nếu không có hoặc đã deleted_at trả về ERROR )

5)CRUD Staff:
a)get-list:(tương tự)
b)post:
-Lấy listRole = request.data['roles'].split(",")
-Kiểm tra Permission:   if has_permission(user, 'add_staff')
-Nếu Ổn:
+Kiểm tra Username đã tồn tại hoăc đã bị deleted_at chưa
+Kiểm tra  đã tồn tại hoăc đã bị deleted_at chưa
+Điều kiện role admin không thể lưu role admin và role staff không thể lưu role admin và role staff 
+Store user và trả về mess thành công ( sử dụng assign_role(staff.user, Admin) và clear_roles(staff.user) )
c)Update:
-Lấy listRole = request.data['roles'].split(",")
-Kiểm tra Permission:  if has_permission(request.user, 'change_staff') or request.user.id == User.objects.get(customer=pk).id:
-Nếu Ổn:
+Điều kiện role admin không thể edit role admin và role staff không thể edit role admin và role staff 
-Update và trả về Customer mới.( nếu không có hoặc đã deleted_at trả về ERROR )
d)delete:
-Kiểm tra Permission: if has_permission(user, 'delete_customer'):
-Nếu Ổn:
+Điều kiện role admin không thể delete role admin và role staff không thể delete role admin và role staff 
-Delete và trả về Customer đã bị delete(xóa mềm).( nếu không có hoặc đã deleted_at trả về ERROR )
e)get-detail:
-Kiểm tra Permission: if has_permission(user, 'view_customer') or request.user.id == User.objects.get(staff=pk).id:
-Nếu Ổn:
+Điều kiện role admin có thể get-detail role admin và role staff có thể get-detail role staff nhưung không thể get-detail role admin 
-Get detail và trả về Customer chi tiết.( nếu không có hoặc đã deleted_at trả về ERROR )
f)activate:
-Kiểm tra Permission: if has_permission(user, 'change_customer') or request.user.id == User.objects.get(staff=pk).id:
-Nếu Ổn:
+Điều kiện role admin có thể activate role admin và role staff có thể activate role staff nhưung không thể activate role admin 
-Đổi và lưu lại status mới( nếu không có hoặc đã deleted_at trả về ERROR )
g)change_password trong Staff:
-Kiểm tra Permission: if has_permission(user, 'change_customer') or request.user.id == User.objects.get(customer=pk).id:
-Update password và trả về Staff có password ( nếu không có hoặc đã deleted_at trả về ERROR )

II)Brands and Category and Subcate:

