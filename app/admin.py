from sqladmin import Admin, ModelView
from app.database import engine
from app.models.tenant import Tenant
from app.models.product import Product
from app.models.stock import Stock


class TenantAdmin(ModelView, model=Tenant):
    column_list = [Tenant.id, Tenant.name]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name]


class StockAdmin(ModelView, model=Stock):
    column_list = [
        Stock.id,
        Stock.tenant_id,
        Stock.product_id,
        Stock.quantity,
        Stock.minimum_quantity
    ]


def setup_admin(app):
    admin = Admin(app, engine)
    admin.add_view(TenantAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(StockAdmin)
