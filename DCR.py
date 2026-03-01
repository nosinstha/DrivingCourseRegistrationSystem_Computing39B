from tkinter import *
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox, ttk
import sqlite3 as sq

# ==========================
# DATABASE SETUP
# ==========================

conn = sq.connect("DrivingCourseRegistration.db")
c= conn.cursor()

# Create tables
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


# TRAINER TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS trainer (
    trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trainer_name TEXT,
    phone_number TEXT,
    gmail TEXT,
    vehicle TEXT,
    duration TEXT,
    time_shift TEXT,
    seats INTEGER     
)
""")

# RESERVATION TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    phone_number TEXT,
    gmail TEXT,
    trainer_id INTEGER,
    user_id INTEGER,
          
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
conn.commit()
conn.close()

# ==========================
# GLOBAL VARIABLES
# ==========================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"  # Fixed admin password

current_user_id = None
current_user_name = None

# Ensure admin exists
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




# ==========================
# MAIN WINDOW
# ==========================

root = Tk()
root.title("Driving Course Registration System")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("Title.TLabel", font=("Arial", 24, "bold"))
style.configure("Subtitle.TLabel", font=("Arial", 14))
style.configure("TButton", font=("Arial", 11), padding=5)





# ==========================
# UTILITY FUNCTIONS
# ==========================

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
# ==========================
# DASHBOARD FUNCTIONS
# ==========================

def logout():
    global current_user_id, current_user_name
    current_user_id = None
    current_user_name = None
    login_page()


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

    security_question = str(record[4])  # security_questions column
    correct_answer = str(record[5])     # security_answer column

    answer = simpledialog.askstring("Security Question", security_question)

    if answer is None:
        return  # User cancelled

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



def onclick_changeps():

    c.execute("SELECT * FROM users WHERE username=?", (current_user_name,))
    record = c.fetchone()

    security_question = str(record[4])  # security_questions column
    correct_answer = str(record[5])     # security_answer column

    answer = simpledialog.askstring("Security Question", security_question)

    if answer is None:
        return  # User cancelled

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

            data= (new.get(), current_user_name)
            c.execute("UPDATE users SET password=? WHERE username=?", data)

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
        # Show Sign Up only if role is user
        if role_var.get() == "user":
            signup_btn.pack(pady=5)
            forgetps_btn.pack(pady=5)
        else:
            signup_btn.pack_forget()
            forgetps_btn.pack_forget()

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
            c.execute("SELECT id, username FROM users WHERE username=? AND password=?", (username, password))
            result = c.fetchone()
            conn.close()

            if result:
                current_user_id, current_user_name = result
                DCR_user()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        else:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                current_user_name = "Administrator"
                DCR_admin()
            else:
                messagebox.showerror("Error", "Invalid admin credentials")

    # Only one set of buttons
    ttk.Button(frame, text="Login", command=login, width=20).pack(pady=5)
    signup_btn = ttk.Button(frame, text="Sign Up", command=signup_page, width=20)
    signup_btn.pack(pady=5)
    forgetps_btn = ttk.Button(frame, text="forgot password", command=onclick_forgetps, width= 20)
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

# ===== KEEP IMAGE REFERENCES (CRITICAL FIX) =====
icons = {}

def DCR_admin():
    clear_window()
    # ----------- SIDE FRAME --------------
    sidebar = Frame(root,bg="#ffffff",bd=1,relief="solid",width=140)
    sidebar.pack(side=LEFT,fill="y")
    
    def reset_button_color():
        home_btn.config(bg="#ffffff")
        record_btn.config(bg="#ffffff")
        trainer_btn.config(bg="#ffffff")

    def clear_main_area():
        for widget in root.winfo_children():
            if widget != sidebar:
                widget.destroy()

                
    def onclick_home_btn():
        reset_button_color()
        home_btn.config(bg="#6a88ff")
        clear_main_area()
        
        # ---------------- HEADER ----------------
        header = Frame(root, bg="#0f1b4c")
        header.pack(fill="x")
        
        Label(header, text="Hi Admin, Welcome !",
              font=("Josefin Sans", 22, "bold"),
              fg="#ffffff", bg="#0f1b4c").pack(pady=20)
        
        # ---------------- FILTER ----------------
        filter = Frame(root, bg="#939e2d")
        filter.pack(fill="x", pady=5)
        
        Label(filter, text="Filter :",
              font=("Inter", 16, "bold"),
              bg="#939e2d", fg="#1D1D1D").pack(side=LEFT, padx=20, pady=40)
        
        global clicked_vehicle, clicked_course_package, clicked_time_shift, clicked_course_category
        clicked_course_category = StringVar(value="---Course Category---")
        OptionMenu(filter, clicked_course_category, "Fully Booked", "Unbooked").pack(side=LEFT, padx=5)
        
        clicked_vehicle = StringVar(value="---Vehicle---")
        OptionMenu(filter, clicked_vehicle, "car", "van", "scooter", "motorbike").pack(side=LEFT, padx=5)
        
        clicked_course_package = StringVar(value="---Course Package---")
        OptionMenu(filter, clicked_course_package, "7 Days", "15 Days", "30 Days", "3 Months").pack(side=LEFT, padx=5)
        
        clicked_time_shift = StringVar(value="---Time Shift---")
        OptionMenu(filter, clicked_time_shift, "8am-10am", "10am-12pm", "12pm-2pm", "2pm-4pm").pack(side=LEFT, padx=5)



        
        # ---------------- CONTENT AREA ----------------
        content = Frame(root, bg="#ffffff", bd=1, relief="solid")
        content.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        
        content_canvas = Canvas(content, bg="#ffffff", highlightthickness=0)
        content_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(content, orient=VERTICAL, command=content_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        content_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollable_frame = Frame(content_canvas, bg="#ffffff")
        canvas_window = content_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        content_canvas.bind("<Configure>", lambda e:
            content_canvas.itemconfig(canvas_window, width=e.width))
        
        scrollable_frame.bind("<Configure>", lambda e:
            content_canvas.configure(scrollregion=content_canvas.bbox("all")))
        

        
        
        # ---------------- QUERY ----------------
        def query():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
                
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
            c.execute("SELECT * FROM trainer")
            records = c.fetchall()
            
            found = False
            for record in records:
                trainer_id = record[0]
                seats = int(record[7])
                
                c.execute("SELECT COUNT(*) FROM reservations WHERE trainer_id=?", (trainer_id,))
                reserve_count = c.fetchone()[0]

                     
                category = "Fully Booked" if reserve_count >= seats else "Unbooked"
                
               
                if clicked_course_category.get() not in ("---Course Category---", category):
                        continue
                if clicked_vehicle.get() not in ("---Vehicle---", record[4]):
                        continue
                if clicked_course_package.get() not in ("---Course Package---", record[5]):
                        continue
                if clicked_time_shift.get() not in ("---Time Shift---", record[6]):
                        continue

                found = True

                card = Frame(scrollable_frame, bg="#0f1b4c")
                card.pack(fill="x", padx=15, pady=10)

                card.columnconfigure(0, weight=1)
                card.columnconfigure(1, weight=0)

                details = Frame(card, bg="#0f1b4c")
                details.grid(row=0, column=0, sticky="w", padx=20, pady=15)

                Label(details, text=f"Trainer : {record[1]}\n",
                      font=("Inter", 16, "bold"),
                      fg="#ffffff", bg="#0f1b4c").pack(anchor="w")

                Label(details,
                  text=(f"Vehicle     : {record[4]}\n"
                        f"Package     : {record[5]}\n"
                        f"Time Shift  : {record[6]}\n"
                        f"Status      : {category}\n\n"
                        f"Phone Number: {record[2]}\n"
                        f"Gmail       : {record[3]}\n\n"),
                  font=("Inter", 10),
                  fg="#e0e0e0",
                  bg="#0f1b4c",
                  justify=LEFT).pack(anchor="w", pady=6)
                
                Label(details, text=f"Seats Left  : {seats - reserve_count}\n",
                      font=("Inter", 12, "bold"),
                      fg="#ffffff", bg="#0f1b4c").pack(anchor="w")

                action = Frame(card, bg="#0f1b4c")
                action.grid(row=0, column=1, sticky="e", padx=25)

                if category == "Unbooked":
                    Button(action, text="Book Course",
                       bg="#DA07C4", fg="#FFFFFF",
                       font=("Inter", 10, "bold"),
                       bd=0, padx=18, pady=6,
                       command=lambda tid=trainer_id: open_booking(tid)).pack()
                else:
                    Label(action, text="FULL",
                      fg="red", bg="#0f1b4c",
                      font=("Inter", 10, "bold")).pack(side=RIGHT)

            conn.close()

            if not found:
                Label(scrollable_frame, text="No matching records found.",
                  fg="red", bg="#FFFFFF",
                  font=("Inter", 16, "bold")).pack(pady=100)
        query()

        Button(filter, text="Search",
           bg="#830404", fg="#ffffff",
           font=("Inter", 10, "bold"),
           command=query).pack(side=LEFT, padx=8)
    
        def open_booking(trainer_id):
            top = Toplevel()
            top.title("Book Seat")
            top.geometry("350x420")
            
            Label(top, text="Your Full Name :").pack(pady=(10, 0))
            reserver_name= Entry(top, width=30)
            reserver_name.pack()
        
            Label(top, text="Phone Number :").pack(pady=(10, 0))
            reserver_phoneno = Entry(top, width=30)
            reserver_phoneno.pack()
        
            Label(top, text="Gmail :").pack(pady=(10, 0))
            reserver_gmail = Entry(top, width=30)
            reserver_gmail.pack()

        
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
            c.execute("SELECT * FROM trainer WHERE trainer_id=?", (trainer_id,))
            t = c.fetchone()
            conn.close()
        
            Label(top, text=f"\nTrainer: {t[1]}").pack()
            Label(top, text=f"Vehicle: {t[4]}").pack()
            Label(top, text=f"Package: {t[5]}").pack()
            Label(top, text=f"Time Shift: {t[6]}").pack()

        
            def save():
                conn = sq.connect("DrivingCourseRegistration.db")
                c = conn.cursor()
 
                if not reserver_name.get():
                    messagebox.showwarning("Input Error", "Name is required",parent=top)
                    return
    
                if not reserver_gmail.get():
                    messagebox.showwarning("Input Error", "Email is required",parent=top)
                    return
            
                if "@gmail.com" not in reserver_gmail.get():
                    messagebox.showwarning("Input Error", "Invalid Gmail ID. Please enter the domain '@gmail.com' as well",parent=top)
                    return
            
                if not reserver_phoneno.get():
                    messagebox.showwarning("Input Error", "Phone number is required",parent=top)
                    return
            
                if len(reserver_phoneno.get())!=10 or not reserver_phoneno.get().isdigit():
                    messagebox.showwarning("Input Error", "Invalid Phone Number",parent=top)
                    return
            
                c.execute("""
                    INSERT INTO reservations (full_name, phone_number, gmail, trainer_id)
                    VALUES (?, ?, ?, ?)
                    """, (
                        reserver_name.get().title(),
                        reserver_phoneno.get(),
                        reserver_gmail.get(),
                        trainer_id
                    ))
            
                conn.commit()
                conn.close()
            
                messagebox.showinfo("Success", "Course booked successfully!")
                top.destroy()
            Button(
                top,
                text="Save Booking",
                bg="#000000",
                fg="#ffffff",
                padx=30,
                pady=6,
                command=save
            ).pack(pady=20)
            

    def onclick_record_btn():
        reset_button_color()
        clear_main_area()

        record_btn.config(bg="#6a88ff")

        # ---------------- CRUD FUNCTIONS ----------------
        def add():
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")

            if not Name.get():
                messagebox.showwarning("Input Error", "Name is required")
                return
            if not Gmail.get():
                messagebox.showwarning("Input Error", "Email is required")
                return
            if "@gmail.com" not in Gmail.get():
                messagebox.showwarning("Input Error", "Invalid Gmail ID. Please enter the domain '@gmail.com' as well")
                return
            if not PhoneNo.get():
                messagebox.showwarning("Input Error", "Phone number is required")
                return
            if len(PhoneNo.get())!=10 or not PhoneNo.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Phone Number")
                return
            if not TrainerID.get():
                messagebox.showwarning("Input Error", "Trainer ID is required")
                return
            if not TrainerID.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Trainer ID ")
                return

            c.execute("SELECT trainer_id FROM trainer WHERE trainer_id = ?", (TrainerID.get(),))
            trainer = c.fetchone()
            if trainer is None:
                messagebox.showwarning("Invalid Trainer ID", "The entered Trainer ID does not exist!")
                conn.close()
                return
        
            c.execute("SELECT seats FROM trainer WHERE trainer_id=?", (TrainerID.get(),))
            seats = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM reservations WHERE trainer_id=?", (TrainerID.get(),))
            reserve_count = c.fetchone()[0]

            if reserve_count >= seats:
                messagebox.showwarning("Seat Full", "Seat is fully booked!")
                conn.close()
                return


            c.execute("INSERT INTO reservations (full_name, phone_number, gmail, trainer_id) VALUES (?, ?, ?, ?)",
                    (Name.get().title(), PhoneNo.get(), Gmail.get(), TrainerID.get()))

            messagebox.showinfo("Records", "Inserted Successfully")
            conn.commit()
            conn.close()

            Name.delete(0, END)
            Gmail.delete(0, END)
            PhoneNo.delete(0, END)
            TrainerID.delete(0, END)
            query()
        
        def query():
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
        
            c.execute(
            """SELECT r.reservation_id, r.full_name, r.phone_number, r.gmail,
               t.trainer_name, t.phone_number, t.gmail,
               t.vehicle, t.duration, t.time_shift
               FROM reservations r
               LEFT JOIN trainer t
               ON r.trainer_id = t.trainer_id
            """
            )
        
            records = c.fetchall()
            conn.close()

            for widget in table_inner.winfo_children():
                widget.destroy()
                
            headings = [
                "Reservation ID", "Reserver Name", "Reserver Phone No", "Reserver Gmail",
                "Trainer Name", "Trainer Phone No", "Trainer Gmail",
                "Vehicle", "Duration", "Time Shift"
                ]
            for col, heading in enumerate(headings):
                lbl = Label(table_inner, text=heading, bg="#000000", fg="#ffffff",
                    font=("Inter", 10, "bold"), borderwidth=1, relief="solid", padx=3, pady=3)
                lbl.grid(row=0, column=col, sticky="nsew",pady=(20,10))
            
            for row_index, record in enumerate(records, start=1):
                safe = [str(x) if x is not None else "-" for x in record]
                for col_index, value in enumerate(safe):
                    lbl = Label(table_inner, text=value, bg="#000000", fg="#ffffff",
                        font=("Inter", 10), borderwidth=1, relief="solid", padx=3, pady=3)
                    lbl.grid(row=row_index, column=col_index, sticky="nsew")
            
            for col in range(len(headings)):
                table_inner.grid_columnconfigure(col, weight=1)



        def delete():
            if not ReservationID_entry.get():
                messagebox.showerror("Input Error", "Please enter an ID to delete!")
                return

            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()

            c.execute("SELECT reservation_id FROM reservations WHERE reservation_id = ?", (ReservationID_entry.get(),))
            reservation = c.fetchone()
            if reservation is None:
                messagebox.showwarning("Invalid Reservation ID", "The entered Reservation ID does not exist!")
                conn.close()
                return

            c.execute("DELETE FROM reservations WHERE reservation_id = ?", (ReservationID_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Deleted Successfully!")
            ReservationID_entry.delete(0, END)
            query()



        def edit():
            
            # -- check wheather reservation id exists ----
            if not ReservationID_entry.get().strip():
                messagebox.showerror("Input Error", "Please enter a Reservation ID!")
                return
        
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()

            c.execute("SELECT reservation_id FROM reservations WHERE reservation_id = ?", (ReservationID_entry.get(),))
            reservation = c.fetchone()
            if reservation is None:
                messagebox.showwarning("Invalid Reservation ID", "The entered Reservation ID does not exist!")
                conn.close()
                return
            


            # --- new screen to update data---

            global top_editor
            top_editor = Toplevel()
            top_editor.title("Update Data")
            top_editor.geometry("300x400")

            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
        
            record_id = ReservationID_entry.get()
            c.execute("SELECT * FROM reservations WHERE reservation_id = ?", (record_id,))
            records = c.fetchall()
            conn.close()

            global name_editor, gmail_editor, phoneno_editor, trainerid_editor

            name_editor = Entry(top_editor, width=30)
            name_editor.grid(row=0, column=1, padx=20, pady=(10,0))
            gmail_editor = Entry(top_editor, width=30)
            gmail_editor.grid(row=1, column=1)
            phoneno_editor = Entry(top_editor, width=30)
            phoneno_editor.grid(row=2, column=1)
            trainerid_editor = Entry(top_editor, width=30)
            trainerid_editor.grid(row=3, column=1)

            Label(top_editor, text="Full Name").grid(row=0, column=0, pady=(10,0))
            Label(top_editor, text="Gmail").grid(row=1, column=0)
            Label(top_editor, text="Phone Number").grid(row=2, column=0)
            Label(top_editor, text="Trainer ID").grid(row=3, column=0)

            # insert prvious data onto the entry fields

            for record in records:
                name_editor.insert(0, record[1])
                phoneno_editor.insert(0, record[2])
                gmail_editor.insert(0, record[3])
                trainerid_editor.insert(0, record[4])

            Button(top_editor, text="Save", command=update).grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

        def update():

            if not name_editor.get():
                messagebox.showwarning("Input Error", "Name is required",parent=top_editor)
                return
            if not gmail_editor.get():
                messagebox.showwarning("Input Error", "Email is required", parent=top_editor)
                return
            if "@gmail.com" not in gmail_editor.get():
                messagebox.showwarning("Input Error", "Invalid Gmail ID. Please enter the domain '@gmail.com' as well", parent=top_editor)
                return
            if not phoneno_editor.get():
                messagebox.showwarning("Input Error", "Phone number is required", parent=top_editor)
                return
            if len(phoneno_editor.get())!=10 or not phoneno_editor.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Phone Number", parent=top_editor)
                return
            if not trainerid_editor.get():
                messagebox.showwarning("Input Error", "Trainer ID is required", parent=top_editor)
                return
            if not trainerid_editor.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Trainer ID ", parent=top_editor)
                return

        
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
        
            c.execute("SELECT trainer_id FROM trainer WHERE trainer_id = ?", (trainerid_editor.get(),))
            trainer = c.fetchone()
            if trainer is None:
                messagebox.showwarning("Invalid Trainer ID", "The entered Trainer ID does not exist!",parent=top_editor)
                conn.close()
                return
        
            c.execute("SELECT seats FROM trainer WHERE trainer_id=?", (trainerid_editor.get(),))
            seats = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM reservations WHERE trainer_id=?", (trainerid_editor.get(),))
            reserve_count = c.fetchone()[0]

            if reserve_count >= seats:
                messagebox.showwarning("Seat Full", "Seat is fully booked!", parent=top_editor)
                conn.close()
                return
            
            data = (name_editor.get(), gmail_editor.get(), phoneno_editor.get(), trainerid_editor.get(), ReservationID_entry.get())
            c.execute("UPDATE reservations SET full_name=?, gmail=?, phone_number=?, trainer_id=? WHERE reservation_id=?", data)
            messagebox.showinfo("Records", "Updated Successfully")
            conn.commit()
            conn.close()
            query()
            ReservationID_entry.delete(0, END)
            top_editor.destroy()


        def search():
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
        
            c.execute(
            """SELECT r.reservation_id, r.full_name, r.phone_number, r.gmail,
               t.trainer_name, t.phone_number, t.gmail,
               t.vehicle, t.duration, t.time_shift
               FROM reservations r
               LEFT JOIN trainer t
               ON r.trainer_id = t.trainer_id
            """
            )
        
            records = c.fetchall()
            conn.close()

            for widget in table_inner.winfo_children():
                widget.destroy()
                
            headings = [
                "Reservation ID", "Reserver Name", "Reserver Phone No", "Reserver Gmail",
                "Trainer Name", "Trainer Phone No", "Trainer Gmail",
                "Vehicle", "Duration", "Time Shift"
                ]
            

            for col, heading in enumerate(headings):
                lbl = Label(table_inner, text=heading, bg="#000000", fg="#ffffff",
                    font=("Inter", 10, "bold"),
                    borderwidth=1, relief="solid", padx=3, pady=3)
                lbl.grid(row=0, column=col, sticky="nsew")
                
                
            found = False
            row_number = 1

            rname_search = reserver_name_search.get().strip().lower()
            tname_search = trainer_name_search.get().strip().lower()  

            
            for record in records:
                reserver_name = str(record[1]).lower()
                trainer_name = str(record[4]).lower()

                if (rname_search == "" or rname_search in reserver_name) and \
                    (tname_search == "" or tname_search in trainer_name):

                    found = True
                
                    for col_index, value in enumerate(record):
                        lbl = Label(table_inner, text=str(value),
                            bg="#000000", fg="#ffffff",
                            font=("Inter", 10),
                            borderwidth=1, relief="solid",
                            padx=3, pady=3)
                        lbl.grid(row=row_number, column=col_index, sticky="nsew")
                        
                    row_number += 1
            
            if not found:
                lbl = Label(table_inner, text="No Record Found",
                    bg="#000000", fg="red",
                    font=("Inter", 12, "bold"))
                lbl.grid(row=2, column=0, columnspan=len(headings))

            for col in range(len(headings)):
                table_inner.grid_columnconfigure(col, weight=1)
         


        # ---------------- CRUD FRAME ----------------
        
        crud = Frame(root, bg="#0f1b4c", width=440)
        crud.pack(side=LEFT, fill=BOTH, padx=5)

        Label(crud, text="Full Name:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        Name = Entry(crud)
        Name.pack(fill=X, padx=10, pady=5)

        Label(crud, text="Gmail:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        Gmail = Entry(crud, width= 48)
        Gmail.pack(fill=X, padx=10, pady=5)

        Label(crud, text="Phone Number:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        PhoneNo = Entry(crud, width= 48)
        PhoneNo.pack(fill=X, padx=10, pady=5)

        Label(crud, text="Trainer ID:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        TrainerID = Entry(crud, width= 48)
        TrainerID.pack(fill=X, padx=10, pady=5)

        Button(crud, text="Add", bg="#E900E9", command=add).pack(pady=10, fill=X, padx=10)
        Button(crud, text="Show Records", bg="#000000", fg="#ffffff", command=query).pack(pady=10, fill=X, padx=10)



        # ---------------- CONTENT FRAME ----------------
        content = Frame(root, bg="#000000", bd=1, relief="solid", height=50)
        content.pack(fill="x", padx=5)



        # -------------- Update Delete Frame -----------------

        ud = Frame(content, bg="#30818b", bd=1, relief="solid", height=50)
        ud.pack(side=LEFT, fill="y", padx=10, pady=10)

        Label(ud, text="Reservation ID:", fg="#000000", font=("Arial",8,"bold")).grid(row=0, column=0, padx=10, pady=(25,10))
        ReservationID_entry = Entry(ud, width=50, bg="#CED1D3", fg="#000000")
        ReservationID_entry.grid(row=0, column=1, padx=(5,10), pady=(25,10), sticky="w")

        Button(ud, text="Update", bg="#E900E9", fg="#000000", command=edit).grid(row=1, column=0, padx=(10,0), pady=40, sticky="w")
        Button(ud, text="Delete", bg="#E900E9", fg="#000000", command=delete).grid(row=1, column=1, pady=40, sticky="w")




        # ------------------- Search Frame ------------------

        find = Frame(content, bg="#30818b", bd=1, relief="solid", height=50)
        find.pack(side=LEFT,fill="y", padx=(0,10), pady=10)

        Label(find, text="Search By :", bg="#30818b", fg="#000000", font=("Arial",11,"bold")).grid(row=2, column=0, padx=2, pady=(10,0), sticky="w")


        Label(find, text="Reserver Name:", fg="#000000", font=("Arial",8,"bold")).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        reserver_name_search = Entry(find, width=50, bg="#CED1D3", fg="#000000")
        reserver_name_search.grid(row=4, column=1, padx=5, pady=10, sticky="w")

        Label(find, text="Trainer Name:", fg="#000000", font=("Arial",8,"bold")).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        trainer_name_search = Entry(find, width=50, bg="#CED1D3", fg="#000000")
        trainer_name_search.grid(row=5, column=1, padx=5, pady=10, sticky="w")

        Button(find, text="Search", bg="#830404", fg="#FFFFFF", command= search).grid(row=6, column=0, padx=(20,0), pady=20, sticky="w")




            # ---------------- TABLE FRAME (SCROLLABLE) ----------------
 
        table = Frame(root, bg="#ffffff", bd=1, relief="solid")
        table.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        
        table_container = Frame(table)
        table_container.pack(fill=BOTH, expand=True)
        
        table_canvas = Canvas(table_container, bg="#0F0F0F", highlightthickness=0)
        table_canvas.grid(row=0, column=0, sticky="nsew")
        
        v_scroll = Scrollbar(table_container, orient=VERTICAL, command=table_canvas.yview)
        v_scroll.grid(row=0, column=1, sticky="ns") 
        
        h_scroll = Scrollbar(table_container, orient=HORIZONTAL, command=table_canvas.xview)
        h_scroll.grid(row=1, column=0, sticky="ew") 
        
        
        table_canvas.configure(
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set)
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        table_inner = Frame(table_canvas, bg="#000000")
        table_window = table_canvas.create_window((0, 0), window=table_inner, anchor="nw")
        
        def _resize_table(event):
            table_canvas.configure(scrollregion=table_canvas.bbox("all"))
            
        table_inner.bind("<Configure>", _resize_table)


    def onclick_trainer_btn():
        reset_button_color()
        clear_main_area()

        trainer_btn.config(bg="#6a88ff")

        # ---------------- CRUD FUNCTIONS ----------------
        def add():
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")

            if not Name.get():
                messagebox.showwarning("Input Error", "Name is required")
                return
            if not Gmail.get():
                messagebox.showwarning("Input Error", "Email is required")
                return
            if "@gmail.com" not in Gmail.get():
                messagebox.showwarning("Input Error", "Invalid Gmail ID. Please enter the domain '@gmail.com' as well")
                return
            if not PhoneNo.get():
                messagebox.showwarning("Input Error", "Phone number is required")
                return
            if len(PhoneNo.get())!=10 or not PhoneNo.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Phone Number")
                return
            if vc.get() == " ":
                messagebox.showwarning("Input Error", "Select a vehicle from option")
                return
            if dc.get() == " ":
                messagebox.showwarning("Input Error", "Select a course package from option")
                return
            if tc.get() == " ":
                messagebox.showwarning("Input Error", "Select a time shift from option")
                return
            if not seat.get():
                messagebox.showwarning("Input Error", "Number of Seats is required")
                return
            if not seat.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Input. Enter digits!")
                return

            c.execute("INSERT INTO trainer (trainer_name, phone_number, gmail, vehicle, duration, time_shift, seats) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (Name.get().title(), PhoneNo.get(), Gmail.get(), vc.get(), dc.get(), tc.get(), seat.get()))

            messagebox.showinfo("Records", "Inserted Successfully")
            conn.commit()
            conn.close()

            Name.delete(0, END)
            Gmail.delete(0, END)
            PhoneNo.delete(0, END)
            query()

        def query():
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()

            c.execute("SELECT trainer_id, trainer_name, phone_number, gmail, vehicle, duration, time_shift, seats FROM trainer")

            records = c.fetchall()
            conn.close()
        
            headings = [
                "Trainer ID","Trainer Name", "Trainer Phone No", "Trainer Gmail",
                "Vehicle", "Duration", "Time Shift", "No of Seats"
                ]
            for col, heading in enumerate(headings):
                lbl = Label(table_inner, text=heading, bg="#000000", fg="#ffffff",
                    font=("Inter", 10, "bold"), borderwidth=1, relief="solid", padx=3, pady=3)
                lbl.grid(row=0, column=col, sticky="nsew",pady=(20,10))
            
            for row_index, record in enumerate(records, start=1):
                safe = [str(x) if x is not None else "-" for x in record]
                for col_index, value in enumerate(safe):
                    lbl = Label(table_inner, text=value, bg="#000000", fg="#ffffff",
                        font=("Inter", 10), borderwidth=1, relief="solid", padx=3, pady=3)
                    lbl.grid(row=row_index, column=col_index, sticky="nsew")
            
            for col in range(len(headings)):
                table_inner.grid_columnconfigure(col, weight=1)


        def delete():
            if not TrainerID_entry.get():
                messagebox.showerror("Input Error", "Please enter an ID to delete!")
                return

            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()

            c.execute("SELECT trainer_id FROM trainer WHERE trainer_id = ?", (TrainerID_entry.get(),))
            reservation = c.fetchone()
            if reservation is None:
                messagebox.showwarning("Invalid Trainer ID", "The entered Trainer ID does not exist!")
                conn.close()
                return
  
            c.execute("DELETE FROM trainer WHERE trainer_id = ?", (TrainerID_entry.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Deleted Successfully!")
            TrainerID_entry.delete(0, END)
            query()

        def edit():
            if not TrainerID_entry.get().strip():
                messagebox.showerror("Input Error", "Please enter a Trainer ID!")
                return
        
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()

            c.execute("SELECT trainer_id FROM trainer WHERE trainer_id = ?", (TrainerID_entry.get(),))
            reservation = c.fetchone()
            if reservation is None:
                messagebox.showwarning("Invalid Trainer ID", "The entered Trainer ID does not exist!")
                conn.close()
                return

            global top_update
            top_update = Toplevel()
            top_update.title("Update Data")
            top_update.geometry("400x700")

            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
        
            record_id = TrainerID_entry.get()
            c.execute("SELECT * FROM trainer WHERE trainer_id = ?", (record_id,))
            records = c.fetchall()
            conn.close()

            global name_update, gmail_update, phoneno_update, seat_update, ev, de, et

            name_update = Entry(top_update, width=30)
            name_update.grid(row=0, column=1, padx=20, pady=(10,0))
            gmail_update = Entry(top_update, width=30)
            gmail_update.grid(row=1, column=1)
            phoneno_update = Entry(top_update, width=30)
            phoneno_update.grid(row=2, column=1)
            seat_update = Entry(top_update, width=30)
            seat_update.grid(row=21, column=1)

            
            ev= StringVar()
            ev.set(records[0][4])
        
            Radiobutton(top_update,text="car",variable=ev, value="car").grid(row=5, column=0)
            Radiobutton(top_update,text="scooter",variable=ev, value="scooter").grid(row=6, column=0)
            Radiobutton(top_update,text="motorbike",variable=ev, value="motorbike").grid(row=7, column=0)
        

            de= StringVar()
            de.set(records[0][5])
        
            Radiobutton(top_update,text="7 Days",variable=de, value="7 Days").grid(row=10, column=0)
            Radiobutton(top_update,text="15 Days",variable=de, value="15 Days").grid(row=11, column=0)
            Radiobutton(top_update,text="30 Days",variable=de, value="30 Days").grid(row=12, column=0)
            Radiobutton(top_update,text="3 Months",variable=de, value="3 Months").grid(row=13, column=0)



            et= StringVar()
            et.set(records[0][6])
            Radiobutton(top_update,text="8am-10am",variable=et, value="8am-10am").grid(row=16, column=0)
            Radiobutton(top_update,text="10am-12pm",variable=et, value="10am-12pm").grid(row=17, column=0)
            Radiobutton(top_update,text="12pm-2pm",variable=et, value="12pm-2pm").grid(row=18, column=0)
            Radiobutton(top_update,text="2pm-4pm",variable=et, value="2pm-4pm").grid(row=19, column=0)



            Label(top_update, text="Full Name").grid(row=0, column=0, pady=(10,0))
            Label(top_update, text="Gmail").grid(row=1, column=0)
            Label(top_update, text="Phone Number").grid(row=2, column=0)
            Label(top_update, text="Vehicle : ").grid(row=4, column=0)
            Label(top_update, text="Course Package :").grid(row=9, column=0)
            Label(top_update, text="Time Shift :").grid(row=15, column=0)
            Label(top_update, text="No of Seats :").grid(row=21, column=0)


            name_update.insert(0, records[0][1])
            phoneno_update.insert(0, records[0][2])
            gmail_update.insert(0, records[0][3])
            seat_update.insert(0, records[0][7])

            Button(top_update, text="Save", command=update).grid(row=23, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

        def update():
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()

            if not name_update.get():
                messagebox.showwarning("Input Error", "Name is required", parent=top_update)
                return
            if not gmail_update.get():
                messagebox.showwarning("Input Error", "Email is required", parent=top_update)
                return
            if "@gmail.com" not in gmail_update.get():
                messagebox.showwarning("Input Error", "Invalid Gmail ID. Please enter the domain '@gmail.com' as well", parent=top_update)
                return
            if not phoneno_update.get():
                messagebox.showwarning("Input Error", "Phone number is required", parent=top_update)
                return
            if len(phoneno_update.get())!=10 or not phoneno_update.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Phone Number", parent=top_update)
                return
            if not seat_update.get():
               messagebox.showwarning("Input Error", "Number of Seats is required", parent=top_update)
               return
            if not seat_update.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Input. Enter digits!", parent=top_update)
                return
            if not TrainerID_entry.get():
                messagebox.showwarning("Input Error", "Trainer ID is required", parent=top_update)
                return
            if not TrainerID_entry.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Trainer ID ", parent=top_update)
                return
            
            data = (name_update.get(), phoneno_update.get(), gmail_update.get(), ev.get(), de.get(), et.get(), seat_update.get(), TrainerID_entry.get())
            c.execute("UPDATE trainer SET trainer_name=?, phone_number=?, gmail=?, vehicle=?, duration=?, time_shift=?, seats=? WHERE trainer_id=?", data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Updated Successfully!")
            query()
            top_update.destroy()

         # ---------------- CRUD FRAME ----------------
        crud = Frame(root, bg="#0f1b4c", width=440)
        crud.pack(side=LEFT, fill=BOTH, padx=5)
        Label(crud,text=".",font=("Inter",1),bg="#0f1b4c").pack(padx=150)

    
        crud_canvas = Canvas(crud, bg="#0f1b4c", highlightthickness=0)
        crud_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        crud_scrollbar = Scrollbar(crud, orient=VERTICAL, command=crud_canvas.yview)
        crud_scrollbar.pack(side=RIGHT, fill=Y)

        crud_canvas.configure(yscrollcommand=crud_scrollbar.set)

        scrollable_frame = Frame(crud_canvas, bg="#0f1b4c")
        crud_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: crud_canvas.configure(scrollregion=crud_canvas.bbox("all"))
        )


        Label(scrollable_frame, text=".", font=("Inter",1), bg="#0f1b4c").pack(pady=5)

        # Name field
        Label(scrollable_frame, text="Full Name:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(0,0))
        Name = Entry(scrollable_frame, width= 30)
        Name.pack(fill=X, padx=10, pady=5)

        # Gmail field
        Label(scrollable_frame, text="Gmail:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        Gmail = Entry(scrollable_frame, width= 30)
        Gmail.pack(fill=X, padx=10, pady=5)

        # Phone Number field
        Label(scrollable_frame, text="Phone Number:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        PhoneNo = Entry(scrollable_frame, width=30)
        PhoneNo.pack(fill=X, padx=10, pady=5)

        Label(scrollable_frame, text="Choose:", font=("Inconsolata", 9, "bold"), fg="#ffffff", bg="#0f1b4c").pack(pady=15, anchor=W, padx=10)

        # ------------- CRUD RADIO BUTTONS ---------------

        # Vehicle Choice
 
        Label(scrollable_frame, text="Vehicle:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))

        vc= StringVar()
        vc.set(" ")

        v1= Radiobutton(scrollable_frame,text="car",variable=vc, value="car")
        v1.pack(anchor=W, padx=10, pady=(10,0))
    
        v2= Radiobutton(scrollable_frame,text="scooter",variable=vc, value="scooter")
        v2.pack(anchor=W, padx=10, pady=(10,0))
    
        v3= Radiobutton(scrollable_frame,text="motorbike",variable=vc, value="motorbike")
        v3.pack(anchor=W, padx=10, pady=(10,0))
    


        # Course Package Choice

        Label(scrollable_frame, text="Course Package:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(20,0))
    
        dc= StringVar()
        dc.set(" ")

        d1= Radiobutton(scrollable_frame,text="7 Days",variable=dc, value="7 Days")
        d1.pack(anchor=W, padx=10, pady=(10,0))
    
        d2= Radiobutton(scrollable_frame,text="15 Days",variable=dc, value="15 Days")
        d2.pack(anchor=W, padx=10, pady=(10,0))
    
        d3= Radiobutton(scrollable_frame,text="30 Days",variable=dc, value="30 Days")
        d3.pack(anchor=W, padx=10, pady=(10,0))

        d4= Radiobutton(scrollable_frame,text="3 Months",variable=dc, value="3 Months")
        d4.pack(anchor=W, padx=10, pady=(10,0))
    


        # Course Package Choice

        Label(scrollable_frame, text="Time Shift:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(20,0))
    
        tc= StringVar()
        tc.set(" ")

        t1= Radiobutton(scrollable_frame,text="8am-10am",variable=tc, value="8am-10am")
        t1.pack(anchor=W, padx=10, pady=(10,0))
    
        t2= Radiobutton(scrollable_frame,text="10am-12pm",variable=tc, value="10am-12pm")
        t2.pack(anchor=W, padx=10, pady=(10,0))
    
        t3= Radiobutton(scrollable_frame,text="12pm-2pm",variable=tc, value="12pm-2pm")
        t3.pack(anchor=W, padx=10, pady=(10,0))

        t4= Radiobutton(scrollable_frame,text="2pm-4pm",variable=tc, value="2pm-4pm")
        t4.pack(anchor=W, padx=10, pady=(10,0))
    

        # Seat field
        Label(scrollable_frame, text="Number of Seats:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        seat = Entry(scrollable_frame, width=30)
        seat.pack(fill=X, padx=10, pady=5)

        # Add Button
        Button(scrollable_frame, text="Add", bg="#E900E9", command=add).pack(pady=(20,10), fill=X, padx=10)

        # Show Records Button
        Button(scrollable_frame, text="Show Records", bg="#000000", fg="#ffffff", command=query).pack(pady=(10,30), fill=X, padx=10)
    

        # ---------------- CONTENT FRAME ----------------
        content = Frame(root, bg="#ffffff", bd=1, relief="solid", height=50)
        content.pack(fill="x", padx=5)

        Label(content, text="Trainer ID:", bg="#000000", fg="#ffffff").pack(side= LEFT, padx=10, pady=10)
        TrainerID_entry = Entry(content, width=50, bg="#2c3e50", fg="#ffffff")
        TrainerID_entry.pack(side= LEFT, padx=10, pady=10)

        Button(content, text="Update", bg="#E900E9", fg="#000000", command=edit).pack(side= LEFT, padx=10, pady=10)
        Button(content, text="Delete", bg="#E900E9", fg="#000000", command=delete).pack(side= LEFT, padx=10, pady=10)
    

        # ---------------- TABLE FRAME ----------------
        table = Frame(root, bg="#ffffff", bd=1, relief="solid")
        table.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        
        table_container = Frame(table)
        table_container.pack(fill=BOTH, expand=True)
        
        table_canvas = Canvas(table_container, bg="#000000", highlightthickness=0)
        table_canvas.grid(row=0, column=0, sticky="nsew")
        
        v_scroll = Scrollbar(table_container, orient=VERTICAL, command=table_canvas.yview)
        v_scroll.grid(row=0, column=1, sticky="ns") 
        
        h_scroll = Scrollbar(table_container, orient=HORIZONTAL, command=table_canvas.xview)
        h_scroll.grid(row=1, column=0, sticky="ew") 
        
        
        table_canvas.configure(
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set)
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        table_inner = Frame(table_canvas, bg="#000000")
        table_window = table_canvas.create_window((0, 0), window=table_inner, anchor="nw")
        
        def _resize_table(event):
            table_canvas.configure(scrollregion=table_canvas.bbox("all"))
            
        table_inner.bind("<Configure>", _resize_table)
    

    # ===================== SIDEBAR BUTTONS =====================
    icons["home"] = ImageTk.PhotoImage(Image.open("home.ico").resize((30, 30)))
    home_btn = Button(sidebar, image=icons["home"], command=onclick_home_btn)
    home_btn.place(x=50, y=100)
    Label(sidebar,text="Home",fg="#000000").place(x=50, y=150)



    icons["record"] = ImageTk.PhotoImage(Image.open("report.ico").resize((30, 30)))
    record_btn = Button(sidebar, image=icons["record"], command=onclick_record_btn)
    record_btn.place(x=50, y=200)
    Label(sidebar,text="Reservation Records",fg="#000000").place(x=20, y=250)



    icons["trainer"] = ImageTk.PhotoImage(Image.open("table.ico").resize((30, 30)))
    trainer_btn = Button(sidebar, image=icons["trainer"], command=onclick_trainer_btn)
    trainer_btn.place(x=50, y=320)
    Label(sidebar,text="Trainer Details",fg="#000000").place(x=30, y=370)

    Button(sidebar,text="Logout",bg="#880F0F",fg="#FFFFFF",font=("Inter", 9, "bold"), command=logout).place(x= 50, y=600)

    onclick_home_btn()



def DCR_user():
    clear_window()
# ----------- SIDE FRAME --------------

    sidebar = Frame(root,bg="#ffffff",bd=1,relief="solid",width=140)
    sidebar.pack(side=LEFT,fill="y")
    
    def user_reset_button_color():
        user_home_btn.config(bg="#ffffff")
        reservation_btn.config(bg="#ffffff")
        
    def user_clear_main_area():
        for widget in root.winfo_children():
            if widget != sidebar:
                widget.destroy()

                
    def onclick_user_home_btn():
        user_reset_button_color()
        user_home_btn.config(bg="#6a88ff")
        user_clear_main_area()
        
        # ---------------- HEADER ----------------
        header = Frame(root, bg="#0f1b4c")
        header.pack(fill="x")
        
        Label(header, text="Hi Admin, Welcome !",
              font=("Josefin Sans", 22, "bold"),
              fg="#ffffff", bg="#0f1b4c").pack(pady=20)
        
        # ---------------- FILTER ----------------
        filter = Frame(root, bg="#9aa728")
        filter.pack(fill="x", pady=5)
        
        Label(filter, text="Filter :",
              font=("Inter", 16, "bold"),
              bg="#9aa728", fg="#1D1D1D").pack(side=LEFT, padx=20, pady=40)
        
        global clicked_vehicle, clicked_course_package, clicked_time_shift
        
        clicked_vehicle = StringVar(value="---Vehicle---")
        OptionMenu(filter, clicked_vehicle, "car", "van", "scooter", "motorbike").pack(side=LEFT, padx=5)
        
        clicked_course_package = StringVar(value="---Course Package---")
        OptionMenu(filter, clicked_course_package, "7 Days", "15 Days", "30 Days", "3 Months").pack(side=LEFT, padx=5)
        
        clicked_time_shift = StringVar(value="---Time Shift---")
        OptionMenu(filter, clicked_time_shift, "8am-10am", "10am-12pm", "12pm-2pm", "2pm-4pm").pack(side=LEFT, padx=5)
        
        # ---------------- CONTENT AREA ----------------
        content = Frame(root, bg="#ffffff", bd=1, relief="solid")
        content.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        
        content_canvas = Canvas(content, bg="#ffffff", highlightthickness=0)
        content_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(content, orient=VERTICAL, command=content_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        content_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollable_frame = Frame(content_canvas, bg="#ffffff")
        canvas_window = content_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        content_canvas.bind("<Configure>", lambda e:
            content_canvas.itemconfig(canvas_window, width=e.width))
        
        scrollable_frame.bind("<Configure>", lambda e:
            content_canvas.configure(scrollregion=content_canvas.bbox("all")))
        
        # ---------------- QUERY ----------------
        def query():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
                
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
            c.execute("SELECT * FROM trainer")
            records = c.fetchall()
            
            found = False
            for record in records:
                trainer_id = record[0]
                seats = int(record[7])
                
                c.execute("SELECT COUNT(*) FROM reservations WHERE trainer_id=?", (trainer_id,))
                reserve_count = c.fetchone()[0]
                category = "Booked" if reserve_count >= seats else "Unbooked"

                    
                if not (
                    clicked_vehicle.get() in ("---Vehicle---", record[4]) and
                    clicked_course_package.get() in ("---Course Package---", record[5]) and
                    clicked_time_shift.get() in ("---Time Shift---", record[6])
                ):
                    continue



                if category == "Unbooked":
                    found = True

                    card = Frame(scrollable_frame, bg="#0f1b4c")
                    card.pack(fill="x", padx=15, pady=10)
                    
                    card.columnconfigure(0, weight=1)
                    card.columnconfigure(1, weight=0)

                    details = Frame(card, bg="#0f1b4c")
                    details.grid(row=0, column=0, sticky="w", padx=20, pady=15)

                    Label(details, text=f"Trainer : {record[1]}",
                      font=("Inter", 12, "bold"),
                      fg="#ffffff", bg="#0f1b4c").pack(anchor="w")

                    Label(details,
                      text=(f"Vehicle     : {record[4]}\n"
                        f"Package     : {record[5]}\n"
                        f"Time Shift  : {record[6]}\n"
                        f"Status      : {category}\n\n"
                        f"Phone Number: {record[2]}\n"
                        f"Gmail       : {record[3]}\n\n"),
                      font=("Inter", 10),
                      fg="#e0e0e0",
                      bg="#0f1b4c",
                      justify=LEFT).pack(anchor="w", pady=6)
                    

                     
                    Label(details, text=f"Seats Left  : {seats - reserve_count}\n",
                      font=("Inter", 12, "bold"),
                      fg="#ffffff", bg="#0f1b4c").pack(anchor="w")

                    action = Frame(card, bg="#0f1b4c")
                    action.grid(row=0, column=1, sticky="e", padx=25)

                    Button(action, text="Book Course",
                       bg="#DA07C4", fg="#FFFFFF",
                       font=("Inter", 10, "bold"),
                       bd=0, padx=18, pady=6,
                       command=lambda tid=trainer_id: open_booking(tid)).pack()
                else:
                    continue

            conn.close()

            if not found:
                Label(scrollable_frame, text="No matching records found.",
                  fg="red", bg="#FFFFFF",
                  font=("Inter", 16, "bold")).pack(pady=100)
        query()

        Button(filter, text="Search",
           bg="#000000", fg="#ffffff",
           font=("Inter", 10, "bold"),
           command=query).pack(side=LEFT, padx=5)
    
        def open_booking(trainer_id):

            global reserver_name, reserver_phoneno, reserver_gmail

            top = Toplevel()
            top.title("Book Seat")
            top.geometry("350x420")
            
            Label(top, text="Your Full Name :").pack(pady=(10, 0))
            reserver_name= ttk.Entry(top, width=30)
            reserver_name.pack()
        
            Label(top, text="Phone Number :").pack(pady=(10, 0))
            reserver_phoneno = ttk.Entry(top, width=30)
            reserver_phoneno.pack()
        
            Label(top, text="Gmail :").pack(pady=(10, 0))
            reserver_gmail = ttk.Entry(top, width=30)
            reserver_gmail.pack()

        
            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
            c.execute("SELECT * FROM trainer WHERE trainer_id=?", (trainer_id,))
            t = c.fetchone()
            conn.close()
        
            Label(top, text=f"\nTrainer: {t[1]}").pack()
            Label(top, text=f"Vehicle: {t[4]}").pack()
            Label(top, text=f"Package: {t[5]}").pack()
            Label(top, text=f"Time Shift: {t[6]}").pack()

        
            def save():
                conn = sq.connect("DrivingCourseRegistration.db")
                c = conn.cursor()
 
                if not reserver_name.get():
                    messagebox.showwarning("Input Error", "Name is required",parent=top)
                    return
    
                if not reserver_gmail.get():
                    messagebox.showwarning("Input Error", "Email is required",parent=top)
                    return
            
                if "@gmail.com" not in reserver_gmail.get():
                    messagebox.showwarning("Input Error", "Invalid Gmail ID. Please enter the domain '@gmail.com' as well",parent=top)
                    return
            
                if not reserver_phoneno.get():
                    messagebox.showwarning("Input Error", "Phone number is required",parent=top)
                    return
            
                if len(reserver_phoneno.get())!=10 or not reserver_phoneno.get().isdigit():
                    messagebox.showwarning("Input Error", "Invalid Phone Number",parent=top)
                    return
            
                c.execute("""
                    INSERT INTO reservations (full_name, phone_number, gmail, trainer_id, user_id)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        reserver_name.get().title(),
                        reserver_phoneno.get(),
                        reserver_gmail.get(),
                        trainer_id,
                        current_user_id
                    ))
            
                conn.commit()
                conn.close()
            
                messagebox.showinfo("Success", "Course booked successfully!")
                top.destroy()
                query()

            Button(
                top,
                text="Save Booking",
                bg="#000000",
                fg="#ffffff",
                padx=30,
                pady=6,
                command=save
            ).pack(pady=20)

    def onclick_reservation_btn():
        user_reset_button_color()
        user_clear_main_area()
        reservation_btn.config(bg="#6a88ff")

        content = Frame(root, bg="#ffffff", bd=1, relief="solid")
        content.pack(side=RIGHT, fill=BOTH, expand=True)

        content_canvas = Canvas(content, bg="#ffffff", highlightthickness=0)
        content_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(content, orient=VERTICAL, command=content_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        content_canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = Frame(content_canvas, bg="#ffffff")
        canvas_window = content_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        content_canvas.bind(
            "<Configure>",
            lambda e: content_canvas.itemconfig(canvas_window, width=e.width)
        )

        scrollable_frame.bind(
            "<Configure>",
            lambda e: content_canvas.configure(scrollregion=content_canvas.bbox("all"))
        )

        def query():
   
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()

            c.execute(
                "SELECT * FROM reservations WHERE user_id=?",
                (current_user_id,)
            )
            reservations = c.fetchall()

            found = False

            for r in reservations:
                found = True
  
                trainer_id = r[4]
                c.execute("SELECT * FROM trainer WHERE trainer_id=?", (trainer_id,))
                trainer = c.fetchone()
                trainer_name = trainer[1] if trainer else "N/A"

                card = Frame(scrollable_frame, bg="#0f1b4c")
                card.pack(fill="x", padx=15, pady=10)

                card.columnconfigure(0, weight=1)

                details = Frame(card, bg="#0f1b4c")
                details.grid(row=0, column=0, sticky="w", padx=20, pady=15)

                Label(
                    details,
                    text=f"Reserver : {r[1]}",
                    font=("Inter", 12, "bold"),
                    fg="#ffffff",
                    bg="#0f1b4c"
                ).pack(anchor="w")

                Label(
                    details,
                    text=f"Trainer : {trainer_name}",
                    font=("Inter", 12, "bold"),
                    fg="#ffffff",
                    bg="#0f1b4c"
                ).pack(anchor="w")

                Label(
                    details,
                    text=(
                        f"Vehicle     : {trainer[4]}\n"
                        f"Package     : {trainer[5]}\n"
                        f"Time Shift  : {trainer[6]}\n"
                        f"Phone Number: {trainer[2]}\n\n"
                        f"Gmail       : {trainer[3]}"
                    ),
                    font=("Inter", 10),
                    fg="#e0e0e0",
                    bg="#0f1b4c",
                    justify=LEFT
                ).pack(anchor="w", pady=6)

                action = Frame(card, bg="#0f1b4c")
                action.grid(row=0, column=1, sticky="e", padx=25)



                def onclick_cancel(reservation_id=r[0]):
                    confirm = messagebox.askyesno("Confirm", "Cancel this reservation?")
                    if not confirm:
                        return
                    
                    conn2 = sq.connect("DrivingCourseRegistration.db")
                    c2 = conn2.cursor()
                    c2.execute("DELETE FROM reservations WHERE reservation_id = ?",(reservation_id,))
                    conn2.commit()
                    conn2.close()


                    messagebox.showinfo("Success", "Booking Cancelled successfully!")

                    query()

                    
                Button(
                    action,
                    text="Cancel",
                    bg="#DA0707",
                    fg="#000000",
                    font=("Inter", 10, "bold"),
                    padx=12,
                    pady=6,
                    command= onclick_cancel).pack(side=RIGHT, anchor="ne")
            conn.close()

            if not found:
                 Label(
                    scrollable_frame,
                    text="No Bookings Done Yet.",
                    fg="red",
                    bg="#ffffff",
                    font=("Inter", 16, "bold")
                ).pack(pady=100)

        query()




    # ===================== SIDEBAR BUTTONS =====================
    icons["user_home"] = ImageTk.PhotoImage(Image.open("home.ico").resize((30, 30)))
    user_home_btn = Button(sidebar, image=icons["user_home"], command=onclick_user_home_btn)
    user_home_btn.place(x=50, y=100)
    Label(sidebar,text="Home",fg="#000000").place(x=50, y=150)

    icons["user_record"] = ImageTk.PhotoImage(Image.open("report.ico").resize((30, 30)))
    reservation_btn = Button(sidebar, image=icons["user_record"], command=onclick_reservation_btn)
    reservation_btn.place(x=50, y=200)
    Label(sidebar,text="Your Reservations",fg="#000000").place(x=30, y=250)

    Button(sidebar,text="Logout",bg="#880F0F",fg="#FFFFFF",font=("Inter", 9, "bold"), command=logout).place(x= 50, y=500)
    Button(sidebar,text="Change Password",bg="#880F0F",fg="#FFFFFF",font=("Inter", 9, "bold"), command= onclick_changeps).place(x=15, y=550)


    onclick_user_home_btn()


if __name__ == "__main__":
    login_page()
    root.mainloop()