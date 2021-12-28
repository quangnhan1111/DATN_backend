from django.contrib.auth.models import Group

from sales.repository import SaleRepository


class SaleService:
    def __init__(self):
        self.sale_repository = SaleRepository()

    def get_totel_user(self):
        users = self.sale_repository.get_totel_user()
        return users

    def get_total_product_sold_out(self):
        total = self.sale_repository.get_total_product_sold_out()
        return total

    def get_sale_figure_by_day(self):
        users = self.sale_repository.get_sale_figure_by_day()
        return users

    def get_sale_figure_by_month(self):
        users = self.sale_repository.get_sale_figure_by_month()
        return users

    def get_sale_figure_by_staff(self):
        users = self.sale_repository.get_sale_figure_by_staff()
        return users



