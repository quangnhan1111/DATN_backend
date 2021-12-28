from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand
from faker import Faker

from mailer.models import ScheduleMail
from posts.models import Post
from products.models import Attribute
from staffs.models import Staff
from rolepermissions.roles import assign_role

from app.roles import Admin


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        # Post.objects.create(title="asdaasdsdsad", content="asdasdsadasdasdasdsaasd", image_name="Sadsasdad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdavvsdsad", content="asdasdvvsadasdasdsaasd", image_name="Sadvvsad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdasvvvdsad", content="asdasdsadvvvasdasdsaasd", image_name="Sadsnnnad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdasdnnnsad", content="asdasdsadnasdasdsaasd", image_name="Sadmmmsad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdmmasdsad", content="asdasdsmmadasdasdsaasd", image_name="Sadhhhysad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdghgghasdsad", content="asdasghvbvbdsadasdasdsaasd", image_name="Sadsfgfgdfdfad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdascvcvdsad", content="asdasdsvbvbadasdasdsaasd", image_name="Sadbbbbsad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdasbtttdsad", content="asdastttdsadasdasdsaasd", image_name="Stttadsad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdasdsattttd", content="asdasdsadasdayyyysdsaasd", image_name="Sayyyydsad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="asdghghasdsad", content="asdasdsadjjjjasdasdsaasd", image_name="Sadsjjjjad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        # Post.objects.create(title="ashjhnmnkjdasdsad", content="asdasdsajkjkdasdasdsaasd", image_name="Sakkkdsad",
        #                     image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")
        #
        # Post.objects.create(title="asjkjkdasdsad", content="asdasdsadasdasdsjkjkjkaasd", image_name="Sadsajkjkjkd", image_link="https://interactive-examples.mdn.mozilla.net/media/cc0-images/grapefruit-slice-332-332.jpg")

        Group.objects.create(name='admin')
        Group.objects.create(name='staff')
        Group.objects.create(name='customer')

        user = User.objects.create(username='admin02', email='admin02@email.com', first_name='admin02', last_name='admin02')
        user.set_password('123qwe!@#')
        user.save()

        admin = Staff.objects.create(user=user, address="VN HUe22", phone_number="840796578027")
        admin.save()
        assign_role(admin.user, Admin)

        Attribute.objects.create(label='price', type='Float')
        Attribute.objects.create(label='number', type='Int')
        Attribute.objects.create(label='color', type='Varchar')
        Attribute.objects.create(label='size', type='Varchar')

        ScheduleMail.objects.create(subject="HPBD", message="CMSN")
