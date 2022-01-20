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

2)Login:
a)Customer:
-Model Customer kế thừa từ Base( Abstract). Trong Base có: created_at, updated_at, deleted_at
-Sau khi lấy data:
+kiểm tra xem customer có đúng username và password ko
+kiểm tra customer is not verified check your mail
+kiểm tra xem customer có active 
-Nếu Ổn: Tạo Token cho customer đó và trả về data gồm: token, group_name và các dữ liẹu cá nhân của customer



1) Authentication: sử dụng jwt trong TokenAuthentication DRF
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]

class ColorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    ...
