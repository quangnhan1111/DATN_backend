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
        
-Tạo và kiểm soát Permission: Tao roles.py trong 
https://viblo.asia/p/cau-chuyen-kiem-soat-truy-cap-trong-django-Qbq5QaDm5D8
https://django-role-permissions.readthedocs.io/en/stable/roles.html#roles-file

xem thêm: https://www.youtube.com/watch?v=epLhHHvJOSs&t=219s

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
+Store user và trả về customer 
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

II)Brands, Category, Subcate, Color, Coupon, Post, Role, Review, Product:

1)CRUD Brand, Color, Coupon, Post, Role, Product:
a)get-list:
-get current_page ==> tinh ra start = (current_page-1)*per_page, end = current_page*per_page, per_page=10
-Kiem tra Permission:  if has_permission(user, 'view_brand'):
-Nếu Ổn: Trả về data.
b)post: 
-Kiểm tra Permission:   if has_permission(user, 'add_customer')
-Nếu Ổn:
+Kiểm tra name Brand  đã tồn tại hoăc đã bị deleted_at chưa
+Kiểm tra  đã tồn tại hoăc đã bị deleted_at chưa ( Nếu có thì restore() )
+Store brand và trả về brand 
c)Update:
-Kiểm tra Permission:  if has_permission(user, 'change_brand'):
-Update và trả về Customer mới.( nếu không có hoặc đã deleted_at trả về ERROR )
d)Delete:
-Kiểm tra Permission: if has_permission(user, ' if has_permission(user, 'delete_brand'):'):
-Delete và trả về Customer đã bị delete(xóa mềm).( nếu không có hoặc đã deleted_at trả về ERROR )
e)get-detail:
-Kiểm tra Permission:     if has_permission(user, 'view_brand'):
-Get detail và trả về chi tiết.( nếu không có hoặc đã deleted_at trả về ERROR )
f)activate:
-Kiểm tra Permission:  if has_permission(user, 'change_brand'):
-Đổi và lưu lại status mới( nếu không có hoặc đã deleted_at trả về ERROR )

2)Category
-các chức năng như trên
a)get_category_and_detail_subcategory():
    def add_sub_into_cate(self, list_category, sub_list, item):
        sub_list.append({
            'id': item['subcategory'],
            'name': item['subcategory__name']
        })
        list_category.append({
            'id': item['id'],
            'name': item['name'],
            'children': sub_list
        })

    def get_category_and_detail_subcategory(self):
        category = Category.objects.filter(deleted_at=False).exclude(subcategory=None).values('id', 'name',
                                                                                              'status',
                                                                                              'created_at',
                                                                                              'updated_at',
                                                                                              'subcategory__name',
                                                                                              'subcategory')
        list_category = []
        for item in category:
            if list_category:
                flag = 0
                for index in list_category:
                    if index['id'] == item['id']:
                        flag = 1
                        index['children'].append({
                            'id': item['subcategory'],
                            'name': item['subcategory__name']
                        })
                        break
                if flag == 0:
                    sub_list = list()
                    self.add_sub_into_cate(list_category, sub_list, item)
            else:
                sub_list = list()
                self.add_sub_into_cate(list_category, sub_list, item)
        print(list_category)
        serializer = CategoryDetailSerializer(instance=list_category, many=True)
        return serializer.data

3)Subcategory:
-Các chức năng trên tương tự
a)get_sub_base_on_category(request, pk):
-Get subcategory và trả về chi tiết subcate va parent-category của nó.( nếu không có hoặc đã deleted_at trả về ERROR )

4)Role:
a)get_role_by_user(request, pk):
-Kiểm tra Permission: if has_permission(user, 'view_role'):
-Kiểm tra xem User có tồn tại hay bị xóa ko
-Nếu ổn: 
        data = User.objects.get(pk=pk)
        name_group = list()
        for i in data.groups.all():
            name_group.append(i.name)
        return name_group[0]
-Trả về Response   
b)get_users_by_role(request, pk):
-Kiểm tra Permission: if has_permission(user, 'view_role'):
-Kiểm tra xem Role có tồn tại hay bị xóa ko
-Nếu ổn: Dùng filter ra các User trong  mỗi role và trả về Response 
c)CRUD cho Role : Tương Tự

5)Review:
a)get_good_review:
reviews = Review.objects.filter(star__gte=3, star__lte=5).order_by('-star')[0:4].values()
b)get_all_review_by_product(self, pk):
filter theo product_id và product_deleted_at = False.

6)Product:
a)sorted_high_to_low(request):
-get current_page ==> tinh ra start = (current_page-1)*per_page, end = current_page*per_page, per_page=10
-Trả về data:
Product.objects.filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False, type='config', brand__deleted_at=False, )......

b)search_base_review(self, rating):
-get current_page ==> tinh ra start = (current_page-1)*per_page, end = current_page*per_page, per_page=10
-Trả về data:
Product.objects.filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False, type='config', brand__deleted_at=False, )......
==>Lấy nhưng product mà product['avgStar'] > float(rating). 

c)search_base_price(self, price_min, price_max):
Tương Tự chức năng b)

d)get_product_by_search(self, key):
-get current_page ==> tinh ra start = (current_page-1)*per_page, end = current_page*per_page, per_page=10
-Trả về data:
Product.objects.filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False, type='config', brand__deleted_at=False, name__contains=key)......

e)get_wishlist_product(request, idCustomer):
-get current_page ==> tinh ra start = (current_page-1)*per_page, end = current_page*per_page, per_page=10
-Trả về data:
WishlistProduct.objects.filter(product__deleted_at=False, product__subcategory__deleted_at=False,
                                                          product__subcategory__category__deleted_at=False,
                                                          product__brand__deleted_at=False,
                                                          customer_id=idCustomer)....
 
f)add_wishlist_product(request, idCustomer):
product = WishlistProduct.objects.create(
            customer_id=int(idCustomer),
            product_id=request.data['product_id'],
        )
product.save()

g)check_wishlist_product(selfS, idCustomer, idPro):
if WishlistProduct.objects.filter(product_id=idPro, customer_id=idCustomer).exists():
   return 1
return 0

h)get_new_product:  .order_by('-created_at')[0:4]

i)get_best_product:  .order_by('-invoicedetail__number')[0:4]

ii)get_related_product_by_brand(request, pk):
-get current_page ==> tinh ra start = (current_page-1)*per_page, end = current_page*per_page, per_page=10
-Trả về data:
Product.objects.filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False, type='config', brand_id=pk)...

iii)CRUD:
Model và các chức năng xem chi tiết trong code !!!

III)Invoice:
a)getInvoicesForOneEmployee(self, pk):
-get current_page ==> tinh ra start = (current_page-1)*per_page, end = current_page*per_page, per_page=10
-Kiểm tra Permission:   if has_permission(user, 'can_view_invoice'):
-Trả về data: Invoice.objects.filter(deleted_at=False, staff_id=pk)..... : thông tin các invoice của 1 staff đã xác  

b)getInvoicesForOneCustomer(self, pk):
Tương tự a nhưng đối vs Customer

c)getInvoicesForEmployeeStatus(self):
Tương Tự a nhưng đối vs all Staff 

d)getInvoicesForCustomerStatus(self):
Tương Tự a nhưng đối vs all Customer

e)
showOneInvoices( request, pk):
showOneInvoicesAndShowEmployee(request, pk):
showOneInvoicesAndShowCustomer(request, pk):
-Tương Tự a nhưng lấy thông tin cụ thể của 1 invoice hoặc có thêm các thông tin liên quan đến product và staff hoặc 

f)CRUD
-list: Tương Tự
-update: update paid_status và staff_id đã xác nhận đơn hàng đó.
-delete: Tương Tự
-add: Xem chi tiết trong code !!!

IV)Sale:
1)get_totel_user(request):
-Kiểm tra Permission:   if has_permission(user, 'can_view_invoice'):
-Lấy data về.

==> Tương tự với các chức năng:
get_total_product_sold_out
get_sale_figure_by_staff
get_sale_figure_by_day
get_sale_figure_by_month:
(
sale_by_month = Invoice.objects.exclude(staff_id=None).annotate(total_sale=Sum('totalPrice'),
                                                                        Month=Extract('updated_at', 'month'),
                                                                        Year=Extract('updated_at', 'year'), ) \
            .values('total_sale', 'Month', 'Year')
)


V)fakedata:
-Xem chi tiết trong 
cmd: python manage.py seed_data 

Tham khảo: https://www.youtube.com/watch?v=8LHdbaV7Dvo&t=369s

VI)Mail(Celery)
Model ScheduleMail(models.Model) xem trong code
-settings.py
-Tạo celery.py trong app(xem code) và thêm code celery trong __init__()

-Trong tasks.py
@shared_task
def send_scheduled_mails():
    mail = ScheduleMail.objects.all().first()
    send_mail(subject=mail.subject, from_email=settings.EMAIL_HOST_USER,
              recipient_list=[_.user.email for _ in CustomerModel.objects.all()],
              message=mail.message,
              fail_silently=True, html_message=mail.html_content)
              
     
celery -A app beat -l info --pidfile =
celery -A app worker -l INFO -P gevent

              
 Tham Khảo:
 https://toidicodedao.com/2019/10/08/message-queue-la-gi-ung-dung-microservice/
 https://viblo.asia/p/tim-hieu-ve-celery-1VgZv4dr5Aw
 https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
 https://www.youtube.com/watch?v=kdVXWCaRQVg
 https://www.youtube.com/watch?v=K5stle-8eRY&t=389s



VII)Notification(Websocket- Channel):
-asgi.py
-settings.py
-wsgi.py
-routings.py

Tham Khảo: 
https://viblo.asia/p/django-channels-vi-du-cap-nhat-real-time-trang-thai-online-offline-cua-nguoi-dung-maGK7kmAKj2
https://codelearn.io/sharing/lap-trinh-web-socket-voi-python
https://www.youtube.com/watch?v=F4nwRQPXD8w
https://www.youtube.com/watch?v=wos1uhnd3qM&t=1922s



