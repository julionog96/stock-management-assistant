from app.database import SessionLocal, Base, engine
from app.models.tenant import Tenant
from app.models.product import Product
from app.models.stock import Stock

'''
Script para criar dados de teste no banco de dados.
'''


def seed():
    '''
    Função para criar dados de teste no banco de dados.
    '''
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        tenant1 = Tenant(name="Loja A")
        tenant2 = Tenant(name="Loja B")

        db.add_all([tenant1, tenant2])
        db.commit()

        product1 = Product(name="Produto X")
        product2 = Product(name="Produto Y")

        db.add_all([product1, product2])
        db.commit()

        stocks = [
            Stock(tenant_id=tenant1.id, product_id=product1.id, quantity=10, minimum_quantity=5),
            Stock(tenant_id=tenant1.id, product_id=product2.id, quantity=3, minimum_quantity=6),
            Stock(tenant_id=tenant2.id, product_id=product1.id, quantity=20, minimum_quantity=10),
        ]

        db.add_all(stocks)
        db.commit()

        print("Seed data created")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
