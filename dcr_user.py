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
                DCR_user()
                
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


icons = {}

def DCR_user():
    clear_window()
    
    # ------------ Side Frame -----------

    sidebar = Frame(root, bg="#ffffff", bd=1, relief="solid", width= 140)
    sidebar.pack(side= LEFT, fill="y")

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


        # ----- header frame-----
        header = Frame(root, bg="#0f1b4c")
        header.pack(fill="x")

        Label(header, text="Hi Admin, Welcome!",font=("Josefin Sans", 22, "bold"), fg="#ffffff", bg="#0f1b4c").pack(pady=20)

        # filter
        filter = Frame(root, bg="#9aa728")
        filter.pack(fill="x", pady=5)

        Label(filter, text="Filter: ", font=("Inter", 16, "bold"), bg="#9aa728", fg="#1D1D1D").pack(side=LEFT, padx=20, pady=40)

        global clicked_vehicle, clicked_course_package, clicked_time_shift


        clicked_vehicle =  StringVar(value="---Vehicle---")
        OptionMenu(filter, clicked_vehicle, "car", "van", "scooter", "motorbike").pack(side=LEFT, padx=5)

        clicked_course_package =  StringVar(value="---Course Package---")
        OptionMenu(filter, clicked_course_package,"7 Days", "15 Days", "30 Days", "3 Months").pack(side=LEFT, padx=5)

        clicked_time_shift = StringVar(value="---Time Shift---")
        OptionMenu(filter, clicked_time_shift, "8am-10am","10am-12pm","2pm-4pm").pack(side=LEFT, padx=5)

        #-------- Content Area--------

        content = Frame(root, bg="#ffffff", bd=1, relief="solid")
        content.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        content_canvas = Canvas(content, bg="#ffffff", highlightthickness=0)
        content_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(content, orient= VERTICAL, command=content_canvas.yview)
        scrollbar.pack(side= RIGHT, fill=Y)

        content_canvas.configure(yscrollcommand= scrollbar.set)

        scrollable_frame = Frame(content_canvas, bg="#ffffff")
        canvas_window = content_canvas.create_window((0,0), window=scrollable_frame, anchor="nw")

        content_canvas.bind("<Configure>", lambda e:
            content_canvas.itemconfig(canvas_window, width=e.width))
        
        scrollable_frame.bind("<Configure>", lambda e:
            content_canvas.configure(scrollregion=content_canvas.bbox("all")))
        

        #--- Query----

        def query():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()
            c.execute("SELECT * FROM trainer")
            records = c.fetchall()

            found= False
            for record in records:
                trainer_id = record[0]
                seats = int(record[7])
                
                c.execute("SELECT COUNT(*) FROM reservations WHERE trainer_id=?",(trainer_id,))
                reserver_count = c.fetchone()[0]
                category = "Booked" if reserver_count>=seats else "Unbooked"



                if not(
                    clicked_vehicle.get() in ("---Vehicle---", record[4]) and
                    clicked_course_package.get() in ("---Course Package---", record[5]) and
                    clicked_time_shift.get() in ("---Time Shift---", record[6])
                ):
                    continue

                

                if category == "Unbooked":
                    found= True

                    card= Frame(scrollable_frame, bg="#0f1b4c")
                    card.pack(fill="x", padx=15, pady=10)

                    card.columnconfigure(0, weight=1)
                    card.columnconfigure(1, weight=0)

                    details= Frame(card, bg="#0f1b4c")
                    details.grid(row=0, column=0, sticky="w", padx=20, pady=15)

                    Label(details, text=f"Trainer: {record[1]}", 
                          font=("Inter", 12, "bold"), fg="#ffffff", 
                          bg="#0f1b4c").pack(anchor="w")
                    
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
                    
                    Label(details, text= f"Seats Left  : {seats - reserver_count}\n",
                          font=("Inter", 12, "bold"),
                          fg="#ffffff", bg="#0f1b4c").pack(anchor="w")
                    
                    action = Frame(card, bg="#0f1b4c")
                    action.grid(row=0, column=1, sticky="e", padx=25)

                    Button(action, text="Book Course",bg="#DA07C4",fg="#ffffff",
                           font= ("Inter", 10, "bold"),
                           bd=0, padx=18, pady=6,
                           command=lambda tid= trainer_id: open_booking(tid))
                else:
                    continue

            conn.close()

            if not found:
                Label(scrollable_frame, text="No matching records found.",
                      fg="red", bg="#ffffff",
                      font=("Inter", 16, "bold")).pack(pady=100)
                
        query()

        Button(filter, text="Search",
               bg="#000000",fg="#ffffff",
               font=("Inter", 10, "bold"),
               command=query).pack(side=LEFT, padx=5)
        
        def open_booking(trainer_id):
            global reserver_name, reserver_phoneno, reserver_gmail

            top= Toplevel()
            top.title("Book Seat")
            top.geometry("350x420")

            Label(top, text="Your Full Name: ").pack(pady=(10,0))
            reserver_name = ttk.Entry(top, width=30)
            reserver_name.pack()

            Label(top, text="Phone Number: ").pack(pady=(10,0))
            reserver_phoneno = ttk.Entry(top, widget=30)
            reserver_phoneno.pack()

            Label(top, text="Gmail: ").pack(pady=(10,0))
            reserver_gmail = ttk.Entry(top, widget=30)
            reserver_gmail.pack()

            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()
            c.execute("SELECT * FROM trainer WHERE trainer_id=?",(trainer_id,))
            t= c.fetchone()
            conn.close()

            Label(top, text= f"\nTrainer: {t[1]}").pack()
            Label(top, text= f"Vehicle: {t[4]}").pack()
            Label(top, text= f"Package: {t[5]}").pack()
            Label(top, text= f"Time Shift: {t[6]}").pack()

            def save():
                conn = sq.connect("DrivingCourseRegistration.db")
                c= conn.cursor()

                if not reserver_name.get():
                    messagebox.showwarning("Input Error","Name is required.", parent=top)
                    return
                
                if not reserver_gmail.get():
                    messagebox.showwarning("Input Error","Email is required.", parent=top)
                    return
                
                if not "@gmail.com" in reserver_gmail.get():
                    messagebox.showwarning("Input Error","Invalid Gmail ID.", parent=top)
                    return
                
                if not reserver_phoneno.get():
                    messagebox.showwarning("Input Error", "Phone Number is required.", parent=top)
                    return
                
                if len(reserver_phoneno.get())!= 10 or not reserver_phoneno.get().isdigit():
                    messagebox.showwarning("Input Error","Invalid Phone.",parent=top)
                    return
                
                c.execute("""
                          INSERT INTO reservations (full_name, phone_number, gmail, trainer_id, user_id) VALUES (?,?,?,?,?)
                          """, (
                              reserver_name.get().title(),
                              reserver_phoneno.get(),
                              reserver_gmail.get(),
                              trainer_id,
                              current_user_id
                          ))
                
                conn.commit()
                conn.close()

                messagebox.showinfo("Success","Course booked successfully!")
                top.destroy()
            
            Button (
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
        content_canvas.pack(side= LEFT, fill= BOTH, expand= True)

        scrollbar = Scrollbar(content, orient=VERTICAL, command= content_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        content_canvas.configure(yscrollcommand= scrollbar.set)

        scrollable_frame = Frame(content_canvas, bg="#ffffff")
        canvas_window = content_canvas.create_window((0,0), window=scrollable_frame, anchor="nw")

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
            c= conn.cursor()

            c.execute(
                "SELECT * FROM reservations WHERE user_id=?",(current_user_id,)
            )
            reservations = c.fetchall()

            found = False

            for r in reservations:
                found= True

                trainer_id = r[4]

                c.execute("SELECT * FROM trainer WHERE trainer_id=?",(trainer_id,))
                trainer = c.fetchone()
                trainer_name = trainer[1] if trainer else "N/A"

                card = Frame(scrollable_frame, bg="#0f1b4c")
                card.pack(fill="x", padx=15, pady=10)

                card.columnconfigure(0, weight=1)
                details = Frame(card, bg="#0f1b4c")
                details.grid(row=0, column=0, sticky="w", padx=20, pady=15)

                Label(
                    details,
                    text= f"Reserver : {r[1]}",
                    font = ("Inter", 12, "bold"),
                    fg= "#ffffff",
                    bg="#0f1b4c"
                ).pack(anchor="w")

                Label(
                    details,
                    text= f"Trainer : {trainer_name}",
                    font=("Inter", 12, "bold"),
                    fg="#ffffff", bg="#0f1b4c"
                ).pack(anchor="w")

                Label(
                    details,
                    text=(
                        f"Vehicle     : {trainer[4]}\n"
                        f"Package     : {trainer[5]}\n"
                        f"Time Shift  : {trainer[6]}\n"
                        f"Phone Number: {trainer[2]}\n\n"
                        f"Gmail       : {trainer[3]}"
                    ), font= ("Inter", 10), fg="#e0e0e0",
                    bg="#0f1b4c", justify= LEFT
                ).pack(anchor="w", pady=6)

                action = Frame(card, bg="#0f1b4c")
                action.grid(row=0, column=1, sticky="e", padx=25)

                def onclick_cancel(reservation_id= r[0]):
                    confirm = messagebox.askyesno("Confirm","Do you want to cancel this reservation?")
                    if not confirm:
                        return
                    
                    conn2 = sq.connect("DrivingCourseRegistration.db")
                    c2 = conn2.cursor()
                    c2.execute("DELETE FROM reservations WHERE reservation_id=?", (reservation_id,))
                    conn2.commit()
                    conn2.close()

                    messagebox.showinfo("Success","Booking Cancelled Successfully!")
                    query()

                Button(action, text="Cancel", bg="#DA0707", fg="#000000",
                       font=("Inter",10,"bold"), padx=12, pady=6, 
                       command=onclick_cancel).pack(side= RIGHT, anchor="ne")
            conn.close()

            if not found:
                Label(
                    scrollable_frame,
                    text= "No Bookings Done Yet.",
                    fg="red", bg="#ffffff", font=("Inter", 16, "bold")
                ).pack(pady=100)
        query()



    # Sidebar buttons
    icons["user_home"]= ImageTk.PhotoImage(Image.open("home.ico").resize((30,30)))
    user_home_btn = Button(sidebar, image= icons["user_home"], command=onclick_user_home_btn)
    user_home_btn.place(x=50, y=100)
    Label(sidebar, text="Home", fg="#000000").place(x=50, y= 150)

    icons["user_record"]= ImageTk.PhotoImage(Image.open("report.ico").resize((30,30)))
    reservation_btn = Button(sidebar, image= icons["user_record"], command=onclick_reservation_btn)
    reservation_btn.place(x=50, y=200)
    Label(sidebar, text="Your Reservations", fg="#000000").place(x=30, y=250)





if __name__ == "__main__":
    login_page()
    root.mainloop()

      
            
            














              






                    






                    







                
        



        
             