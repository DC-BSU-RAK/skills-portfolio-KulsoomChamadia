# k𖹭.ᐟ------------------importing necessary libraries---------------------------$𖹭.ᐟ
from tkinter import *
from PIL import ImageTk, Image # k𖹭.ᐟ-----this is for importing images----$𖹭.ᐟ
import json # k𖹭.ᐟ----this is for reading JSON file----$𖹭.ᐟ
from tkinter import messagebox # k𖹭.ᐟ----this is for showing popup message----$𖹭.ᐟ
import matplotlib.pyplot as plt # k𖹭.ᐟ----this is used for creating graphs----$𖹭.ᐟ
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # k𖹭.ᐟ----this is displaying graph inside the tkiter with the help of matplotlib----$𖹭.ᐟ
import matplotlib 
matplotlib.use('Agg') # k𖹭.ᐟ----to prevent matplotlib windows from opening sepratly----$𖹭.ᐟ
import matplotlib.patches as patches # k𖹭.ᐟ----this is used for drawing shapes in graphs----$𖹭.ᐟ
import matplotlib.path as path  # k𖹭.ᐟ----this is used for creating custom paths in graphs----$𖹭.ᐟ
import numpy as np  # k𖹭.ᐟ----this is used for calculations----$𖹭.ᐟ

# k𖹭.ᐟ------------------create main window---------------------------$𖹭.ᐟ
root = Tk()
root.geometry("1900x1000")
root.title("Student Manager")
root.iconphoto(False, ImageTk.PhotoImage(file="ex3/bgpics/logoo.png"))


# k𖹭.ᐟ------------------file path for student data---------------------------$𖹭.ᐟ
FILE_PATH = r"C:\Users\kulso\OneDrive\Desktop\CodeLab2 Assessment1\ex3\studentmarks.json"

# k𖹭.ᐟ------------------function for switching frames---------------------------$𖹭.ᐟ
def frame_switch(frame):
    frame.tkraise()

# k𖹭.ᐟ------------------load student data from JSON file---------------------------$𖹭.ᐟ
def import_studentdata():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            students = data.get("Student Details", [])
        else:
            students = data

        if not isinstance(students, list):
            print("❌ error: student data is not a list")
            return []

        return students

    except FileNotFoundError:
        print(f"info: {FILE_PATH} not found")
        return []

    except json.JSONDecodeError as e:
        print("❌ json decode error:", e)
        return []

    except Exception as e:
        print("❌ error while loading json:", e)
        return []

# k𖹭.ᐟ------------------saveing student data to JSON file---------------------------$𖹭.ᐟ
def record_stdlist(students):
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=4)
        return True, None
    except Exception as e:
        return False, str(e)

# k𖹭.ᐟ------------------calculating grades from percentage---------------------------$𖹭.ᐟ
def grading(p):
    if p >= 85:
        return "A"
    elif p >= 70:
        return "B"
    elif p >= 55:
        return "C"
    elif p >= 40:
        return "D"
    else:
        return "F"

# k𖹭.ᐟ------------------global student data---------------------------$𖹭.ᐟ
student_data = import_studentdata()

# k𖹭.ᐟ------------------showing each student with details---------------------------$𖹭.ᐟ
def veiw_studentlst():
    global student_data
    student_data = import_studentdata()
    frame_switch(frame2)
    text_box.delete("1.0", END)

    if not student_data:
        text_box.insert(END, "No student data found.\n")
        return

    for s in student_data:
        try:
            test_total = int(s.get('course1', 0)) + int(s.get('course2', 0)) + int(s.get('course3', 0))
            exam_total = int(s.get('exam', 0))
            total_marks = test_total + exam_total
            percentage = (total_marks / 160) * 100 if 160 != 0 else 0
            grade = grading(percentage)
        except Exception:
            test_total = 0
            exam_total = 0
            total_marks = 0
            percentage = 0
            grade = "N/A"

        text_box.insert(
            END,
            f"Student Id: {s.get('code', '')}\n"
            f"Name: {s.get('name', '')}\n"
            f"Course1: {s.get('course1', '')}\n"
            f"Course2: {s.get('course2', '')}\n"
            f"Course3: {s.get('course3', '')}\n"
            f"Exam: {s.get('exam', '')}\n"
            f"Total Marks (out of 160): {total_marks}\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Grade: {grade}\n"
            f"--------------------------------------\n\n"
        )

# k𖹭.ᐟ------------------showing performance graph for each student---------------------------$𖹭.ᐟ
def show_student_graph(student):
    popup = Toplevel(root)
    popup.title(f"Performance Analysis - {student.get('name', '')}")
    popup.geometry("900x750")
    popup.configure(bg="#1A5276")
    
    details_frame = Frame(popup, bg="#2874A6", padx=10, pady=10)
    details_frame.pack(fill="x", padx=20, pady=10)
    
    details_text = (
        f"Student ID: {student.get('code', '')} | "
        f"Name: {student.get('name', '')} | "
        f"Course1: {student.get('course1', 0)} | "
        f"Course2: {student.get('course2', 0)} | "
        f"Course3: {student.get('course3', 0)} | "
        f"Exam: {student.get('exam', 0)}"
    )
    
    Label(details_frame, text=details_text, font=("Arial", 12, "bold"), 
          bg="#2874A6", fg="white").pack()
    
    try:
        test_total = int(student.get('course1', 0)) + int(student.get('course2', 0)) + int(student.get('course3', 0))
        exam_total = int(student.get('exam', 0))
        total_marks = test_total + exam_total
        percentage = (total_marks / 160) * 100 if 160 != 0 else 0
        grade = grading(percentage)
        
        performance_text = f"Total Marks: {total_marks}/160 | Percentage: {percentage:.2f}% | Grade: {grade}"
        Label(details_frame, text=performance_text, font=("Arial", 11), 
              bg="#2874A6", fg="#ECF0F1").pack()
    except Exception as e:
        print(f"error calculating performance: {e}")
        percentage = 0
        grade = "N/A"

    charts_frame = Frame(popup, bg="#1A5276")
    charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor('#1A5276')
    
    courses = ['Course 1', 'Course 2', 'Course 3']
    try:
        marks = [
            int(student.get('course1', 0)),
            int(student.get('course2', 0)), 
            int(student.get('course3', 0))
        ]
    except (ValueError, TypeError):
        marks = [0, 0, 0]
    
    line = ax1.plot(courses, marks, marker='o', linewidth=4, markersize=10, 
                   color='#27AE60', markerfacecolor='#F39C12', 
                   markeredgecolor='white', markeredgewidth=2)
    
    ax1.set_facecolor('#2874A6')
    ax1.set_ylabel('Marks', fontsize=12, fontweight='bold', color='white')
    ax1.set_xlabel('Courses', fontsize=12, fontweight='bold', color='white')
    ax1.set_title('Performance Trend Across Courses', 
                 fontsize=14, fontweight='bold', pad=20, color='white')
    
    ax1.tick_params(axis='x', colors='white', which='both')
    ax1.tick_params(axis='y', colors='white', which='both')
    ax1.set_ylim(0, 25)
    
    for spine in ax1.spines.values():
        spine.set_color('white')
    ax1.grid(True, alpha=0.2, linestyle='--', color='white')
    
    create_gauge_chart(ax2, percentage, grade)
    
    plt.tight_layout(pad=3.0)
    
    canvas = FigureCanvasTkAgg(fig, master=charts_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    close_btn = Button(popup, text="Close", font=("Arial", 12, "bold"),
                      bg="#27AE60", fg="white", command=popup.destroy)
    close_btn.pack(pady=10)
    
    popup.transient(root)
    popup.grab_set()
    popup.focus_set()

# k𖹭.ᐟ------------------createing gauge chart for indival students ---------------------------$𖹭.ᐟ
def create_gauge_chart(ax, percentage, grade):
    ax.clear()
    
    max_value = 100
    start_angle = 180
    end_angle = 0
    
    zones = [
        (0, 40, '#E74C3C'),
        (40, 55, '#F39C12'),
        (55, 70, '#F1C40F'),
        (70, 85, '#2ECC71'),
        (85, 100, '#27AE60')
    ]
    
    for min_val, max_val, color in zones:
        zone_start_angle = 180 - (min_val / max_value * 180)
        zone_end_angle = 180 - (max_val / max_value * 180)
        
        wedge = patches.Wedge(center=(0.5, 0.3), r=0.4,
                             theta1=zone_end_angle, theta2=zone_start_angle, 
                             width=0.2, color=color, alpha=0.7)
        ax.add_patch(wedge)
    
    needle_angle = 180 - (percentage / max_value * 180)
    
    needle_length = 0.35
    needle_x = 0.5 + needle_length * np.cos(np.radians(needle_angle))
    needle_y = 0.3 + needle_length * np.sin(np.radians(needle_angle))
    
    ax.plot([0.5, needle_x], [0.3, needle_y], color='#2C3E50', 
            linewidth=4, solid_capstyle='round')
    
    center_circle = plt.Circle((0.5, 0.3), 0.03, color='#2C3E50')
    ax.add_patch(center_circle)
    
    ax.text(0.5, 0.3, f'{percentage:.1f}%', 
            horizontalalignment='center', verticalalignment='center',
            fontsize=16, fontweight='bold', color='white')
    
    ax.text(0.5, 0.15, f'Grade: {grade}', 
            horizontalalignment='center', verticalalignment='center',
            fontsize=12, fontweight='bold', color='white')
    
    for i in range(0, 101, 20):
        angle = 180 - (i / max_value * 180)
        x = 0.5 + 0.45 * np.cos(np.radians(angle))
        y = 0.3 + 0.45 * np.sin(np.radians(angle))
        ax.text(x, y, f'{i}%', fontsize=8, color='white', 
                ha='center', va='center', fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.8)
    ax.set_facecolor('#2874A6')
    ax.set_title('Overall Performance', fontsize=14, 
                 fontweight='bold', color='white', pad=20)
    ax.axis('off')

# k𖹭.ᐟ------------------global variables---------------------------$𖹭.ᐟ
student_data = import_studentdata()
graph_button = None

# k𖹭.ᐟ------------------show student names as clickable list---------------------------$𖹭.ᐟ
def veiw_indivisual():
    global student_data, graph_button
    
    if graph_button:
        graph_button.destroy()
        graph_button = None
    
    student_data = import_studentdata()
    frame_switch(frame2)
    text_box.delete("1.0", END)

    if not student_data:
        text_box.insert(END, "No student data found.\n")
        return

    for s in student_data:
        text_box.insert(END, s.get('name', '') + "\n")

    text_box.tag_configure("clickable", foreground="blue", underline=0)
    text_box.tag_add("clickable", "1.0", END)
    text_box.tag_unbind("clickable", "<Button-1>")
    text_box.tag_bind("clickable", "<Button-1>", choose_student)
    
    text_box.insert(END, "\n\n📝 Click on any student name to view details")

# k𖹭.ᐟ-----------------this is for going back to main page--------------------------$𖹭.ᐟ
def go_back_to_main():
    global graph_button
    if graph_button:
        graph_button.destroy()
        graph_button = None
    frame_switch(frame1)

def frame_switch(frame):
    global graph_button
    if graph_button and frame != frame2:
        graph_button.destroy()
        graph_button = None
    frame.tkraise()

# k𖹭.ᐟ------------------click studnet for details---------------------------$𖹭.ᐟ
def choose_student(event):
    global graph_button
    
    if graph_button:
        graph_button.destroy()
        graph_button = None
    
    index = text_box.index("@%s,%s" % (event.x, event.y))
    line_number = int(index.split(".")[0]) - 1

    student_data_local = import_studentdata()
    if 0 <= line_number < len(student_data_local):
        s = student_data_local[line_number]
        try:
            test_total = int(s.get('course1', 0)) + int(s.get('course2', 0)) + int(s.get('course3', 0))
            exam_total = int(s.get('exam', 0))
            total_marks = test_total + exam_total
            percentage = (total_marks / 160) * 100 if 160 != 0 else 0
            grade = grading(percentage)
        except Exception:
            test_total = 0
            exam_total = 0
            total_marks = 0
            percentage = 0
            grade = "N/A"

        text_box.delete("1.0", END)
        text_box.insert(
            END,
            f"Student Id: {s.get('code','')}\n"
            f"Name: {s.get('name','')}\n"
            f"Tests Total (out of 60): {test_total}\n"
            f"Exam (out of 100): {exam_total}\n"
            f"Total Marks (out of 160): {total_marks}\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Grade: {grade}\n"
            f"────────▸▸▸────────\n\n"
            f"Click the button below to view detailed performance graph:\n"
        )
        
        graph_button = Button(frame2, text="📊 View Performance Graph", 
                          font=("Arial", 14, "bold"), bg="#3498db", fg="white",
                          command=lambda student=s: show_student_graph(student))
        graph_button.place(x=500, y=600)

# k𖹭.ᐟ------------------displaying highest student score---------------------------$𖹭.ᐟ
def score_highest():
    global student_data
    student_data = import_studentdata()
    frame_switch(frame2)
    text_box.delete("1.0", END)

    if not student_data:
        text_box.insert(END, "No student data found.")
        return

    highest_student = max(
        student_data,
        key=lambda s: (int(s.get('course1', 0)) + int(s.get('course2', 0)) + int(s.get('course3', 0)) + int(s.get('exam', 0)))
    )

    test_total = int(highest_student.get('course1', 0)) + int(highest_student.get('course2', 0)) + int(highest_student.get('course3', 0))
    exam_total = int(highest_student.get('exam', 0))
    total_marks = test_total + exam_total
    percentage = (total_marks / 160) * 100 if 160 != 0 else 0
    grade = grading(percentage)

    text_box.insert(
        END,
        "🏆 HIGHEST SCORER 🏆\n\n"
        f"Student Id: {highest_student.get('code','')}\n"
        f"Name: {highest_student.get('name','')}\n"
        f"Tests Total (out of 60): {test_total}\n"
        f"Exam (out of 100): {exam_total}\n"
        f"Total Marks (out of 160): {total_marks}\n"
        f"Percentage: {percentage:.2f}%\n"
        f"Grade: {grade}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
    )

# k𖹭.ᐟ------------------displaying lowest score for student ---------------------------$𖹭.ᐟ
def score_lowest():
    global student_data
    student_data = import_studentdata()
    frame_switch(frame2)
    text_box.delete("1.0", END)

    if not student_data:
        text_box.insert(END, "No student data found.")
        return

    lowest_student = min(
        student_data,
        key=lambda s: (int(s.get('course1', 0)) + int(s.get('course2', 0)) + int(s.get('course3', 0)) + int(s.get('exam', 0)))
    )

    test_total = int(lowest_student.get('course1', 0)) + int(lowest_student.get('course2', 0)) + int(lowest_student.get('course3', 0))
    exam_total = int(lowest_student.get('exam', 0))
    total_marks = test_total + exam_total
    percentage = (total_marks / 160) * 100 if 160 != 0 else 0
    grade = grading(percentage)

    text_box.insert(
        END,
        "🔻 LOWEST SCORER 🔻\n\n"
        f"Student Id: {lowest_student.get('code','')}\n"
        f"Name: {lowest_student.get('name','')}\n"
        f"Tests Total (out of 60): {test_total}\n"
        f"Exam (out of 100): {exam_total}\n"
        f"Total Marks (out of 160): {total_marks}\n"
        f"Percentage: {percentage:.2f}%\n"
        f"Grade: {grade}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
    )

# k𖹭.ᐟ------------------ascending order for the students detial---------------------------$𖹭.ᐟ
def sort_ascending():
    global student_data
    student_data = import_studentdata()
    frame_switch(frame2)
    text_box.delete("1.0", END)

    if not student_data:
        text_box.insert(END, "No student data found.")
        return

    sorted_students = sorted(
        student_data,
        key=lambda s: (int(s.get('course1', 0)) + int(s.get('course2', 0)) + int(s.get('course3', 0)) + int(s.get('exam', 0)))
    )

    for s in sorted_students:
        test_total = int(s.get('course1', 0)) + int(s.get('course2', 0)) + int(s.get('course3', 0))
        exam_total = int(s.get('exam', 0))
        total_marks = test_total + exam_total
        percentage = (total_marks / 160) * 100 if 160 != 0 else 0
        grade = grading(percentage)

        text_box.insert(
            END,
            f"Name: {s.get('name','')}\n"
            f"Total Marks: {total_marks}/160\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Grade: {grade}\n"
            f"----------------------------------\n"
        )

# k𖹭.ᐟ------------------descending order for students details ---------------------------$𖹭.ᐟ
def sort_descending():
    global student_data
    student_data = import_studentdata()
    frame_switch(frame2)
    text_box.delete("1.0", END)

    if not student_data:
        text_box.insert(END, "No student data found.")
        return

    sorted_students = sorted(
        student_data,
        key=lambda s: (int(s.get('course1', 0)) + int(s.get('course2', 0)) + int(s.get('course3', 0)) + int(s.get('exam', 0))),
        reverse=True
    )

    for s in sorted_students:
        test_total = int(s.get('course1', 0)) + int(s.get('course2', 0)) + int(s.get('course3', 0))
        exam_total = int(s.get('exam', 0))
        total_marks = test_total + exam_total
        percentage = (total_marks / 160) * 100 if 160 != 0 else 0
        grade = grading(percentage)

        text_box.insert(
            END,
            f"Name: {s.get('name','')}\n"
            f"Total Marks: {total_marks}/160\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Grade: {grade}\n"
            f"----------------------------------\n"
        )

# k𖹭.ᐟ------------------adding new student in edit button---------------------------$𖹭.ᐟ
def add_new_std():
    global student_data
    frame_switch(frame2)
    text_box.delete("1.0", END)

    template = (
        "Fill in the student details below (use 'Field: value' format):\n\n"
        "Name: \n"
        "ID: \n"
        "Course1 (0-20): \n"
        "Course2 (0-20): \n"
        "Course3 (0-20): \n"
        "Exam (0-100): \n\n"
        "After filling the values on the right of each label, press 'Save Student'.\n"
    )
    text_box.insert(END, template)

    save_btn = Button(frame2, text="Save Student", bg="#4CAF50", fg="white",
                      font=("Arial", 14, "bold"),
                      command=lambda: save_new_std(save_btn))
    save_btn.place(x=200, y=600)

# k𖹭.ᐟ------------------this is for saving new studmet in file ---------------------------$𖹭.ᐟ
def save_new_std(btn):
    global student_data
    text = text_box.get("1.0", END).strip()
    if not text:
        messagebox.showerror("Error", "Text box is empty.")
        return

    lines = [line for line in text.splitlines() if ":" in line]
    parsed = {}

    for line in lines:
        try:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            key = key.split()[0]
            parsed[key] = value.strip()
        except Exception:
            continue

    try:
        name = parsed.get("name", "")
        if not name:
            raise ValueError("Name is required.")
        code_raw = parsed.get("id", parsed.get("code", ""))
        if not code_raw:
            raise ValueError("ID is required.")
        code = int(code_raw)

        course1 = int(parsed.get("course1", "0") or 0)
        course2 = int(parsed.get("course2", "0") or 0)
        course3 = int(parsed.get("course3", "0") or 0)
        exam    = int(parsed.get("exam", "0") or 0)

    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")
        return

    student_data = import_studentdata()

    for s in student_data:
        try:
            if int(s.get('code')) == int(code):
                messagebox.showerror("Error", f"A student with ID {code} already exists.")
                return
        except Exception:
            continue

    new_student = {
        "code": code,
        "name": name,
        "course1": course1,
        "course2": course2,
        "course3": course3,
        "exam": exam
    }

    student_data.append(new_student)

    ok, err = save_student_list_to_file(student_data)
    if not ok:
        messagebox.showerror("Error", f"Failed to save JSON: {err}")
        return

    messagebox.showinfo("Success", f"Student '{name}' added successfully!")

    student_data = import_studentdata()
    text_box.delete("1.0", END)
    veiw_studentlst()

# k𖹭.ᐟ------------------update student details---------------------------$𖹭.ᐟ
def dropdown_updatestd():
    frame_switch(frame2)
    text_box.delete("1.0", END)

    text_box.insert(END, "Select how you want to search for the student:\n")

    options = ["Name", "ID"]
    selected_option = StringVar()
    selected_option.set(options[0])

    dropdown = OptionMenu(frame2, selected_option, *options)
    dropdown.place(x=207, y=270)

    entry_label = Label(frame2, text="Enter Name or ID for the student:",bg="#B7C874", font=("Arial", 16))
    entry_label.place(x=203, y=340)
    entry = Entry(frame2, width=20,bg="#C2D86C", font=("Arial", 14))
    entry.place(x=207, y=370)

    search_btn = Button(frame2, text="Find Student", bg="#C2D86C", fg="black",
                        font=("Arial", 14, "bold"),
                        command=lambda: show_dropdown_updatestd(selected_option.get(), entry.get(), dropdown, entry_label, entry, search_btn))
    search_btn.place(x=207, y=500)

# k𖹭.ᐟ------------------updating records for each student ---------------------------$𖹭.ᐟ
def show_dropdown_updatestd(search_by, value, dropdown, entry_label, entry, btn):
    raw_value = value
    value = value.strip()
    if not value:
        text_box.insert(END, "\n❌ Please enter a Name or ID.\n")
        return

    students_list = import_studentdata()
    if not students_list:
        text_box.insert(END, "\n❌ No student records loaded.\n")
        return

    student_to_update = None
    mode = search_by.strip().lower()

    for s in students_list:
        s_code = s.get('code')
        s_name = s.get('name', '')
        code_str = str(s_code).strip() if s_code is not None else ""
        name_str = str(s_name).strip().lower() if s_name else ""

        if mode == "name" and name_str == value.lower():
            student_to_update = s
            break
        elif mode == "id":
            try:
                if code_str == value.strip() or int(code_str) == int(value):
                    student_to_update = s
                    break
            except Exception:
                pass
        if name_str == value.lower() or code_str == value:
            student_to_update = s
            break

    if student_to_update is None:
        text_box.insert(END, f"\n❌ Student '{raw_value}' not found!\n")
        sample = []
        for i, s in enumerate(students_list[:5]):
            sample.append(f"{i+1}. {s.get('code')} - {s.get('name')}")
        text_box.insert(END, "\nLoaded sample records:\n" + "\n".join(sample) + "\n")
        return

    dropdown.destroy()
    entry_label.destroy()
    entry.destroy()
    btn.destroy()

    s = student_to_update
    s_code = s.get('code', '')
    s_name = s.get('name', '')
    s_course1 = s.get('course1', '')
    s_course2 = s.get('course2', '')
    s_course3 = s.get('course3', '')
    s_exam = s.get('exam', '')

    text_box.delete("1.0", END)
    text_box.insert(END,
        f"Name: {s_name}\n"
        f"ID: {s_code}\n"
        f"Course1: {s_course1}\n"
        f"Course2: {s_course2}\n"
        f"Course3: {s_course3}\n"
        f"Exam: {s_exam}\n\n"
        "You can edit only the fields you want. Leave others as is.\n"
        "After editing, click 'Save Changes'\n"
    )

    save_btn = Button(frame2, text="Save Changes", bg="#4CAF50", fg="white",
                      font=("Arial", 14, "bold"),
                      command=lambda: save_updatedstd(student_to_update, save_btn))
    save_btn.place(x=200, y=600)

# k𖹭.ᐟ------------------saving deatils for the updated student---------------------------$𖹭.ᐟ
def save_updatedstd(student_to_update, btn):
    global student_data

    try:
        lines = text_box.get("1.0", END).splitlines()
        updated_dict = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                updated_dict[key.strip().lower()] = value.strip()

        student_to_update['course1'] = int(updated_dict.get("course1", student_to_update.get('course1', 0)))
        student_to_update['course2'] = int(updated_dict.get("course2", student_to_update.get('course2', 0)))
        student_to_update['course3'] = int(updated_dict.get("course3", student_to_update.get('course3', 0)))
        student_to_update['exam']    = int(updated_dict.get("exam", student_to_update.get('exam', 0)))
        student_to_update['name']    = updated_dict.get("name", student_to_update.get('name', ''))
        if "id" in updated_dict:
            try:
                student_to_update['code'] = int(updated_dict.get("id"))
            except Exception:
                pass

        student_data = import_studentdata()
        updated_code = int(student_to_update.get('code'))
        for i, s in enumerate(student_data):
            try:
                if int(s.get('code')) == updated_code:
                    student_data[i] = student_to_update
                    break
            except Exception:
                continue

        ok, err = save_student_list_to_file(student_data)
        if not ok:
            text_box.insert(END, f"\n❌ Failed to save JSON: {err}\n")
            return

        text_box.insert(END, f"\n✅ Student '{student_to_update.get('name')}' updated successfully!\n")
        btn.destroy()

        veiw_studentlst()

    except ValueError:
        text_box.insert(END, "\n❌ Please enter valid numeric values for courses and exam.\n")
    except Exception as e:
        text_box.insert(END, f"\n❌ Error: {e}\n")

# k𖹭.ᐟ------------------student delteing button---------------------------$𖹭.ᐟ
def delete_std():
    frame_switch(frame2)
    text_box.lift()
    text_box.delete("1.0", END)
    text_box.insert(END, "Select search method to delete a student:\n")

    choices = ["Name", "ID"]
    selected_option = StringVar(value=choices[0])

    dropdown = OptionMenu(frame2, selected_option, *choices)
    dropdown.place(x=207, y=270)

    entry_label = Label(frame2, text="Enter value:", font=("Arial", 16), bg="#b7c874")
    entry_label.place(x=203, y=340)

    entry_box = Entry(frame2, font=("Arial", 16), bg="#C2D86C", width=20)
    entry_box.place(x=207, y=370)

    search_btn = Button(
        frame2,
        text="Search",
        font=("Arial", 14, "bold"),
        bg="#3498db",
        fg="white",
        command=lambda: std_for_delete(selected_option.get(), entry_box.get(), dropdown, entry_label, entry_box, search_btn)
    )
    search_btn.place(x=207, y=500)

# k𖹭.ᐟ------------------search studnet for deleting the record---------------------------$𖹭.ᐟ
def std_for_delete(method, value, dropdown, entry_label, entry_box, search_btn):
    frame_switch(frame2)
    text_box.lift()
    text_box.delete("1.0", END)
    value = value.strip()

    if not value:
        text_box.insert(END, "❌ Please enter a value.\n")
        return

    found = None
    method_lower = method.lower()

    students = import_studentdata()
    for s in students:
        student_name = str(s.get("name", "")).strip().lower()
        student_id = str(s.get("code", "")).strip()

        if method_lower == "name" and student_name == value.lower():
            found = s
            break
        elif method_lower == "id" and student_id == value:
            found = s
            break

    if not found:
        text_box.insert(END, f"❌ No student found for '{value}'.\n")
        return

    dropdown.destroy()
    entry_label.destroy()
    entry_box.destroy()
    search_btn.destroy()

    display_deleted_record(found)

# k𖹭.ᐟ------------------display student records for deleting---------------------------$𖹭.ᐟ
def display_deleted_record(student):
    frame_switch(frame2)
    text_box.lift()
    text_box.delete("1.0", END)

    text_box.insert(END,
        f"STUDENT FOUND:\n\n"
        f"Name: {student.get('name', 'N/A')}\n"
        f"ID: {student.get('code', 'N/A')}\n"
        f"Course1: {student.get('course1', 'N/A')}\n"
        f"Course2: {student.get('course2', 'N/A')}\n"
        f"Course3: {student.get('course3', 'N/A')}\n"
        f"Exam: {student.get('exam', 'N/A')}\n\n"
        "Click DELETE to remove this student permanently.\n"
    )

    delete_btn = Button(
        frame2,
        text="DELETE STUDENT",
        font=("Arial", 16, "bold"),
        bg="red",
        fg="white",
        command=lambda: removed_student(student, delete_btn)
    )
    delete_btn.place(x=500, y=550)
    delete_btn.lift()

# k𖹭.ᐟ------------------remove student from file---------------------------$𖹭.ᐟ
def removed_student(student, btn):
    global student_data

    try:
        student_data = import_studentdata()
        student_code = student.get('code')
        new_list = [s for s in student_data if str(s.get('code')) != str(student_code)]
        ok, err = save_student_list_to_file(new_list)
        if not ok:
            text_box.insert(END, f"Error deleting student: {err}\n")
            return

        student_data = import_studentdata()
        text_box.delete("1.0", END)
        text_box.insert(END, f"Student '{student.get('name','N/A')}' deleted successfully.\n")
        btn.destroy()
        veiw_studentlst()

    except Exception as e:
        text_box.insert(END, f"Error deleting student: {e}\n")

# k𖹭.ᐟ------------------save student list to file---------------------------$𖹭.ᐟ
def save_student_list_to_file(students):
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump({"Student Details": students}, file, indent=4)
        return True, None
    except Exception as e:
        return False, str(e)

# k𖹭.ᐟ------------------this is my frame 1 (main page)---------------------------$𖹭.ᐟ
frame1 = Frame(root, width=1900, height=1000)
frame1.place(x=0, y=0)

# k𖹭.ᐟ------------------exit button for frame 1---------------------------$𖹭.ᐟ
btn11 = ImageTk.PhotoImage(Image.open("ex3/btn/exit.png").resize((61, 30)))
Button(frame1, image=btn11, borderwidth=0, highlightthickness=0,
bg=frame1["bg"], activebackground=frame1["bg"],
command=lambda : frame_switch(frame3)).place(x=200, y=108)

# k𖹭.ᐟ------------------background image for frame 1---------------------------$𖹭.ᐟ
try:
    frame1_bg = ImageTk.PhotoImage(Image.open("ex3/bgpics/pg1.jpg").resize((1280, 650)))
    Label(frame1, image=frame1_bg).place(x=0, y=0)
except Exception:
    pass

# k𖹭.ᐟ------------------view menu button---------------------------$𖹭.ᐟ
view_menu = Frame(frame1, bg="white")
try:
    view_img = ImageTk.PhotoImage(Image.open("ex3/btn/view.png").resize((185, 50)))
    view_btn = Button(frame1, image=view_img, borderwidth=0, highlightthickness=0, bg=frame1["bg"])
except Exception:
    view_btn = Button(frame1, text="View", borderwidth=0, highlightthickness=0, bg=frame1["bg"])
view_btn.place(x=395, y=27)

# k𖹭.ᐟ------------------view all button---------------------------$𖹭.ᐟ
try:
    view_all_img = ImageTk.PhotoImage(Image.open("ex3/btn/view,1.png").resize((170, 50)))
    Button(view_menu, image=view_all_img, borderwidth=0, bg=view_menu["bg"],activebackground=view_menu["bg"], 
        command=lambda: [view_menu.place_forget(), veiw_studentlst()]).pack(fill="x")
except Exception:
    Button(view_menu, text="View All", borderwidth=0, bg=view_menu["bg"],
           command=lambda: [view_menu.place_forget(), veiw_studentlst()]).pack(fill="x")

# k𖹭.ᐟ------------------view individual student button---------------------------$𖹭.ᐟ
try:
    view_one_img = ImageTk.PhotoImage(Image.open("ex3/btn/view,2.png").resize((170, 50)))
    Button(view_menu, image=view_one_img, borderwidth=0, bg=view_menu["bg"],activebackground=view_menu["bg"], 
        command=lambda: [view_menu.place_forget(), veiw_indivisual()]).pack(fill="x")
except Exception:
    Button(view_menu, text="View One", borderwidth=0, bg=view_menu["bg"],
           command=lambda: [view_menu.place_forget(), veiw_indivisual()]).pack(fill="x")

# k𖹭.ᐟ------------------view button hover effects---------------------------$𖹭.ᐟ
view_btn.bind("<Enter>", lambda e: show_menu(view_menu, view_btn))
view_btn.bind("<Leave>", lambda e: root.after(200, lambda: hide_menu(view_menu, view_btn)))
view_menu.bind("<Leave>", lambda e: hide_menu(view_menu, view_btn))

# k𖹭.ᐟ------------------scores menu button---------------------------$𖹭.ᐟ
scores_menu = Frame(frame1, bg="white", bd=0, highlightthickness=0)
try:
    scores_img = ImageTk.PhotoImage(Image.open("ex3/btn/score.png").resize((185, 50)))
    scores_btn = Button(frame1, image=scores_img, borderwidth=0, highlightthickness=0, bg=frame1["bg"])
except Exception:
    scores_btn = Button(frame1, text="Scores", borderwidth=0, highlightthickness=0, bg=frame1["bg"])
scores_btn.place(x=590, y=27)

# k𖹭.ᐟ------------------highest score button---------------------------$𖹭.ᐟ
try:
    scores_high_img = ImageTk.PhotoImage(Image.open("ex3/btn/score,1.png").resize((170, 50)))
    Button(scores_menu, image=scores_high_img, borderwidth=0, bg=scores_menu["bg"],activebackground=scores_menu["bg"], 
        command=lambda: [scores_menu.place_forget(), score_highest()]).pack(fill="x")
except Exception:
    Button(scores_menu, text="Highest", borderwidth=0, bg=scores_menu["bg"],activebackground=scores_menu["bg"], 
        command=lambda: [scores_menu.place_forget(), score_highest()]).pack(fill="x")

# k𖹭.ᐟ------------------lowest score button---------------------------$𖹭.ᐟ
try:
    scores_low_img = ImageTk.PhotoImage(Image.open("ex3/btn/score,2.png").resize((170, 50)))
    Button(scores_menu, image=scores_low_img, borderwidth=0, bg=scores_menu["bg"],activebackground=scores_menu["bg"], 
        command=lambda: [scores_menu.place_forget(), score_lowest()]).pack(fill="x")
except Exception:
    Button(scores_menu, text="Lowest", borderwidth=0, bg=scores_menu["bg"],activebackground=scores_menu["bg"], 
        command=lambda: [scores_menu.place_forget(), score_lowest()]).pack(fill="x")

# k𖹭.ᐟ------------------scores button hover effects---------------------------$𖹭.ᐟ
scores_btn.bind("<Enter>", lambda e: show_menu(scores_menu, scores_btn))
scores_btn.bind("<Leave>", lambda e: root.after(200, lambda: hide_menu(scores_menu, scores_btn)))
scores_menu.bind("<Leave>", lambda e: hide_menu(scores_menu, scores_btn))

# k𖹭.ᐟ------------------sort button in score button---------------------------$𖹭.ᐟ
scores_sub_menu = Frame(frame1, bg="white", bd=1, relief="solid")
try:
    scores_sort_img = ImageTk.PhotoImage(Image.open("ex3/btn/sort.png").resize((170, 50)))
    sort_btn = Button(scores_menu, image=scores_sort_img, borderwidth=0,bg=scores_menu["bg"], activebackground=scores_menu["bg"])
    sort_btn.pack(fill="x")
except Exception:
    sort_btn = Button(scores_menu, text="Sort", borderwidth=0,bg=scores_menu["bg"], activebackground=scores_menu["bg"])
    sort_btn.pack(fill="x")

# k𖹭.ᐟ------------------ascending sort button---------------------------$𖹭.ᐟ
try:
    score_top5_img = ImageTk.PhotoImage(Image.open("ex3/btn/sort,1.png").resize((170, 50)))
    Button(scores_sub_menu, image=score_top5_img, borderwidth=0, bg="white", activebackground="white", 
    command=lambda: [scores_sub_menu.place_forget(), sort_ascending()]).pack(fill="x")
except Exception:
    Button(scores_sub_menu, text="Ascending", borderwidth=0, bg="white", activebackground="white", 
    command=lambda: [scores_sub_menu.place_forget(), sort_ascending()]).pack(fill="x")

# k𖹭.ᐟ------------------descending sort button---------------------------$𖹭.ᐟ
try:
    score_bottom5_img = ImageTk.PhotoImage(Image.open("ex3/btn/sort,2.png").resize((170, 50)))
    Button(scores_sub_menu, image=score_bottom5_img, borderwidth=0, bg="white",activebackground="white", 
    command=lambda: [scores_sub_menu.place_forget(), sort_descending()]).pack(fill="x")
except Exception:
    Button(scores_sub_menu, text="Descending", borderwidth=0, bg="white",activebackground="white", 
    command=lambda: [scores_sub_menu.place_forget(), sort_descending()]).pack(fill="x")

# k𖹭.ᐟ------------------sort button hover effects---------------------------$𖹭.ᐟ
sort_btn.bind("<Enter>", lambda e: show_sub_menu(scores_sub_menu, sort_btn))
sort_btn.bind("<Leave>", lambda e: root.after(200, lambda: hide_sub_menu(scores_sub_menu, sort_btn)))
scores_sub_menu.bind("<Leave>", lambda e: hide_sub_menu(scores_sub_menu, sort_btn))

# k𖹭.ᐟ------------------edit menu button---------------------------$𖹭.ᐟ
edit_menu = Frame(frame1, bg="white", bd=1, relief="solid")
try:
    edit_img = ImageTk.PhotoImage(Image.open("ex3/btn/edit.png").resize((185, 50)))
    edit_btn = Button(frame1, image=edit_img, borderwidth=0, highlightthickness=0, bg=frame1["bg"])
except Exception:
    edit_btn = Button(frame1, text="Edit", borderwidth=0, highlightthickness=0, bg=frame1["bg"])
edit_btn.place(x=785, y=27)

# k𖹭.ᐟ------------------add new student button---------------------------$𖹭.ᐟ
try:
    edit_add_img = ImageTk.PhotoImage(Image.open("ex3/btn/edit,1.png").resize((170, 50)))
    Button(edit_menu, image=edit_add_img, borderwidth=0, bg=edit_menu["bg"],activebackground=edit_menu["bg"], 
        command=lambda: [edit_menu.place_forget(), add_new_std()]).pack(fill="x")
except Exception:
    Button(edit_menu, text="Add", borderwidth=0, bg=edit_menu["bg"],activebackground=edit_menu["bg"], 
        command=lambda: [edit_menu.place_forget(), add_new_std()]).pack(fill="x")

# k𖹭.ᐟ------------------update student button---------------------------$𖹭.ᐟ
try:
    edit_update_img = ImageTk.PhotoImage(Image.open("ex3/btn/edit,2.png").resize((170, 50)))
    Button(edit_menu, image=edit_update_img, borderwidth=0, bg=edit_menu["bg"],activebackground=edit_menu["bg"], 
        command=lambda: [edit_menu.place_forget(), dropdown_updatestd()]).pack(fill="x")
except Exception:
    Button(edit_menu, text="Update", borderwidth=0, bg=edit_menu["bg"],activebackground=edit_menu["bg"], 
        command=lambda: [edit_menu.place_forget(), dropdown_updatestd()]).pack(fill="x")

# k𖹭.ᐟ------------------delete student button---------------------------$𖹭.ᐟ
try:
    edit_delete_img = ImageTk.PhotoImage(Image.open("ex3/btn/edit,3.png").resize((170, 50)))
    Button(edit_menu, image=edit_delete_img, borderwidth=0, bg=edit_menu["bg"],activebackground=edit_menu["bg"], 
        command=lambda: [edit_menu.place_forget(), delete_std()]).pack(fill="x")
except Exception:
    Button(edit_menu, text="Delete", borderwidth=0, bg=edit_menu["bg"],activebackground=edit_menu["bg"], 
        command=lambda: [edit_menu.place_forget(), delete_std()]).pack(fill="x")

# k𖹭.ᐟ------------------edit button hover effects---------------------------$𖹭.ᐟ
edit_btn.bind("<Enter>", lambda e: show_menu(edit_menu, edit_btn))
edit_btn.bind("<Leave>", lambda e: root.after(200, lambda: hide_menu(edit_menu, edit_btn)))
edit_menu.bind("<Leave>", lambda e: hide_menu(edit_menu, edit_btn))

# k𖹭.ᐟ------------------help menu button---------------------------$𖹭.ᐟ
help_menu = Frame(frame1, bg="white", bd=1, relief="solid")
try:
    help_img = ImageTk.PhotoImage(Image.open("ex3/btn/help.png").resize((185, 50)))
    help_btn = Button(frame1, image=help_img, borderwidth=0, highlightthickness=0, bg=frame1["bg"])
except Exception:
    help_btn = Button(frame1, text="Help", borderwidth=0, highlightthickness=0, bg=frame1["bg"])
help_btn.place(x=200, y=27)

# k𖹭.ᐟ------------------about button---------------------------$𖹭.ᐟ
try:
    help_abt_img = ImageTk.PhotoImage(Image.open("ex3/btn/about.png").resize((170, 50)))
    Button(help_menu, image=help_abt_img, borderwidth=0, bg=help_menu["bg"],activebackground=help_menu["bg"],
        command=lambda: frame_switch(frame4)).pack(fill="x")
except Exception:
    Button(help_menu, text="About", borderwidth=0, bg=help_menu["bg"],activebackground=help_menu["bg"],
            command=lambda: frame_switch(frame4)).pack(fill="x")

# k𖹭.ᐟ------------------help button hover effects---------------------------$𖹭.ᐟ
help_btn.bind("<Enter>", lambda e: show_menu(help_menu, help_btn))
help_btn.bind("<Leave>", lambda e: root.after(200, lambda: hide_menu(help_menu, help_btn)))
help_menu.bind("<Leave>", lambda e: hide_menu(help_menu, help_btn))

# k𖹭.ᐟ------------------show menu on hover---------------------------$𖹭.ᐟ
def show_menu(menu, btn):
    menu.place(x=btn.winfo_x(), y=btn.winfo_y() + btn.winfo_height())

# k𖹭.ᐟ------------------hide menu when its not hovring---------------------------$𖹭.ᐟ
def hide_menu(menu, btn):
    x, y = root.winfo_pointerx(), root.winfo_pointery()

    if not (btn.winfo_rootx() <= x <= btn.winfo_rootx() + btn.winfo_width() and
            btn.winfo_rooty() <= y <= btn.winfo_rooty() + btn.winfo_height()) and \
       not (menu.winfo_rootx() <= x <= menu.winfo_rootx() + menu.winfo_width() and
            menu.winfo_rooty() <= y <= menu.winfo_rooty() + menu.winfo_height()):
        menu.place_forget()

# k𖹭.ᐟ------------------show sub menu on hover---------------------------$𖹭.ᐟ
def show_sub_menu(menu, parent_btn):
    menu.place(x=parent_btn.winfo_rootx() - frame1.winfo_rootx() + parent_btn.winfo_width(),
               y=parent_btn.winfo_rooty() - frame1.winfo_rooty())

# k𖹭.ᐟ------------------hide sub menu when not hovering---------------------------$𖹭.ᐟ
def hide_sub_menu(menu, parent_btn):
    x, y = root.winfo_pointerx(), root.winfo_pointery()

    if not (menu.winfo_rootx() <= x <= menu.winfo_rootx() + menu.winfo_width() and
            menu.winfo_rooty() <= y <= menu.winfo_rooty() + menu.winfo_height()) and \
       not (parent_btn.winfo_rootx() <= x <= parent_btn.winfo_rootx() + parent_btn.winfo_width() and
            parent_btn.winfo_rooty() <= y <= parent_btn.winfo_rooty() + parent_btn.winfo_height()):
        menu.place_forget()

# k𖹭.ᐟ------------------this is my frame 2 for displaying student details page---------------------------$𖹭.ᐟ
frame2 = Frame(root, width=1900, height=1000)
frame2.place(x=0, y=0)

# k𖹭.ᐟ------------------background image for frame 2---------------------------$𖹭.ᐟ
try:
    frame2_bg = ImageTk.PhotoImage(Image.open("ex3/bgpics/pg2.jpg").resize((1280, 650)))
    Label(frame2, image=frame2_bg).place(x=0, y=0)
except Exception:
    pass

# k𖹭.ᐟ------------------creating text box to show student deatils---------------------------$𖹭.ᐟ
text_box = Text(frame2, width=80, height=20, font=("Arial", 14), bg="#b7c874", fg="black")
text_box.place(x=200, y=230)

# k𖹭.ᐟ------------------exit button for frame 2---------------------------$𖹭.ᐟ
btn2 = ImageTk.PhotoImage(Image.open("ex3/btn/exit.png").resize((64, 30)))
Button(frame2, image=btn2, borderwidth=0, highlightthickness=0,
bg=frame2["bg"], activebackground=frame2["bg"],
command=lambda : frame_switch(frame3)).place(x=260, y=46)

# k𖹭.ᐟ------------------back button for frame 2---------------------------$𖹭.ᐟ
btn2a = ImageTk.PhotoImage(Image.open("ex3/btn/back2.png").resize((61, 30)))
Button(frame2, image=btn2a, borderwidth=0, highlightthickness=0,
bg=frame2["bg"], activebackground=frame2["bg"],
command=lambda : frame_switch(frame1)).place(x=75, y=48)

# k𖹭.ᐟ------------------frame 3 exit page(yes or no)---------------------------$𖹭.ᐟ
frame3 = Frame(root, width=1900, height=1000)
frame3.place(x=0, y=0)

# k𖹭.ᐟ------------------background image for frame 3---------------------------$𖹭.ᐟ
frame3bg = ImageTk.PhotoImage(Image.open("ex3/bgpics/pg3.jpg").resize((1280, 650)))
Label(frame3, image=frame3bg).place(x=0, y=0)

# k𖹭.ᐟ------------------yes button to exit---------------------------$𖹭.ᐟ
btn3 = ImageTk.PhotoImage(Image.open("ex3/btn/yes.png").resize((70, 100)))
Button(frame3, image=btn3, borderwidth=0, highlightthickness=0,
bg=frame3["bg"], activebackground=frame3["bg"],
command= root.destroy).place(x=815, y=295)

# k𖹭.ᐟ------------------no button to go back to frame 1---------------------------$𖹭.ᐟ
btn3a = ImageTk.PhotoImage(Image.open("ex3/btn/no.png").resize((70, 90)))
Button(frame3, image=btn3a, borderwidth=0, highlightthickness=0,
bg=frame3["bg"], activebackground=frame3["bg"],
command=lambda : frame_switch(frame1)).place(x=815, y=450)

# k𖹭.ᐟ------------------frame 4 about page---------------------------$𖹭.ᐟ
frame4 = Frame(root, width=1900, height=1000)
frame4.place(x=0, y=0)

# k𖹭.ᐟ------------------background image for frame 4---------------------------$𖹭.ᐟ
frame4bg = ImageTk.PhotoImage(Image.open("ex3/bgpics/pg4.jpg").resize((1280, 650)))
Label(frame4, image=frame4bg).place(x=0, y=0)

# k𖹭.ᐟ------------------back button for frame 4---------------------------$𖹭.ᐟ
btn4 = ImageTk.PhotoImage(Image.open("ex3/btn/back2.png").resize((61, 30)))
Button(frame4, image=btn4, borderwidth=0, highlightthickness=0,
bg=frame4["bg"], activebackground=frame4["bg"],
command=lambda : frame_switch(frame1)).place(x=1100, y=38)

# k𖹭.ᐟ------------------show frame1 at start---------------------------$𖹭.ᐟ
frame_switch(frame1)

# k𖹭.ᐟ------------------load student data at start---------------------------$𖹭.ᐟ
student_data = import_studentdata()

# k𖹭.ᐟ------------------start the application---------------------------$𖹭.ᐟ
root.mainloop()