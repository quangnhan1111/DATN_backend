from rolepermissions.roles import AbstractUserRole


class SystemAdmin(AbstractUserRole):
    available_permissions = {
        'drop_tables': True,
    }


class Admin(AbstractUserRole):
    available_permissions = {
        'view_brand': True,
        'add_brand': True,
        'change_brand': True,
        'delete_brand': True,

        'view_category': True,
        'add_category': True,
        'change_category': True,
        'delete_category': True,

        'view_subcategory': True,
        'add_subcategory': True,
        'change_subcategory': True,
        'delete_subcategory': True,

        'view_color': True,
        'add_color': True,
        'change_color': True,
        'delete_color': True,

        'view_coupon': True,
        'add_coupon': True,
        'change_coupon': True,
        'delete_coupon': True,

        'view_customer': True,
        'add_customer': True,
        'change_customer': True,
        'delete_customer': True,

        'view_invoice': True,
        'add_invoice': True,
        'change_invoice': True,
        'delete_invoice': True,

        'view_post': True,
        'add_post': True,
        'change_post': True,
        'delete_post': True,

        'view_product': True,
        'add_product': True,
        'change_product': True,
        'delete_product': True,

        'view_staff': True,
        'add_staff': True,
        'change_staff': True,
        'delete_staff': True,

        'view_review': True,
        'delete_review': True,

        'view_role': True,
        'add_role': True,
        'change_role': True,
        'delete_role': True,

        'view_sale': True,

        'view_chat_room': True,
        'add_chat_room': True,
        'change_chat_room': True,
        'delete_chat_room': True

    }


class Staff(AbstractUserRole):
    available_permissions = {
        'view_brand': True,
        'add_brand': True,
        'change_brand': True,
        # 'delete_brand': True,

        'view_category': True,
        'add_category': True,
        'change_category': True,
        # 'delete_category': True,

        'view_subcategory': True,
        'add_subcategory': True,
        'change_subcategory': True,
        # 'delete_subcategory': True,

        'view_coupon': True,
        'add_coupon': True,
        'change_coupon': True,
        'delete_coupon': True,


        'view_customer': True,
        'add_customer': True,
        'change_customer': True,
        'delete_customer': True,

        'view_invoice': True,
        'add_invoice': True,
        'change_invoice': True,

        'view_post': True,
        'add_post': True,
        'change_post': True,
        'delete_post': True,

        'view_product': True,
        'add_product': True,
        'change_product': True,
        'delete_product': True,

        'view_color': True,
        'add_color': True,
        'change_color': True,
        'delete_color': True,

        'view_review': True,
        'delete_review': True,

    }


class Customer(AbstractUserRole):
    available_permissions = {
        'view_brand': True,

        'view_category': True,

        'view_subcategory': True,

        'view_invoice': True,

        'view_post': True,

        'view_product': True,

        'view_color': True,

        'view_review': True,
        'add_review': True,
        'add_invoice': True,

    }
