import gradio as gr
import requests

# ============================================================
# FASTAPI BACKEND URL
# ============================================================

API_URL = "https://student-management-api1.onrender.com"


# ============================================================
# PERFORMANCE
# ============================================================

def get_performance(marks):
    if marks >= 90:
        return "Excellent "
    elif marks >= 75:
        return "Very Good "
    elif marks >= 60:
        return "Good "
    elif marks >= 40:
        return "Pass "
    else:
        return "Needs Improvement "


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_all_students():
    try:
        response = requests.get(
            f"{API_URL}/student",
            timeout=10
        )

        if response.status_code != 200:
            return [], [], f"❌ Backend Error: {response.text}"

        result = response.json()
        students = result.get("data", [])

        table_data = []

        for student in students:
            marks = student.get("marks", 0)

            table_data.append([
                student.get("id"),
                student.get("name"),
                student.get("course"),
                marks,
                get_performance(marks)
            ])

        ids = [str(student.get("id")) for student in students]

        return (
            table_data,
            ids,
            f"✅ {len(students)} students loaded"
        )

    except requests.exceptions.ConnectionError:
        return [], [], "❌ Cannot connect to FastAPI. Start the backend first."

    except requests.exceptions.Timeout:
        return [], [], "❌ Backend request timed out."

    except Exception as e:
        return [], [], f"❌ Error: {str(e)}"


# ============================================================
# STATISTICS
# ============================================================

def get_total_students(table):
    return len(table) if table else 0


def get_average_marks(table):
    if not table:
        return "0.00"

    marks = [float(row[3]) for row in table]
    return f"{sum(marks) / len(marks):.2f}"


def get_highest_marks(table):
    if not table:
        return 0

    return max(float(row[3]) for row in table)


# ============================================================
# CREATE STUDENT
# ============================================================

def create_student(name, course, marks):
    if not name or not course or marks is None:
        return (
            "❌ Please fill Name, Course and Marks.",
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update()
        )

    try:
        marks = int(marks)

        if marks < 0 or marks > 100:
            return (
                "❌ Marks must be between 0 and 100.",
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update()
            )

        response = requests.post(
            f"{API_URL}/student",
            params={
                "name": name,
                "course": course,
                "marks": marks
            },
            timeout=10
        )

        if response.status_code not in [200, 201]:
            return (
                f"❌ Failed to create student.\n{response.text}",
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update()
            )

        table, ids, message = get_all_students()

        return (
            "✅ Student created successfully!",
            gr.update(choices=ids),
            gr.update(choices=ids),
            gr.update(choices=ids),
            get_total_students(table),
            get_average_marks(table),
            get_highest_marks(table)
        )

    except Exception as e:
        return (
            f"❌ Error: {str(e)}",
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update()
        )


# ============================================================
# GET STUDENT
# ============================================================

def get_student_details(student_id):
    if not student_id:
        return "❌ Please select a Student ID."

    try:
        response = requests.get(
            f"{API_URL}/student/{int(student_id)}",
            timeout=10
        )

        if response.status_code != 200:
            return f"❌ Student not found.\n{response.text}"

        result = response.json()
        data = result.get("data", [])

        if not data:
            return "❌ Student not found."

        student = data[0]
        marks = student.get("marks", 0)

        return (
            "╔══════════════════════════════╗\n"
            "        🎓 STUDENT DETAILS\n"
            "╚══════════════════════════════╝\n\n"
            f"🆔 Student ID : {student.get('id')}\n"
            f"👤 Name       : {student.get('name')}\n"
            f"📚 Course     : {student.get('course')}\n"
            f"📊 Marks      : {marks}\n"
            f"🏆 Performance: {get_performance(marks)}"
        )

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============================================================
# UPDATE STUDENT
# ============================================================

def update_student(student_id, name, course, marks):
    if not student_id:
        return (
            "❌ Please select a Student ID.",
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update()
        )

    if not name or not course or marks is None:
        return (
            "❌ Please fill all fields.",
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update()
        )

    try:
        marks = int(marks)

        if marks < 0 or marks > 100:
            return (
                "❌ Marks must be between 0 and 100.",
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update()
            )

        response = requests.put(
            f"{API_URL}/student/{int(student_id)}",
            params={
                "name": name,
                "course": course,
                "marks": marks
            },
            timeout=10
        )

        if response.status_code != 200:
            return (
                f"❌ Update failed.\n{response.text}",
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update()
            )

        table, ids, message = get_all_students()

        return (
            "✅ Student updated successfully!",
            gr.update(choices=ids),
            gr.update(choices=ids),
            gr.update(choices=ids),
            get_total_students(table),
            get_average_marks(table),
            get_highest_marks(table)
        )

    except Exception as e:
        return (
            f"❌ Error: {str(e)}",
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update()
        )


# ============================================================
# DELETE STUDENT
# ============================================================

def delete_student(student_id):
    if not student_id:
        return (
            "❌ Please select a Student ID.",
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update()
        )

    try:
        response = requests.delete(
            f"{API_URL}/student/{int(student_id)}",
            timeout=10
        )

        if response.status_code != 200:
            return (
                f"❌ Delete failed.\n{response.text}",
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update(),
                gr.update()
            )

        table, ids, message = get_all_students()

        return (
            "🗑️ Student deleted successfully!",
            gr.update(choices=ids),
            gr.update(choices=ids),
            gr.update(choices=ids),
            get_total_students(table),
            get_average_marks(table),
            get_highest_marks(table)
        )

    except Exception as e:
        return (
            f"❌ Error: {str(e)}",
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update()
        )


# ============================================================
# SEARCH
# ============================================================

def search_students(search_text):
    table, ids, message = get_all_students()

    if not search_text:
        return table

    search_text = search_text.lower().strip()

    return [
        row for row in table
        if (
            search_text in str(row[0]).lower()
            or search_text in str(row[1]).lower()
            or search_text in str(row[2]).lower()
        )
    ]


# ============================================================
# DASHBOARD
# ============================================================

def refresh_dashboard():
    table, ids, message = get_all_students()

    top_student = "No students"

    if table:
        top = max(table, key=lambda row: float(row[3]))
        top_student = f"{top[1]} ({top[3]} marks)"

    return (
        gr.update(choices=ids),
        gr.update(choices=ids),
        gr.update(choices=ids),
        get_total_students(table),
        get_average_marks(table),
        get_highest_marks(table),
        top_student,
        message
    )


def show_top_performers():
    table, ids, message = get_all_students()

    if not table:
        return "No students available."

    sorted_students = sorted(
        table,
        key=lambda row: float(row[3]),
        reverse=True
    )

    output = " TOP PERFORMERS\n\n"

    for index, row in enumerate(sorted_students[:5], start=1):
        output += (
            f"{index}. {row[1]} | "
            f"{row[2]} | "
            f"{row[3]} marks | "
            f"{row[4]}\n"
        )

    return output


# ============================================================
# CUSTOM CSS
# ============================================================

custom_css = """
:root {
    --primary: #7c3aed;
    --secondary: #ec4899;
    --accent: #f59e0b;
    --bg: #fff7ed;
    --card: #ffffff;
    --text: #3f3f46;
}

.gradio-container {
    background: linear-gradient(
        135deg,
        #fff7ed 0%,
        #fdf2f8 48%,
        #f5f3ff 100%
    ) !important;
}

h1, h2, h3 {
    color: #581c87 !important;
}

button.primary {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #ec4899
    ) !important;

    border: none !important;
    color: white !important;
}

button.primary:hover {
    background: linear-gradient(
        90deg,
        #6d28d9,
        #db2777
    ) !important;
}

button.secondary {
    background: #f59e0b !important;
    color: white !important;
    border: none !important;
}

input, textarea, select {
    border: 2px solid #e9d5ff !important;
    border-radius: 10px !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 2px #f3e8ff !important;
}

.tabs {
    border-color: #e9d5ff !important;
}

.tab-nav button {
    color: #6b21a8 !important;
}

.tab-nav button.selected {
    color: #db2777 !important;
    border-bottom: 3px solid #db2777 !important;
}

.gr-box, .gr-panel, .gr-group {
    border-color: #f1d5e8 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 15px rgba(
        124,
        58,
        237,
        0.08
    ) !important;
}

#status_message {
    background: #fef3c7 !important;
    border: 1px solid #f59e0b !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

.dashboard-card {
    background: linear-gradient(
        135deg,
        #ffffff,
        #fdf2f8
    ) !important;

    border: 1px solid #f5d0fe !important;
    border-radius: 16px !important;
    padding: 15px !important;
}
"""


# ============================================================
# GRADIO APPLICATION
# ============================================================

with gr.Blocks(
    title="Student Management System",
    theme=gr.themes.Soft(),
    css=custom_css
) as app:

    gr.Markdown(
        """
        # 🎓 Student Management System
        """
    )

    status_message = gr.Markdown(
        "🟡 **Backend:** Checking connection..."
    )

    gr.Markdown("## 📊 Dashboard")

    with gr.Row():

        with gr.Column(elem_classes="stat-card"):
            total_students = gr.Number(
                label=" Total Students",
                value=0,
                interactive=False
            )

        with gr.Column(elem_classes="stat-card"):
            average_marks = gr.Textbox(
                label=" Average Marks",
                value="0.00",
                interactive=False
            )

        with gr.Column(elem_classes="stat-card"):
            highest_marks = gr.Number(
                label=" Highest Marks",
                value=0,
                interactive=False
            )

        with gr.Column(elem_classes="stat-card"):
            top_performer = gr.Textbox(
                label=" Top Performer",
                value="No students",
                interactive=False
            )

    with gr.Row():

        refresh_button = gr.Button(
            " Refresh Dashboard",
            variant="primary"
        )

        # Same pink + purple color as Refresh Dashboard
        top_button = gr.Button(
            " Top Performers",
            variant="primary"
        )

    with gr.Tabs():

        # ====================================================
        # ADD STUDENT
        # ====================================================

        with gr.Tab(" Add Student"):

            gr.Markdown("### Add New Student")

            with gr.Row():

                create_name = gr.Textbox(
                    label="👤 Student Name",
                    placeholder="Enter student name"
                )

                create_course = gr.Textbox(
                    label="📚 Course",
                    placeholder="Enter course"
                )

                create_marks = gr.Number(
                    label="📊 Marks",
                    minimum=0,
                    maximum=100,
                    step=1
                )

            create_button = gr.Button(
                "➕ Add Student",
                variant="primary"
            )

            create_output = gr.Markdown()

        # ====================================================
        # VIEW STUDENT
        # ====================================================

        with gr.Tab("🔍 View Student"):

            gr.Markdown("### Search Student Details")

            read_id = gr.Dropdown(
                label="Select Student ID",
                choices=[]
            )

            read_button = gr.Button(
                "🔍 View Student",
                variant="primary"
            )

            read_output = gr.Textbox(
                label="Student Information",
                lines=8,
                interactive=False
            )

        # ====================================================
        # UPDATE STUDENT
        # ====================================================

        with gr.Tab("✏️ Update Student"):

            gr.Markdown("### Update Existing Student")

            update_id = gr.Dropdown(
                label="Select Student ID",
                choices=[]
            )

            with gr.Row():

                update_name = gr.Textbox(
                    label="👤 Name"
                )

                update_course = gr.Textbox(
                    label="📚 Course"
                )

                update_marks = gr.Number(
                    label="📊 Marks",
                    minimum=0,
                    maximum=100,
                    step=1
                )

            update_button = gr.Button(
                "✏️ Update Student",
                variant="primary"
            )

            update_output = gr.Markdown()

        # ====================================================
        # DELETE STUDENT
        # ====================================================

        with gr.Tab("🗑️ Delete Student"):

            gr.Markdown("### Delete Student Record")

            delete_id = gr.Dropdown(
                label="Select Student ID",
                choices=[]
            )

            delete_button = gr.Button(
                "🗑️ Delete Student",
                variant="stop"
            )

            delete_output = gr.Markdown()

        # ====================================================
        # TOP PERFORMERS
        # ====================================================

        with gr.Tab("🏆 Top Performers"):

            gr.Markdown("### Student Leaderboard")

            top_output = gr.Textbox(
                label="🏆 Top 5 Students",
                lines=10,
                interactive=False
            )

            top_button_inside = gr.Button(
                "🏆 Show Top Performers",
                variant="primary"
            )


    # ========================================================
    # EVENT HANDLERS
    # ========================================================

    create_button.click(
        fn=create_student,
        inputs=[
            create_name,
            create_course,
            create_marks
        ],
        outputs=[
            create_output,
            read_id,
            update_id,
            delete_id,
            total_students,
            average_marks,
            highest_marks
        ]
    )

    read_button.click(
        fn=get_student_details,
        inputs=read_id,
        outputs=read_output
    )

    update_button.click(
        fn=update_student,
        inputs=[
            update_id,
            update_name,
            update_course,
            update_marks
        ],
        outputs=[
            update_output,
            read_id,
            update_id,
            delete_id,
            total_students,
            average_marks,
            highest_marks
        ]
    )

    delete_button.click(
        fn=delete_student,
        inputs=delete_id,
        outputs=[
            delete_output,
            read_id,
            update_id,
            delete_id,
            total_students,
            average_marks,
            highest_marks
        ]
    )

    refresh_button.click(
        fn=refresh_dashboard,
        outputs=[
            read_id,
            update_id,
            delete_id,
            total_students,
            average_marks,
            highest_marks,
            top_performer,
            status_message
        ]
    )

    top_button.click(
        fn=show_top_performers,
        outputs=top_output
    )

    top_button_inside.click(
        fn=show_top_performers,
        outputs=top_output
    )

    app.load(
        fn=refresh_dashboard,
        outputs=[
            read_id,
            update_id,
            delete_id,
            total_students,
            average_marks,
            highest_marks,
            top_performer,
            status_message
        ]
    )

    gr.Markdown(
        """
        ---
        <div class="footer">


        </div>
        """
    )


# ============================================================
# RUN FRONTEND
# ============================================================

if __name__ == "__main__":
    import os

    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )