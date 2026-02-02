from app.database import SessionLocal, Base, engine
from app.models.tenant import Tenant
from app.models.product import Product
from app.models.stock import Stock

'''
Script para criar dados de teste no banco de dados.
'''


def seed():
    '''
    Função para criar tabelas e dados de teste no banco de dados.
    Cria tabelas faltantes e só insere dados se o banco estiver vazio.
    '''
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Só insere dados se ainda não existir nenhum tenant
        if db.query(Tenant).first() is not None:
            print("Banco já possui dados. Apenas tabelas foram verificadas/criadas.")
            return

        tenant1 = Tenant(name="Google")
        tenant2 = Tenant(name="Apple")
        tenant3 = Tenant(name="Microsoft")

        db.add_all([tenant1, tenant2, tenant3])
        db.commit()

        product1 = Product(name="Google Pixel 8")
        product2 = Product(name="Google Pixel 8 Pro")
        product3 = Product(name="Apple iPhone 15")
        product4 = Product(name="Microsoft Surface Pro 9")

        db.add_all([product1, product2, product3, product4])
        db.commit()

        stocks = [
            Stock(tenant_id=tenant1.id, product_id=product1.id, quantity=10, minimum_quantity=5),
            Stock(tenant_id=tenant1.id, product_id=product2.id, quantity=3, minimum_quantity=6),
            Stock(tenant_id=tenant2.id, product_id=product3.id, quantity=20, minimum_quantity=10),
            Stock(tenant_id=tenant3.id, product_id=product4.id, quantity=10, minimum_quantity=5),
        ]

        db.add_all(stocks)
        db.commit()

        print("Seed data created")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
