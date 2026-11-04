from locust import HttpUser, task, between
import random

class WarehouseUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(5)
    def view_analytics(self):
        self.client.get("/analytics")
        
    @task(3)
    def view_orders_paginated(self):
        offset = random.choice([0, 2, 4])
        self.client.get(f"/orders?limit=2&offset={offset}")
        
    @task(1)
    def create_new_order(self):
        payload = {
            "item": "Тестовый товар от робота",
            "price": random.randint(1000, 50000),
            "client_id": 1
        }
        self.client.post("/orders", json=payload)