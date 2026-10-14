from fastapi import FastAPI
from backend.app.database import connection

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI ERP Assistant API is running!"}


@app.get("/products")
def get_products():
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            sku,
            cost_price,
            selling_price,
            stock_quantity,
            description
        FROM products;
    """)

    rows = cursor.fetchall()

    cursor.close()

    products = []

    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "sku": row[2],
            "cost_price": float(row[3]),
            "selling_price": float(row[4]),
            "stock_quantity": row[5],
            "description": row[6]
        })

    return {"products": products}