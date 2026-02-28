from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3 as sq

root = Tk()
root.title("Driving Course Registration System")
root.geometry("900x600")

conn = sq.connect("DrivingCourseRegistration.db")
c= conn.cursor()
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
          )""")

c.execute("""
CREATE TABLE IF NOT EXISTS reservations(
          reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
          full_name TEXT,
          phone_number TEXT,
          gmail TEXT,
          trainer_id INTEGER,
          user_id INTEGER,
          
          FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id),
          FOREIGN KEY (user_id) REFERENCES users(id)
          )""")
conn.commit()
conn.close()

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

icons = {}

def DCR_admin():
    clear_window()

    # ----------- SIDE FRAME --------------
    sidebar = Frame(root, bg="#ffffff", bd=1, relief="solid", width=140)
    sidebar.pack(side=LEFT, fill="y")

    def reset_button_color():
        home_btn.config(bg="#ffffff")
        record_btn.config(bg= "#ffffff")
        trainer_btn.config(bg="#ffffff")

    def clear_main_area():
        for widget in root.winfo_children():
            if widget != sidebar :
                widget.destroy()

    def onclick_record_btn():
        reset_button_color()
        clear_main_area()

        record_btn.config(bg="#6a88ff")

        # ----------- CRUD -----------------

        def add():
            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")

            if not Name.get():
                messagebox.showwarning("Input Error", "Name is required")
                return
            
            if not Gmail.get():
                messagebox.showwarning("Input Error","Email is required")
                return
            
            if "@gmail.com" not in Gmail.get():
                messagebox.showwarning("Input Error","Invalid Gmail ID. Please enter the domain '@gmail.com' as well.")
                return
            
            if not PhoneNo.get():
                messagebox.showwarning("Input Error","Phone Number is required")
                return
            
            if len(PhoneNo.get())!=10 or not PhoneNo.get().isdigit():
                messagebox.showwarning("Input Error","Trainer ID is required")
                return
            
            if not TrainerID.get():
                messagebox.showwarning("Input Error","Trainer ID is required")
                return
            
            if not TrainerID.get().isdigit():
                messagebox.showwarning("Input Error","Invalid Trainer ID")
                return
            
            c.execute("SELECT trainer_id FROM trainer WHERE trainer_id=?",(TrainerID.get(),))
            trainer = c.fetchone()
            if trainer is None:
                messagebox.showwarning("Invalid Trainer ID", "the entered Trainer ID does not exist !")
                conn.close()
                return
            
            c.execute("SELECT seats FROM trainer WHERE trainer_id=?",(TrainerID.get(),))
            seats = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM reservations WHERE trainer_id=?", (TrainerID.get(),))
            reserve_count = c.fetchone()[0]

            if reserve_count >= seats:
                messagebox.showwarning("Seat Full","Seat is fully booked!")
                conn.close()
                return
            c.execute("INSERT INTO reservations (full_name, phone_number, gmail, trainer_id) VALUES (?,?,?,?)",(Name.get().title(), PhoneNo.get(), Gmail.get(), TrainerID.get()))

            messagebox.showinfo("Records","Inserted Successfully")
            conn.commit()
            conn.close()

            Name.delete(0, END)
            Gmail.delete(0, END)
            PhoneNo.delete(0, END)
            TrainerID.delete(0, END)
            query()

        def query():
            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()

            c.execute("""SELECT r.reservation_id, r.full_name, r.phone_number, r.gmail,
                      t.trainer_name, t.phone_number, t.gmail,
                      t.vehicle, t.duration, t.time_shift
                      FROM reservations r
                      LEFT JOIN trainer t
                      ON r.trainer_id = t.trainer_id""")
            
            records = c.fetchall()
            conn.close()

            for widget in table_inner.winfo_children():
                widget.destroy()

            headings = [
                "Reservation ID", "Reserver Name", "Reserver Phone No", "Reserver Gmail",
                "Trainer name", "Trainer Phone No", "Trainer Gmail",
                "Vehicle", "Duration", "Time Shift"
            ]

            for col, heading in enumerate(headings):
                lbl = Label(table_inner, text= heading, bg="#000000",fg="#ffffff", font=("Inter", 10, "bold"), borderwidth=1, relief="solid",padx=3, pady=3)
                lbl.grid(row=0, column=col, sticky="nsew", pady=(20,10))


            for row_index, record in enumerate(records, start=1):
                safe = [str(x) if x is not None else "-" for x in record]
                for col_index, value in enumerate(safe):
                    lbl = Label(table_inner, text= value, bg="#000000", fg="#ffffff", font=("Inter", 10), borderwidth=1, relief="solid", padx=3, pady=3)
                    lbl.grid(row=row_index, column=col_index, sticky="nswe")

            for col in range(len(headings)):
                table_inner.grid_columnconfigure(col, weight=1)

        def delete():
            if not ReservationID_entry.get():
                messagebox.showerror("Input Error","Please enter an ID to delete!")
                return
            conn= sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()

            c.execute("SELECT reservation_id FROM reservations WHERE reservation_id=?",(ReservationID_entry.get(),))
            reservation = c.fetchone()

            if reservation is None:
                messagebox.showwarning("Invalid Reservation ID","the entered Reservation ID does not exist!")
                conn.close()
                return 
            
            c.execute("DELETE FROM reservations WHERE reservation_id=?",(ReservationID_entry.get(),))
            conn.commit()
            conn.close()
            ReservationID_entry.delete(0, END)
            query()

        def edit():
            if not ReservationID_entry.get().strip():
                messagebox.showerror("Input Error","Please enter a Reservation ID!")
                return
            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()

            c.execute("SELECT reservation_id FROM reservations WHERE reservation_id=?",(ReservationID_entry.get(),))

            reservation = c.fetchone()

            if reservation is None:
                messagebox.showwarning("Invalid Reservation ID","The entered Reservation ID does not exists!")
                conn.close()
                return
            

            # ----------- new window to edit-------------
            global top_editor

            top_editor = Toplevel()
            top_editor.title("Update Data")
            top_editor.geometry("300x400")

            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()

            record_id = ReservationID_entry.get()
            c.execute("SELECT * FROM reservations WHERE reservation_id=?", (record_id,))
            records= c.fetchall()
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
            Label(top_editor, text= "Gmail").grid(row=1, column=0)
            Label(top_editor, text="Phone Number").grid(row=2, column=0)
            Label(top_editor, text="Trainer ID").grid(row=3, column=0)

            for record in records:
                name_editor.insert(0, record[1])
                phoneno_editor.insert(0, record[2])
                gmail_editor.insert(0, record[3])
                trainerid_editor.insert(0, record[4])

            Button(top_editor, text= "Save", command=update).grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=50)
        
        def update():
            if not name_editor.get():
                messagebox.showwarning("Input Error", "Name is required", parent= top_editor)
                return
                
            if not gmail_editor.get():
                messagebox.showwarning("Input Error", "Gmail is required", parent= top_editor)
                return
            
            if "@gmail.com" not in gmail_editor.get():
                messagebox.showwarning("Input Error", "Invalid Gmail ID", parent= top_editor)
                return
            
            if not phoneno_editor.get():
                messagebox.showwarning("Input Error", "Phone Number is required", parent= top_editor)
                return
            
            if len(phoneno_editor.get())!=10 or not phoneno_editor.get().isdigit():
                messagebox.showwarning("Input Error","Invalid Phone Number", parent=top_editor)
                return
            
            if not trainerid_editor.get():
                messagebox.showwarning("Input Error", "Trainer ID is required", parent= top_editor)
                return
            
            if not trainerid_editor.get().isdigit():
                messagebox.showwarning("Input Error", "Invalid Trainer ID", parent= top_editor)
                return
            

            conn = sq.connect("DrivingCourseregistration.db")
            c= conn.cursor()

            c.execute("SELECT trainer_id FROM trainer WHERE trainer_id=?", (trainerid_editor.get(),))

            trainer = c.fetchone()

            if trainer is None:
                messagebox.showwarning("Invalid Trainer ID","The entered Trainer ID does not exist!", parent=top_editor)
                conn.close()
                return
            c.execute("SELECT seats FROM trainer WHERE trainer_id=?",(trainerid_editor.get(),))
            seats = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM reservations WHERE trainer_id=?",(trainerid_editor.get(),))
            reserver_count = c.fetchone()[0]

            if reserver_count>=seats:
                messagebox.showwarning("Seat Full","Seat is fully booked!",parent= top_editor)
                conn.close()
                return
                
            data = (name_editor.get().title(), gmail_editor.get(), phoneno_editor.get(), trainerid_editor.get(), ReservationID_entry.get())

            c.execute("UPDATE reservations SET full_name=?, gmail=?, phone_number=?, trainer_id=? WHERE reservation_id=?", data)
            messagebox.showinfo("Records","Updated Successfully")
            conn.commit()
            conn.close()
            query()

            ReservationID_entry.delete(0, END)
            top_editor.destroy()
            
        def search():
            conn= sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()

            c.execute("""SELECT r.reservation_id, r.full_name, r.phone_number, r.gmail,
                      t.trainer_name, t.phone_number, t.gmail, t.vehicle, t.duration, t.time_shift
                      FROM reservations r
                      LEFT JOIN trainer t
                      ON r.trainer_id = t.trainer_id""")
            records = c.fetchall()
            conn.close()

            for widget in table_inner.winfo_children():
                widget.destroy()
            
            headings = [
                "Reservation ID", "Reserver Name", "Reserver Phone No", "Reserver Gamil",
                "Trainer Name", "Trainer Phone No", "Trainer Gmail",
                "Vehicle", "Duration", "Time Shift"
            ]

            for col, heading in enumerate(headings):
                lbl= Label(table_inner, text= heading, bg="#000000", fg="#ffffff", font=("Inter",10,"bold"), 
                           borderwidth=1, relief="solid", padx=3, pady=3)
                lbl.grid(row=0, column=col, sticky="nsew")

            found= False
            row_number = 1

            rname_search = reserver_name_search.get().strip().lower()
            tname_search = trainer_name_search.get().strip().lower()

            for record in records:
                reserver_name = str(record[1]).lower()
                trainer_name = str(record[4]).lower()

                if (rname_search == "" or rname_search in reserver_name) and (tname_search == "" or tname_search in trainer_name):
                    found=True

                    for col_index, value in enumerate(record):
                        lbl = Label(table_inner, text= str(value),
                                    bg="#000000", fg="#ffffff", font=('Inter', 10), 
                                    borderwidth= 1, relief= "solid", padx= 3, pady= 3)
                        lbl.grid(row= row_number, column= col_index, sticky= "nsew")

                    row_number+=1

            if not found:
                    lbl = Label(table_inner, text="No record Found", bg="#000000", fg="red", font=("Inter",12,"bold"))
                    lbl.grid(row=2, column= 0, columnspan= len(headings))

            for col in range(len(headings)):
                    table_inner.grid_columnconfigure(col, weight=1)


            
        
        # ------------ CRUD FRAME --------------------
        crud =  Frame(root, bg="#0f1b4c", width= 440)
        crud.pack(side= LEFT, fill= BOTH, padx=5)
        
        Label(crud, text= "Full Name: ", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        Name = Entry(crud)
        Name.pack(fill=X, padx=10, pady=5)
        
        Label(crud, text="Gmail: ", fg="#ffffff",bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        Gmail= Entry(crud, width= 48)
        Gmail.pack(fill= X, padx=10, pady=5)
        
        Label(crud, text="Phone Number:", fg="#ffffff", bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        PhoneNo= Entry(crud, width= 48)
        PhoneNo.pack(fill= X, padx= 10, pady= 5)
        
        Label(crud, text="Trainer ID: ",fg="#ffffff",bg="#0f1b4c").pack(anchor=W, padx=10, pady=(10,0))
        TrainerID = Entry(crud, width= 48)
        TrainerID.pack(fill=X, padx=10, pady=5)
        
        Button(crud, text="Add", bg="#E900E9", command=add).pack(pady=10, fill=X, padx=10)
        Button(crud, text="Show Records", bg="#000000", fg="#ffffff", command= query).pack(pady=10, fill= X, padx = 10)
        
        
        # ---------------- CONTENT FRAME ---------------
        content= Frame(root, bg="#000000",bd=1, relief="solid", height=50)
        content.pack(fill="x", padx=5)
        
        #------------ Update Frame------------------ 
        ud= Frame(content, bg="#2d7680",bd=1, relief="solid", height=50)
        ud.pack(side= LEFT, fill="y", padx=5, pady=5)
        
        Label(ud, text="Reservation ID:",fg="#000000", font=("Arial",8, "bold")).grid(row=0, column=0, padx=10, pady=(25,10))
        ReservationID_entry = Entry(ud, width=36, bg="#CED1D3", fg="#000000")
        ReservationID_entry.grid(row=0, column=1, padx=(5,10), pady=(25,10), sticky="w")
        
        Button(ud, text="Update", bg="#E900E9",fg="#000000", command=edit).grid(row=1,column=0, padx=(10,0),pady=40, sticky="w")
        Button(ud, text="Delete",bg="#E900E9", fg="#000000", command=delete).grid(row=1, column=1, pady=40, sticky="w")
        
        #--------- Search Frame -------------------------------

        find= Frame(content, bg="#2d7680", bd=1, relief="solid", height=50)
        find.pack(side=LEFT, fill="y", padx=(0,5), pady=5)

        Label(find, text="Search By:", bg="#2d7680",fg="#000000", font=("Arial", 11,"bold")).grid(row=2, column=0, pady=(10,0), sticky="w")
        
        Label(find, text= "Reserver Name: ", fg="#000000", font=("Arial",8,"bold")).grid(row=4, column=0, padx=10, sticky="w")
        reserver_name_search = Entry(find, width=40, bg="#CED1D3", fg="#000000")
        reserver_name_search.grid(row=4, column=1, padx=5, pady=10, sticky= "w")
        
        Label(find, text="Trainer Name: ", fg="#000000", font=("Arial",8,"bold")).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        trainer_name_search= Entry(find, width=40, bg="#CED1D3", fg="#000000")
        trainer_name_search.grid(row=5, column=1, padx=5, pady=10, sticky="w")

        Button(find, text="Search", bg="#830404", fg="#FFFFFF", command= search).grid(row=6, column=0, padx=(20,0), pady=20, sticky="w")




        #-------------------- TABLE FRAME -------------------------
        table = Frame(root, bg="#ffffff", bd=1, relief="solid")
        table.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

        table_container = Frame(table)
        table_container.pack(fill= BOTH, expand= True)

        table_canvas = Canvas(table_container, bg="#0F0F0F", highlightthickness=0)
        table_canvas.grid(row=0, column=0, sticky="nsew")

        v_scroll = Scrollbar(table_container, orient= VERTICAL, command=table_canvas.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")

        h_scroll = Scrollbar(table_container, orient=HORIZONTAL, command= table_canvas.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")

        table_canvas.configure(
            yscrollcommand= v_scroll.set,
            xscrollcommand= h_scroll.set
        )

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        table_inner = Frame(table_canvas, bg="#000000")
        table_window = table_canvas.create_window((0,0), window = table_inner, anchor="nw")


        def _resize_table(event):
            table_canvas.configure(scrollregion=table_canvas.bbox("all"))
            
        table_inner.bind("<Configure>", _resize_table)



    # ------------ sidebar buttons -------------------
    icons["home"]= ImageTk.PhotoImage(Image.open("home.ico").resize((30,30)))
    home_btn = Button(sidebar, image=icons["home"])
    home_btn.place(x=50, y=100)
    Label(sidebar, text="Home", fg="#000000").place(x=50, y=150)


    icons["records"]= ImageTk.PhotoImage(Image.open("report.ico").resize((30,30)))
    record_btn = Button(sidebar, image=icons["records"], command= onclick_record_btn)
    record_btn.place(x=50, y=200)
    Label(sidebar, text="Reservation Record", fg="#000000").place(x=20, y= 250)

    icons["trainer"]= ImageTk.PhotoImage(Image.open("report.ico").resize((30,30)))
    trainer_btn = Button(sidebar, image=icons["trainer"])
    trainer_btn.place(x=50, y=320)
    Label(sidebar, text="Trainer Details", fg="#000000").place(x=30, y= 370)

if __name__=="__main__":
    DCR_admin()
    root.mainloop()