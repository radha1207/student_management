from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv
import os


# Load variables from .env
load_dotenv()


# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Check credentials
if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase URL or Key is missing")


# Connect to Supabase
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# Create FastAPI application
app = FastAPI()


# HOME
@app.get("/")
def home():
    return {
        "message": "FastAPI with Supabase is running"
    }


# CREATE student endpoint
@app.post("/student")
def create_student(name: str, course: str, marks: int):

    # Data to be inserted into Supabase
    student = {
        "name": name,
        "course": course,
        "marks": marks
    }

    # Insert student into Supabase
    response = (
        supabase
        .table("student")
        .insert(student)
        .execute()
    )

    # Return database response
    return {
        "message": "Student created successfully",
        "data": response.data
    }


# UPDATE student endpoint
@app.put("/student/{student_id}")
def update_student(
    student_id: int,
    name: str,
    course: str,
    marks: int
):

    student_data = {
        "name": name,
        "course": course,
        "marks": marks
    }

    response = (
        supabase
        .table("student")
        .update(student_data)
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student updated successfully",
        "data": response.data
    }


# DELETE student endpoint
@app.delete("/student/{student_id}")
def delete_student(student_id: int):

    response = (
        supabase
        .table("student")
        .delete()
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student deleted successfully",
        "data": response.data
    }

# GET ALL STUDENTS
@app.get("/student")
def get_students():
    response = (
        supabase
        .table("student")
        .select("*")
        .execute()
    )

    return {
        "message": "Students fetched successfully",
        "data": response.data
    }


# GET SINGLE STUDENT
@app.get("/student/{student_id}")
def get_student(student_id: int):

    response = (
        supabase
        .table("student")
        .select("*")
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student fetched successfully",
        "data": response.data
    }