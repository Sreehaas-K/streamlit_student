import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Test@1234",
        database="student_db"
    )

st.title("Student Performance Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Marks", "Delete Student", "Analysis"]
)

# Add Student
if menu == "Add Student":
    st.header("Add Student")

    name = st.text_input("Name")
    age = st.number_input("Age", 0, 100)
    subject = st.selectbox("Subject", ["Maths", "Python", "DBMS", "AI"])
    marks = st.number_input("Marks", 0, 100)

    if st.button("Add"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, age, subject, marks) VALUES (%s,%s,%s,%s)",
            (name, age, subject, marks)
        )
        conn.commit()
        conn.close()
        st.success("Student added")

# View Students
elif menu == "View Students":
    st.header("All Students")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    df["Result"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
    st.dataframe(df)

# Update Marks
elif menu == "Update Marks":
    st.header("Update Marks")

    student_id = st.number_input("Student ID", 1)
    new_marks = st.number_input("New Marks", 0, 100)

    if st.button("Update"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET marks=%s WHERE id=%s",
            (new_marks, student_id)
        )
        conn.commit()
        conn.close()
        st.success("Marks updated")

# Delete Student
elif menu == "Delete Student":
    st.header("Delete Student")

    student_id = st.number_input("Student ID", 1)

    if st.button("Delete"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
        conn.commit()
        conn.close()
        st.success("Student deleted")

# Analysis
else:
    st.header("Performance Analysis")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    if df.empty:
        st.warning("No data available")
    else:
        df["Result"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")

        st.subheader("Average Marks")
        st.write(df["marks"].mean())

        st.subheader("Pass Percentage")
        pass_percent = (df["Result"].value_counts(normalize=True) * 100).get("Pass", 0)
        st.write(f"{pass_percent:.2f}%")

        st.subheader("Top Scorer")
        top = df.loc[df["marks"].idxmax()]
        st.write(top[["name", "subject", "marks"]])

        st.subheader("Subject-wise Average Marks")
        st.dataframe(df.groupby("subject")["marks"].mean())
