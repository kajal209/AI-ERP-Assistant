from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from backend.app.database import connection

app = FastAPI()

class SaleRequest(BaseModel):
    customer_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

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

@app.post("/sales")
def create_sale(sale: SaleRequest):
    cursor = connection.cursor()

    try:
        # Check customer
        cursor.execute(
            "SELECT id FROM customers WHERE id = %s;",
            (sale.customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:
            cursor.close()
            raise HTTPException(
                status_code=404,
                detail="customer not found"
            )

        # Check product and get price + stock
        cursor.execute(
            """
            SELECT id, selling_price, stock_quantity
            FROM products
            WHERE id = %s
            FOR UPDATE;
            """,
            (sale.product_id,)
        )

        product = cursor.fetchone()

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        product_id = product[0]
        selling_price = product[1]
        stock_quantity = product[2]

        # Check stock
        if stock_quantity < sale.quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )

        # Calculate total
        subtotal = selling_price * sale.quantity

        # Create sale
        cursor.execute(
            """
            INSERT INTO sales (customer_id, total_amount)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (sale.customer_id, subtotal)
        )

        sale_id = cursor.fetchone()[0]

        # Create sale item
        cursor.execute(
            """
            INSERT INTO sale_items
            (sale_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                sale_id,
                product_id,
                sale.quantity,
                selling_price,
                subtotal
            )
        )

        # Update product stock
        cursor.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity - %s
            WHERE id = %s;
            """,
            (sale.quantity, product_id)
        )

        connection.commit()
    
        return {
            "message": "Sale created successfully",
            "sale_id": sale_id,
            "total_amount": float(subtotal)
        }

    except HTTPException:
        connection.rollback()
        raise

    except Exception as e:
        connection.rollback()
        cursor.close()

        return {
            "error": "Sale failed",
            "details": str(e)
        }

    finally:
        cursor.close()


@app.get("/sales")
def get_sales():
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT 
                s.id,
                c.name AS customer_name,
                s.sale_date,
                s.total_amount
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            ORDER BY s.id DESC;
            """
        )

        rows = cursor.fetchall()

        sales = []
        for row in rows:
            sales.append({
                "sale_id": row[0],
                "customer_name": row[1],
                "sale_date": str(row[2]),
                "total_amount": float(row[3])
            })

        return {"sales": sales}

    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch sales: {str(e)}"
        )

    finally:
        cursor.close()

@app.get("/sales/{sale_id}")
def get_sale_details(sale_id: int):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT 
                s.id,
                c.name,
                s.sale_date,
                s.total_amount,
                p.name,
                si.quantity,
                si.unit_price,
                si.subtotal
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            JOIN sale_items si ON s.id = si.sale_id
            JOIN products p ON si.product_id = p.id
            WHERE s.id = %s;
            """, (sale_id,)
        )

        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="Sale not found"
            )

        first_row = rows[0]

        items = []
        for row in rows:
            items.append({
                "product_name": row[4],
                "quantity": row[5],
                "unit_price": float(row[6]),
                "subtotal": float(row[7])
            })

        return {
            "sale_id": first_row[0],
            "customer_name": first_row[1],
            "sale_date": str(first_row[2]),
            "total_amount": float(first_row[3]),
            "items": items
        }
    except HTTPException:
        connection.rollback()
        raise

    except Exception as e :
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch sale details: {str(e)}"
        )

    finally:
        cursor.close()




@app.get("/reports/sales-summary")
def get_sales_summary():
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                COUNT(*) AS total_sales,
                COALESCE(SUM(total_amount), 0) AS total_revenue,
                COALESCE(AVG(total_amount), 0) AS average_sale_amount
            FROM sales;
        """)

        row = cursor.fetchone()

        return {
            "total_sales": int(row[0]),
            "total_revenue": float(row[1]),
            "average_sale_amount": round(float(row[2]), 2)
        }

    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch sales summary: {str(e)}"
        )

    finally:
        cursor.close()


@app.get("/reports/products-sales")
def get_product_sales():
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT 
                p.id,
                p.name,
                COALESCE(SUM(si.quantity), 0) AS units_sold,
                COALESCE(SUM(si.subtotal), 0) AS total_revenue
            FROM products p
            LEFT JOIN sale_items si ON p.id = si.product_id
            GROUP BY p.id, p.name
            ORDER BY units_sold DESC, p.name ASC;
            """
        )

        rows = cursor.fetchall()

        products = []
        for row in rows:
            products.append({
                "product_id": row[0],
                "product_name": row[1],
                "units_sold": int(row[2]),
                "total_revenue": float(row[3])
            })

        return {"product_sales": products}

    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail= f"Could not fetch product sales: {str(e)}"
        )

    finally:
        cursor.close()


@app.get("/reports/low-stock")
def get_low_stock(threshold: int = 10):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                name,
                sku,
                stock_quantity
            FROM products
            WHERE stock_quantity <= %s
            ORDER BY stock_quantity ASC;
            """, (threshold,)
        )

        rows = cursor.fetchall()

        products = [] 
        for row in rows:
            products.append({
                "product_id": row[0],
                "product_name": row[1],
                "sku": row[2],
                "stock_quantity": row[3]
            })

        return {
            "threshold": threshold,
            "low_stock_products": products
        }

    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch low-stock report: {str(e)}"
        )

    finally:
        cursor.close()


@app.get("/reports/inventory-summary")
def get_inventory_summary():
    cursor = connection.cursor()


    try:
        cursor.execute(
            """
            SELECT 
                COUNT(*) AS total_products,
                COALESCE(SUM(stock_quantity), 0) AS total_units_in_stock,
                COALESCE(SUM(stock_quantity * cost_price), 0) AS inventory_cost_value,
                COALESCE(SUM(stock_quantity * selling_price), 0) AS potential_sales_value
            FROM products;
            """
        )

        row = cursor.fetchone()

        return {
            "total_products": row[0],
            "total_units_in_stock": row[1],
            "inventory_cost_value": float(row[2]),
            "potential_sales_value": float(row[3])
        }

    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch inventory summary: {str(e)}"
        )

    finally:
        cursor.close()