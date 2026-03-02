from tkinter import *
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox, ttk
import sqlite3 as sq
conn = sq.connect("DrivingCourseRegistration.db")
c= conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    security_questions TEXT NOT NULL,
    security_answer TEXT NOT NULL
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()
conn.close()
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"  
current_user_id = None
current_user_name = None
conn = sq.connect("DrivingCourseRegistration.db")
c = conn.cursor()
c.execute("SELECT id FROM admins WHERE username=?", (ADMIN_USERNAME,))
if not c.fetchone():
    c.execute(
        "INSERT INTO admins (name, username, password) VALUES (?, ?, ?)",
        ("Administrator", ADMIN_USERNAME, ADMIN_PASSWORD)
    )
    conn.commit()
    conn.close()
root = Tk()
root.title("Driving Course Registration System")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("Title.TLabel", font=("Arial", 24, "bold"))
style.configure("Subtitle.TLabel", font=("Arial", 14))
style.configure("TButton", font=("Arial", 11), padding=5)
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def create_centered_frame(parent):
    frame = ttk.Frame(parent)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    return frame

def create_form_entry(parent, label_text, show=None):
    ttk.Label(parent, text=label_text).pack(anchor="w", pady=(10, 2))
    entry = ttk.Entry(parent, width=30, show=show)
    entry.pack(fill="x")
    return entry
icons = {}
def onclick_forgetps():
    conn = sq.connect("DrivingCourseRegistration.db")
    c= conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (current_user_id,))
    record = c.fetchone()
    security_question = str(record[4])
    correct_answer = str(record[5]) 
    answer = simpledialog.askstring("Security Question", security_question, show="*")
    global top, new, conf
    if answer == correct_answer:
        top = Toplevel()
        top.title("Change password")
        top.geometry("300x400")

        new= Entry(top, width= 30)
        new.grid(row=0, column=1, padx=20, pady=(10,0))

        conf = Entry(top, width= 30)
        conf.grid(row=1, column=1)

    Button(top, text="Save", command=updateps).grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

def updateps():
    if not new.get():
        messagebox.showwarning("Input Error", "New password is required",parent=top)
        return
    if not conf.get():
        messagebox.showwarning("Input Error", "Confirmation of entered password is required",parent=top)
        return
    if new.get() != conf.get():
        messagebox.showwarning("Input Error","Passwords confirmation not matched")
        return
    
    conn = sq.connect("DrivingCourseRegistration.db")
    c= conn.cursor()

    data = (new.get(),current_user_id)
    c.execute("UPDATE users SET password=? WHERE username= ?", data)
    messagebox.showinfo("Records", "Updated Successfully")
    conn.commit()
    conn.close()
    login_page()
    top.destroy()

def onclick_forgetps():

    username = simpledialog.askstring("username", "Enter your username: ")

    if not username.strip():
        messagebox.showerror("Input Error", "Please enter a Reservation ID!")
        return
        
    conn = sq.connect("DrivingCourseRegistration.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username.strip(),))
    record = c.fetchone()

    if not record:
        messagebox.showerror("Error", "User not found")
        return
    
    conn.close()

    security_question = str(record[4])  
    correct_answer = str(record[5])     
    answer = simpledialog.askstring("Security Question", security_question)

    if answer is None:
        return 

    if answer.lower() == correct_answer.lower():
        top = Toplevel()
        top.title("Change Password")
        top.geometry("300x200")
        ttk.Label(top, text="New Password").grid(row=0, column=0, padx=10, pady=10)
        new = ttk.Entry(top, width=30, show="*")
        new.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(top, text="Confirm Password").grid(row=1, column=0, padx=10, pady=10)
        conf = ttk.Entry(top, width=30, show="*")
        conf.grid(row=1, column=1, padx=10, pady=10)
        def save_password():
            if not new.get() or not conf.get():
                messagebox.showwarning("Input Error", "Fill all fields", parent=top)
                return
            if new.get() != conf.get():
                messagebox.showwarning("Input Error", "Passwords do not match", parent=top)
                return
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
            c.execute("UPDATE users SET password=? WHERE username=?", (new.get(), username.strip()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Password updated successfully", parent=top)
            top.destroy()

        ttk.Button(top, text="Save", command=save_password).grid(row=2, column=0, columnspan=2, pady=20)

    else:
        messagebox.showerror("Error", "Incorrect answer to security question")

def login_page():
    clear_window()
    frame = create_centered_frame(root)
    ttk.Label(frame, text="Driving Course Registration", style="Title.TLabel").pack(pady=(0, 5))
    ttk.Label(frame, text="Login", style="Subtitle.TLabel").pack(pady=(0, 20))

    username_entry = create_form_entry(frame, "Username")
    password_entry = create_form_entry(frame, "Password", show="*")

    ttk.Label(frame, text="Login as:").pack(anchor="w", pady=(15,5))
    role_var = StringVar(value="user")
    def toggle_signup():
        if role_var.get() == "user":
            signup_btn.pack(pady=5)
        else:
            signup_btn.pack_forget()

    ttk.Radiobutton(frame, text="User", variable=role_var, value="user", command=toggle_signup).pack(side="left", padx=10)
    ttk.Radiobutton(frame, text="Admin", variable=role_var, value="admin", command=toggle_signup).pack(side="left", padx=10)

    def login():
        global current_user_id, current_user_name
        username = username_entry.get().strip()
        password = password_entry.get()
        role = role_var.get()
        if not username or not password:
            messagebox.showerror("Error", "Fill all fields")
            return
        if role == "user":
            conn= sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()
            c.execute("SELECT id, name FROM users WHERE username=? AND password=?", (username, password))
            result = c.fetchone()
            conn.close()
            if result:
                current_user_id, current_user_name = result
                
            else:
                messagebox.showerror("Error", "Invalid credentials")
        else:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                current_user_name = "Administrator"
        
            else:
                messagebox.showerror("Error", "Invalid admin credentials")  
    ttk.Button(frame, text="Login", command=login, width=20).pack(pady=5)
    signup_btn = ttk.Button(frame, text="Sign Up", command=signup_page, width=20)
    signup_btn.pack(pady=5)
    forgetps_btn = ttk.Button(frame, text="forgot password", width= 20, command=onclick_forgetps)
    forgetps_btn.pack(pady=5)
def signup_page():
    clear_window()
    frame = create_centered_frame(root)
    ttk.Label(frame, text="Create Account", style="Title.TLabel").pack(pady=(0,20))

    name_entry = create_form_entry(frame, "Full Name")
    username_entry = create_form_entry(frame, "Username")
    password_entry = create_form_entry(frame, "Password", show="*")
    confirm_entry = create_form_entry(frame, "Confirm Password", show="*")

    global clicked_security_question
    clicked_security_question = StringVar(value="--- Security Question ---")
    OptionMenu(frame, clicked_security_question, "What's Your Hobby?", "What's Your Favourite Color?", "What's Lucky Number?").pack(side="left", padx=5)
    security_answer = create_form_entry(frame, "Security Answer", show="*")

    def signup():
        name = name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get()
        confirm = confirm_entry.get()
        sec_q = clicked_security_question.get()
        sec_a = security_answer.get().strip()

        if not name or not username or not password or not sec_a:
            messagebox.showerror("Error", "Fill all fields")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        try:
            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()
            c.execute("INSERT INTO users (name, username, password, security_questions,security_answer) VALUES (?, ?, ?, ?, ?)",
                           (name, username, password, sec_q, sec_a))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created")
            login_page()
        except sq.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    ttk.Button(frame, text="Create Account", command=signup, width=20).pack(pady=5)
    ttk.Button(frame, text="Back to Login", command=login_page, width=20).pack(pady=5)

if __name__ == "__main__":
    login_page()
    root.mainloop()