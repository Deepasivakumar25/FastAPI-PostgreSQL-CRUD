from fastapi import FastAPI,HTTPException
from db import get_connection
from pydantic import BaseModel, EmailStr
from datetime import date

app = FastAPI()

class Customer(BaseModel):
    customer_id: int  
    customer_name: str
    email: EmailStr
    city: str
    registration_date: date

class CustomerCreate(BaseModel):
    customer_name: str
    email: EmailStr
    city: str
    registration_date: date

class CustomerUpdate(BaseModel):
    customer_name: str | None = None
    email: EmailStr | None = None
    city: str | None = None
    registration_date: date | None = None

class CustomerUpdateFull(BaseModel):
    customer_name: str
    email: EmailStr
    city: str
    registration_date: date


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}

@app.get("/customers",response_model=list[Customer])
def all_customers():
    con=get_connection()
    cursor = con.cursor()
    cursor.execute("Select * from customers")
    customers = cursor.fetchall()
    cursor.close()
    con.close()
    return[{"customer_id":rec[0],
           "customer_name":rec[1],
           "email": rec[2],
           "city": rec[3],
           "registration_date":rec[4]}
           for rec in customers
    ]

@app.get("/get_customer/{customer_id}", response_model=Customer)
def get_customer(customer_id):
        con=get_connection()
        cursor = con.cursor()
        cursor.execute("Select * from customers where customer_id=%s",(customer_id,))
        customer= cursor.fetchone()
        if not customer:
              raise HTTPException(status_code=404, detail="The customer not found")
        cursor.close()
        con.close()
        return{"customer_id":customer[0],
                "customer_name": customer[1],
                "email": customer[2],
                "city": customer[3],
                "registration_date":customer[4]}


@app.post("/create_customer", response_model=Customer,status_code = 201)
def create_customer(customer: CustomerCreate):
        con=get_connection()
        cursor = con.cursor()
        try:
            cursor.execute( """
            INSERT INTO customers (customer_name, email, city,registration_date)
            VALUES (%s, %s, %s, %s)
            RETURNING customer_id, customer_name, email, city, registration_date
            """,
            (customer.customer_name, customer.email, customer.city,customer.registration_date))
            new_customer= cursor.fetchone()

            result = {"customer_id":new_customer[0],
                    "customer_name": new_customer[1],
                    "email": new_customer[2],
                    "city": new_customer[3],
                    "registration_date": new_customer[4]}
            con.commit()
            return result

        except Exception:
            con.rollback()
            raise

        finally:
            cursor.close()
            con.close()


@app.put('/update_customer/{customer_id}',response_model=CustomerUpdateFull,status_code=200)
def update_customer(customer_id:int,customer:CustomerUpdateFull):
     con=get_connection()
     cursor = con.cursor()
     try:

        query = f"""
            UPDATE customers
            SET customer_name=%s, email=%s,city=%s,registration_date=%s
            WHERE customer_id = %s
            RETURNING customer_id, customer_name, email, city, registration_date
        """
        cursor.execute(query, (customer.customer_name,customer.email,customer.city,customer.registration_date,customer_id))

        updated_customer = cursor.fetchone()
        if not updated_customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        result = {"customer_id":updated_customer[0],
                "customer_name": updated_customer[1],
                "email": updated_customer[2],
                "city": updated_customer[3],
                "registration_date": updated_customer[4]}
        con.commit()
        return result
     except Exception:
          con.rollback()
          raise
     finally:
          cursor.close()
          con.close()
          

@app.patch('/update_customer/{customer_id}',response_model=Customer,status_code=200)
def partially_update(customer_id:int,customer:CustomerUpdate):
     con=get_connection()
     cursor = con.cursor()
     try:
        data = customer.model_dump(exclude_unset=True)

        if not data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update"
            )
        set_clause = ", ".join(
            f"{field} = %s"
            for field in data
        )
        values = list(data.values())
        values.append(customer_id)

        query = f"""
            UPDATE customers
            SET {set_clause}
            WHERE customer_id = %s
            RETURNING customer_id, customer_name, email, city, registration_date
        """
        cursor.execute(query, values)

        updated_customer = cursor.fetchone()
        result = {"customer_id":updated_customer[0],
                "customer_name": updated_customer[1],
                "email": updated_customer[2],
                "city": updated_customer[3],
                "registration_date": updated_customer[4]}
        con.commit()
        return result
     except Exception:
          con.rollback()
          raise
     finally:
          cursor.close()
          con.close()
          
          
@app.delete("/delete_customer/{customer_id}",status_code=200)
def delete_customer(customer_id:int):
     con=get_connection()
     cursor = con.cursor()
     try:
        cursor.execute("delete from customers where customer_id=%s RETURNING customer_id",(customer_id,))
        deleted_customer = cursor.fetchone()
        if not deleted_customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        con.commit()
        return {
            "message": "Customer deleted successfully",
            "customer_id": deleted_customer[0]
        }

     except Exception:
        con.rollback()
        raise
     finally:
        cursor.close()
        con.close()
     



            

