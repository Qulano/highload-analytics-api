from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query, HTTPException, status
from database import init_db_pool, close_db_pool, get_db_pool
from schemas import OrderCreateSchema

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_pool()
    yield
    await close_db_pool()

app = FastAPI(title="Warehouse Analytics API", lifespan=lifespan)

@app.get("/analytics")
async def get_analytics(pool = Depends(get_db_pool)):
    async with pool.acquire() as connection:
        
        query = '''
            SELECT clients.name, COUNT(orders.item), SUM(orders.price) 
            FROM clients 
            JOIN orders ON clients.id = orders.client_id 
            GROUP BY clients.name;
        '''
        
        rows = await connection.fetch(query)
        
        return [
            {
                "client_name": row[0],
                "total_orders": row[1],
                "total_spent": row[2]
            }
            for row in rows
        ]
    
    

@app.post("/orders")
async def create_orders(order: OrderCreateSchema, pool = Depends(get_db_pool)):
    async with pool.acquire() as connection:
            
            query = '''
                INSERT INTO orders (item, price, client_id)
                VALUES ($1, $2, $3)
                RETURNING id;
            '''
            new_id = await connection.fetchval(query, order.item, order.price, order.client_id)
            
    return {
        "status": "success",
        "message": "Order created seccessfully!",
        "order_id": new_id
    }


@app.get("/orders")
async def get_orders(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = 0,
    pool = Depends(get_db_pool)
):
    async with pool.acquire() as connection:
        
        query = '''
            SELECT id, item, price, client_id
            FROM orders
            ORDER BY id ASC
            LIMIT $1 OFFSET $2;
        '''
        
        rows = await connection.fetch(query, limit, offset)
        
        return [
            {
                "id": row[0],
                "item": row[1],
                "price": row[2],
                "client_id": row[3]
            }
            for row in rows
        ]
        
        
@app.get("/orders/{order_id}")
async def get_order_by_id(order_id: int, pool = Depends(get_db_pool)):
    async with pool.acquire() as connection:
        query = '''
            SELECT id, item, price, client_id
            FROM orders
            WHERE id = $1;
        '''
        row = await connection.fetchrow(query, order_id)
        
        if row is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail=f"Order #{order_id} not found."
            )
        
        return {
            "id": row["id"],
            "item": row["item"],
            "price": row["price"],
            "client_id": row["client_id"]
        }
        

@app.delete("/orders/{order_id}")
async def delete_order_by_id(order_id: int, pool = Depends(get_db_pool)):
    async with pool.acquire() as connection:
        query = '''
            DELETE FROM orders
            WHERE id = $1
            RETURNING id;
        '''
        deleted_id = await connection.fetchval(query, order_id)
    
        if deleted_id is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Order #{order_id} not found. Nothing to delete."
            )
        
        return {
            "status": "success",
            "message": f"Order #{order_id} was successfully deleted!"
        }
        
        
        