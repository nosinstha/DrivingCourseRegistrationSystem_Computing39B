from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3 as sq

root = Tk()
root.title("Driving Course Registration System")
root.geometry("900x600")

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

icons = {}

def DCR_admin():
    clear_window()

    # ---------- Side Frame -------------
    sidebar = Frame(root, bg="#ffffff", bd=1, relief="solid", width=140)
    sidebar.pack(side= LEFT, fill="y")

    def reset_button_color():
        home_btn.config(bg="#ffffff")
        record_btn.config(bg="#ffffff")
        trainer_btn.config(bg="#ffffff")


    def clear_main_area():
        for widget in root.winfo_children():
            if widget!=sidebar:
                widget.destroy()


    def onclick_trainer_btn():
        reset_button_color()
        clear_main_area()

        trainer_btn.config(bg="#6a88ff")

        # ------------- CRUD ----------------

        def add():
            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")

            if not Name.get():
                messagebox.showwarning("Input Error","Name is required")
                return
            
            if not Gmail.get():
                messagebox.showwarning("Input Error","Gmail is required")
                return
            
            if "@gmail.com" not in Gmail.get():
                messagebox.showwarning("Input Error","Invalid Gmail ID")
                return
            
            if not PhoneNo.get():
                messagebox.showwarning("Input Error","Phone Number is required")
                return
            
            if len(PhoneNo.get())!=10 or not PhoneNo.get().isdigit():
                messagebox.showwarning("Input Error","Invalid Phone Number")
                return
            
            if vc.get()==" ":
                messagebox.showwarning("Input Error","Select a vehicle from option")
                return
            
            if dc.get()==" ":

                messagebox.showwarning("Input Error","Select a course package from option.")
                return
             
            if tc.get() == " ":
                messagebox.showwarning("Input Error","Select time shift from option.")
                return
            
            if not seat.get():
                messagebox.showwarning("Input Error","Number of seats is required")
                return
            
            if not seat.get().isdigit():
                messagebox.showwarning("Input Error","Invalid Input")
                return
            
            c.execute("INSERT INTO trainer (trainer_name, phone_number, gmail, vehicle, duration, time_shift, seats) VALUES (?,?,?,?,?,?,?)",
                      (Name.get().title(), PhoneNo.get(), Gmail.get(), vc.get(), dc.get(), tc.get(), seat.get()))
            
            messagebox.showinfo("Records","Inserted Successfully")
            conn.commit()
            conn.close()

            Name.delete(0, END)
            Gmail.delete(0, END)
            PhoneNo.delete(0, END)
            query()


        def query():
                conn = sq.connect("DrivingCourseRegistration.db")
                c= conn.cursor()
                c.execute("SELECT trainer_id, trainer_name, phone_number, gmail, vehicle, duration, time_shift, seats FROM trainer")

                records = c.fetchall()
                conn.close()

                for widget in table_inner.winfo_children():
                    widget.destroy()
                    
                headings= [
                    "Trainer ID", "Trainer Name", "Trainer Phone No", "Trainer Gmail",
                      "Vehicle", "Duration","Time Shift","No of Seats"
                ]

                for col,heading in enumerate(headings):
                    lbl = Label(table_inner, text=heading, bg="#000000", fg="#ffffff", 
                                font=("Inter",10,"bold"), borderwidth=1, relief="solid", padx=3, pady=3)
                    lbl.grid(row=0, column= col, sticky="nsew", pady=(20,10))

                for row_index, record in enumerate(records, start=1):
                    safe = [str(x) if x is not None else "-" for x in record]
                    for col_index, value in enumerate(safe):
                        lbl= Label(table_inner, text=value, bg="#000000", fg="#ffffff", font=("Inter", 10), borderwidth=1, relief="solid", padx=3, pady=3)
                        lbl.grid(row= row_index, column = col_index, sticky="nsew")

                for col in range(len(headings)):
                    table_inner.grid_columnconfigure(col, weight=1)

        def delete():
                if not TrainerID_entry.get():
                    messagebox.showerror("Input Error","Please enter an ID to delete!")
                    return
                
                conn = sq.connect("DrivingCourseRegistration.db")
                c= conn.cursor()

                c.execute("SELECT trainer_id FROM trainer WHERE trainer_id=?",(TrainerID_entry.get(),))

                reservation = c.fetchone()
                if reservation is None:
                    messagebox.showwarning("invalid Trainer ID","the entered Trainer ID does not exist!")
                    conn.close()
                    return
                
                c.execute("DELETE FROM trainer WHERE trainer_id=?",(TrainerID_entry.get(),))
                conn.commit()
                conn.close()
                TrainerID_entry.delete(0, END)
                messagebox.showinfo("Success","Deleted Successfully")
                query()

        def edit():
                if not TrainerID_entry.get().strip():
                    messagebox.showerror("Input Error","Please enter a Trainer ID!")
                    return
                
                conn= sq.connect("DrivingCourseRegistration.db")
                c= conn.cursor()

                c.execute("SELECT trainer_id FROM trainer WHERE trainer_id=?",(TrainerID_entry.get(),))
                reservation = c.fetchone()

                if reservation is None:
                    messagebox.showwarning("invalid Trainer ID","The entered Trainer ID does not exist!")
                    conn.close()
                    return
                
                global top_update
                top_update = Toplevel()
                top_update.title("Update Data")
                top_update.geometry("400x700")

                conn = sq.connect("DrivingCourseRegistration.db")
                c= conn.cursor()

                record_id = TrainerID_entry.get()
                record_id = TrainerID_entry.get()

                c.execute("Select * FROM trainer WHERE trainer_id = ?",(record_id,))
                records = c.fetchall()
                conn.close()

                global name_update, gmail_update, phoneno_update, seat_update, ev, de, et

                name_update = Entry(top_update, width=30)
                name_update.grid(row=0, column= 1, padx= 20, pady=(10,0))
                gmail_update = Entry(top_update, width=30)
                gmail_update.grid(row=1, column=1)
                phoneno_update = Entry(top_update, width=30)
                phoneno_update.grid(row=2, column=1)
                seat_update = Entry(top_update, width= 30)
                seat_update.grid(row=21, column=1)

                ev= StringVar()
                ev.set(records[0][4])

                Radiobutton(top_update, text="car", variable=ev, value="car").grid(row=5, column=0)
                Radiobutton(top_update, text="scooter", variable=ev, value="scooter").grid(row=6, column=0)
                Radiobutton(top_update, text="motorbike", variable=ev, value="motorbike").grid(row=7, column=0)


                de= StringVar()
                de.set(records[0][5])

                Radiobutton(top_update, text="7 Days", variable=de, value="7 Days").grid(row=10, column=0)
                Radiobutton(top_update, text="15 Days", variable=de, value="15 Days").grid(row=11, column=0)
                Radiobutton(top_update, text="30 Days", variable=de, value="30 Days").grid(row=12, column=0)
                Radiobutton(top_update, text="3 Months", variable= de, value="3 Months").grid(row=13, column=0)

                et= StringVar()
                et.set(records[0][6])
                Radiobutton(top_update, text="8am-10am", variable=et, value="8am-10am").grid(row=16, column=0)
                Radiobutton(top_update, text="10am-12pm", variable=et, value="10am-12pm").grid(row=17, column=0)
                Radiobutton(top_update, text="12pm-2pm", variable=et, value="12pm-2pm").grid(row=18, column=0)
                Radiobutton(top_update, text="2pm-4pm", variable=et, value="2pm-4pm").grid(row=19, column=0)


                Label(top_update, text="Full Name").grid(row=0, column=0,pady=(10,0))
                Label(top_update, text="Gmail").grid(row=1, column=0)
                Label(top_update, text= "Phone Number").grid(row=2, column=0)
                Label(top_update, text="Vehicle: ").grid(row=4, column=0)
                Label(top_update, text="Time Shift: ").grid(row=15, column=0)
                Label(top_update, text="Course Package: ").grid(row=9, column=0)
                Label(top_update, text="No of Seats: ").grid(row=21, column=0)

                name_update.insert(0, records[0][1])
                phoneno_update.insert(0, records[0][2])
                gmail_update.insert(0, records[0][3])
                seat_update.insert(0, records[0][7])

                Button(top_update, text="Save", command=update).grid(row=23, column=0, columnspan=2, pady=10, padx=10, ipadx=50)

        def update():
            conn = sq.connect("DrivingCourseRegistration.db")
            c= conn.cursor()

            if not name_update.get():
                messagebox.showwarning("Input Error", "Name is required",parent=top_update)
                return
            if not gmail_update.get():
                messagebox.showwarning("Input Error","Email is required")
                return
            if "@gmail.com" not in gmail_update.get():
                messagebox.showwarning("Input Error","Invalid Gmail ID", parent=top_update)
                return
            if not phoneno_update.get():
                messagebox.showwarning("Input Error","Phone number is required", parent=top_update)
                return
            if len(phoneno_update.get())!=10 or not phoneno_update.get().isdigit():
                messagebox.showwarning("Input Error","Invalid Phone Number", parent=top_update)
                return
            if not seat_update.get():
                messagebox.showwarning("Input Error", "Invalid Trainer ID", parent=top_update)
                return
            if not TrainerID_entry.get():
                messagebox.showwarning("Input Error","Trainer ID is required", parent=top_update)
                return
            if not TrainerID_entry.get().isdigit():
                messagebox.showwarning("Input Error","Invalid Trainer ID")
                return
            
            data = (name_update.get().title(), phoneno_update.get(), gmail_update.get(), ev.get(), de.get(), et.get(), seat_update.get(), TrainerID_entry.get())
            c.execute("UPDATE trainer SET trainer_name=?, phone_number=?, gmail=?, vehicle=?, duration=?, time_shift=?, seats=? WHERE trainer_id=?",data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Updated Successfully")
            query()
            top_update.destroy()
            



        # ------------ CRUD FRAME --------------
        crud = Frame(root, bg="#0f1b4c", width=440)
        crud.pack(side=LEFT, fill=BOTH, padx=5)
        Label(crud, text=".", font=("Inter",1), bg="#0f1b4c").pack(padx=150)

        crud_canvas = Canvas(crud, bg="#0f1b4c", highlightthickness=0)
        crud_canvas.pack(side= LEFT, fill= BOTH, expand= True)

        crud_scrollbar = Scrollbar(crud, orient= VERTICAL, command= crud_canvas.yview)
        crud_scrollbar.pack(side=RIGHT, fill=Y)

        crud_canvas.configure(yscrollcommand=crud_scrollbar.set)

        scrollable_frame = Frame(crud_canvas, bg="#0f1b4c")
        crud_canvas.create_window((0,0), window= scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: crud_canvas.configure(scrollregion=crud_canvas.bbox("all"))
        )

        Label(scrollable_frame, text=".", font=("Inter",1), bg="#0f1b4c").pack(pady=5)

        # Name field
        Label(scrollable_frame, text="Full Name: ", fg="#ffffff", bg="#0f1b4c",font=("Ariel",8,"bold")).pack(anchor=W, padx=10, pady=(0,0))
        Name= Entry(scrollable_frame, width =30)
        Name.pack(fill= X, padx= 10, pady= 5)

        # Gamil field

        Label(scrollable_frame, text="Gmail: ", fg="#ffffff", bg="#0f1b4c",font=("Ariel",8,"bold")).pack(anchor=W, padx=10, pady=(10,0))
        Gmail = Entry(scrollable_frame, width= 30)
        Gmail.pack(fill= X, padx= 10, pady= 5)


        # PhoneNo field
        Label(scrollable_frame, text="Phone No: ", fg="#ffffff", bg="#0f1b4c",font=("Ariel",8,"bold")).pack(anchor=W, padx=10, pady=(10,0))
        PhoneNo = Entry(scrollable_frame, width= 30)
        PhoneNo.pack(fill= X, padx= 10, pady= 5)

        Label(scrollable_frame, text="Choose: ",font=("Inconsolata",10,"bold"),fg="#ffffff", bg="#0f1b4c").pack(pady=15, anchor=W, padx=10)


        #------------- Crud Radio Buttons -----------

        #vehicle choice
        Label(scrollable_frame, text="Vehicle: ", fg="#ffffff",bg="#0f1b4c",font=("Ariel",8,"bold")).pack(anchor=W, padx=10,pady=(10,0))

        vc= StringVar()
        vc.set(" ")

        v1= Radiobutton(scrollable_frame, text="car", variable=vc, value="car")
        v1.pack(anchor=W, padx=10, pady=(10,0))

        v2= Radiobutton(scrollable_frame, text="scooter", variable=vc, value="scooter")
        v2.pack(anchor=W, padx=10, pady=(10,0))

        v3= Radiobutton(scrollable_frame, text="motorbike", variable=vc, value="motorbike")
        v3.pack(anchor=W, padx=10, pady=(10,0))


        #course package choice
        Label(scrollable_frame, text="Course Package: ", fg="#ffffff",bg="#0f1b4c",font=("Ariel",8,"bold")).pack(anchor=W, padx=10, pady=(20,0))

        dc= StringVar()
        dc.set(" ")

        d1= Radiobutton(scrollable_frame, text="7 Days", variable=dc, value="7 Days")
        d1.pack(anchor=W, padx=10, pady=(10,0))


        d2= Radiobutton(scrollable_frame, text="15 Days", variable=dc, value="15 days")
        d2.pack(anchor=W, padx=10, pady=(10,0))

        d3 = Radiobutton(scrollable_frame, text= "30 Days", variable=dc, value="30 Days")
        d3.pack(anchor=W, padx=10, pady=(10,0))


        #course package choice
        Label(scrollable_frame, text="Time_shift: ", fg="#ffffff",bg="#0f1b4c",font=("Ariel",8,"bold")).pack(anchor=W, padx=10, pady=(20,0))

        tc= StringVar()
        tc.set(" ")

        t1= Radiobutton(scrollable_frame, text="8am-10am",variable=tc, value="8am-10am")
        t1.pack(anchor=W, padx=10, pady=(10,0))

        t2= Radiobutton(scrollable_frame, text="10am-12pm",variable=tc, value="10am-12pm")
        t2.pack(anchor=W, padx=10, pady=(10,0))

        t3= Radiobutton(scrollable_frame, text="12pm-2pm", variable= tc, value="12pm-2pm")
        t3.pack(anchor=W, padx=10, pady=(10,0))

        t4= Radiobutton(scrollable_frame, text="2pm-4pm", variable=tc, value="2pm-4pm")
        t4.pack(anchor=W, padx=10, pady=(10,0))

        #seat field
        Label(scrollable_frame, text="Number of Seats:",fg="#ffffff",bg="#0f1b4c", font=("Ariel",8,"bold")).pack(anchor=W, padx=10, pady=(30,0))
        seat= Entry(scrollable_frame, width=30)
        seat.pack(fill=X, padx=10, pady=(5,30))

        #add button
        Button(scrollable_frame, text="Add",bg="#E900E9", command=add, font=("Ariel",8,"bold")).pack(pady=(20,10), fill=X, padx=10)

        #show record button
        Button(scrollable_frame, text="Show Records", bg="#000000",fg="#ffffff", command=query, font=("Ariel",8,"bold")).pack(pady=(10,30),fill=X, padx=10)

        #----------- Content Frame--------------
        content = Frame(root, bg="#FFFFFF", bd=1, relief="solid",height=50)
        content.pack(fill="x")

        Label(content, text="Trainer ID: ", bg="#000000",fg="#ffffff").pack(side= LEFT, padx= 10, pady= 10)
        TrainerID_entry = Entry(content, width=50, bg="#becfdd",fg="#000000")
        TrainerID_entry.pack(side= LEFT, padx= 10, pady= 10)

        Button(content, text="Update",bg="#E900E9", fg="#000000", command= edit).pack(side=LEFT, padx=10, pady=10)
        Button(content, text="Delete",bg="#E900E9", fg="#000000", command= delete).pack(side=LEFT, padx=10, pady=10)


        # ------------- Table Frame ------------

        table = Frame(root, bg="#000000", bd=1, relief="solid")
        table.pack(side=RIGHT, fill= BOTH, expand=True)

        table_container = Frame(table)
        table_container.pack(fill=BOTH, expand= True)

        table_canvas = Canvas(table_container, bg="#000000", highlightthickness=0)
        table_canvas.grid(row= 0, column= 0, sticky="nsew")

        v_scroll = Scrollbar(table_container, orient=VERTICAL, command=table_canvas.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")

        h_scroll= Scrollbar(table_container, orient= HORIZONTAL, command=table_canvas.xview)
        h_scroll.grid(row=1, column=0, stick="ew")

        table_canvas.configure(
            yscrollcommand=v_scroll.set,
            xscrollcommand= h_scroll.set
        )

        table_container.grid_rowconfigure(0, weight = 1)
        table_container.grid_columnconfigure(0, weight=1)

        table_inner = Frame(table_canvas, bg="#000000")
        table_window = table_canvas.create_window((0,0), window= table_inner,anchor="nw")

        def _resize_table(event):
            table_canvas.configure(scrollregion=table_canvas.bbox("all"))
            
        table_inner.bind("<Configure>", _resize_table)




    
    # --------- sidebar buttons -----------------
    icons["home"] = ImageTk.PhotoImage(Image.open("home.ico").resize((30,30)))
    home_btn = Button(sidebar, image=icons["home"])
    home_btn.place(x=50, y=100)
    Label(sidebar, text="Home",fg="#000000").place(x=50, y=150)

    icons["records"]= ImageTk.PhotoImage(Image.open("report.ico").resize((30,30)))
    record_btn = Button(sidebar, image= icons["records"])
    record_btn.place(x=50, y=200)
    Label(sidebar, text= "Reservation Records").place(x=20, y=250)

    icons["trainer"]= ImageTk.PhotoImage(Image.open("table.ico").resize((30,30)))
    trainer_btn = Button(sidebar, image= icons["trainer"], command=onclick_trainer_btn)
    trainer_btn.place(x=50,y=320)
    Label(sidebar, text="Trainer Details", fg="#000000").place(x=30, y= 370)

if __name__=="__main__":
    DCR_admin()
    root.mainloop()