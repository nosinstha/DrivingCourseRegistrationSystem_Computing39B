from tkinter import*
from PIL import Image,ImageTk
from tkinter import messagebox, ttk
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
    #----------SIDE FRAME---------
    sidebar = Frame(root,bg="#ffffff",bd=1,relief="solid",width=140)
    sidebar.pack(side=LEFT,fill="y")

    def reset_button_color():
        home_btn.config(bg="#ffffff")
        record_btn.config(bg="#ffffff")
        trainer_btn.config(bg="#ffffff")

    def clear_main_area():
        for widget in root.winfo_children():
            if widget !=sidebar:
                widget.destroy()



    def onclick_home_btn():
        reset_button_color()
        home_btn.config(bg="#6a88ff")
        clear_main_area()

        #------------Header------------
        header = Frame(root, bg="#0f1b4c")
        header.pack(fill="x")

        Label(header, text="Hi Admin, Welcome !",
              font=("Josefin Sans",22,"bold"),
              fg="#ffffff",bg="#0f1b4c").pack(pady=20)
        
        #-------------FILTER--------------
        filter = Frame(root, bg="#939e2d")
        filter.pack(fill="x",pady=5)

        Label(filter, text="Filter :",
              font=("Inter",16,"bold"),
              bg="#939e2d",fg="#1D1D1D").pack(side=LEFT, padx=20,pady=40)
        

        global clicked_vehicle, clicked_course_package, clicked_time_shift, clicked_course_category
        clicked_course_category = StringVar(value="---Course Category---")
        OptionMenu(filter, clicked_vehicle,"fully Booked","Unbooked").pack(side=LEFT,padx=5)

        clicked_course_category = StringVar(value="---Vehicle---")
        OptionMenu(filter, clicked_vehicle,"car","van","scooter","motorbike").pack(side=LEFT,padx=5)

        clicked_course_category = StringVar(value="---Course Package---")
        OptionMenu(filter, clicked_vehicle,"7 days","15 days","30 days","3 months").pack(side=LEFT,padx=5)

        clicked_course_category = StringVar(value="---Time Shift---")
        OptionMenu(filter, clicked_vehicle,"8am-10am","10am-12pm","12pm-2pm","2pm-4pm").pack(side=LEFT,padx=5)


        #---------CONTENT AREA--------
        content = Frame(root, bg="#fffff", bd=1, relief="solid")
        content.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)


        content_canvas = Canvas(content, bg="#ffffff", highlightthickness=0)
        content_canvas.pack(side=LEFT, fill= BOTH, expand=True)

        Scrollbar_frame = Scrollbar(content, orient=VERTICAL, command=content_canvas.yview)
        content_canvas.pack(side=LEFT, fill= Y)

        content_canvas.configure(yscrollcommand= scrollbar.set)

        Scrollable_frame = Frame(content_canvas,bg="#ffffff")
        canvas_window = content_canvas.create_window((0,0), window=Scrollable_frame, anchor="nw")

        content_canvas.bind("<Configure>",lambda e:
            content_canvas.itemconfig(canvas_window, width=e.width))
        
        Scrollable_frame.bind("<Configure>", lambda e:
            content_canvas.itemconfig(scrollregion=content_canvas.bbox("all")))
        


        #--------- QUERY --------
        def query():
            for widget in Scrollable_frame.winfo_children():
                widget.destroy()

            conn = sq.connect("DrivingCourseRegistration.db")
            c = conn.cursor()
            c.execute('SELECT * FROM trainer')
            records = c.fetchall()

            found = False
            for record in records:
                trainer_id = record[0]
                seats = int(record[7])

                c.execute("SELECT COUNT(*) FROM reservations WHERE trainer_id=?",(trainer_id,))
                reserve_count = c.fetchone()[0]

                category = "Fully Booked" if reserve_count >=seats else "Unbooked"


                if clicked_course_category.get() not in ("---Course Category---", category):
                    continue    
                if clicked_vehicle.get() not in ("---Vehicle---", record[4]):
                    continue
                if clicked_course_package.get() not in ("---Course Package---", record[5]):
                    continue
                if clicked_time_shift.get() not in ("---Time Shift---", record[6]):
                    continue

                found= True

                card= Frame(Scrollable_frame, bg="#0f1b4c")
                card.pack(fill='x',padx=15, pady=10)

                card.columnconfigure(0, weight=1)
                card.columnconfigure(1, weight=0)
                details = Frame(card, bg="#0f1b4c")
                details.grid(row=0, column=0, sticky= "w", padx=20, pady=15)

                Label(details, text=f"Trainer : {record[1]}\n",
                  font=('Inter',16,"bold"),
                  fg="#ffffff", bg="#0f1b4c").pack(anchor="w")
            

                Label(details,
                    text=(f"vehicle : {record[4]}\n"
                        f"Package : {record[5]}\n"
                        f"Time Shift : {record[6]}\n"
                        f"Status : {category}\n\n"
                        f"Phone Number : {record[2]}\n"
                        f"gmail : {record[3]}\n\n"),
                    font=("Inter",10),
                    fg="#e0e0e0",
                    bg="#0f1b4c",
                    justify="left").pack(anchor="w", pady=6)
            
                Label(details, text=f"seats left : {seats - reserve_count}\n",
                    font=('Inter',12,"bold"),
                    fg="#ffffff", bg="#0f1b4c").pack(anchor="w")
                
                action = Frame(card, bg="#0f1b4c")
                action.grid(row=0, column=1, sticky="e", padx=25)

                if category == "Unbooked":
                    Button(action, text="Book Course",
                        bg="#DA07C4", fg="#FFFFFF",
                        font=("Inter",10,"bold"),
                        command=lambda tid=trainer_id: open_booking(tid)).pack()
                else:
                    Label(action, text="FULL",
                        fg="red", bg="#0f1b4c",
                        font=("Inter",10,"bold")).pack(side=RIGHT)
                
                    
            conn.close()

            if not found:
                    Label(Scrollable_frame, text="No trainers found with the selected filters.",
                        fg="red", bg="#FFFFFF",
                        font=("Inter",16,"bold")).pack(pady=100)
                    
        query()

        Button(filter, text="Search",
            bg="#830404", fg="#ffffff",
            font=("Inter",10,"bold"),
            command=query).pack(side=LEFT, padx=8)
            

        def open_booking(trainer_id):
            top = Toplevel()
            top.title("Book Course")
            top.geometry("350x420")

            Label(top, text="Your Full Name :").pack(pady=(10, 0))
            reserver_name=Entry(top, width=30)
            reserver_name.pack()

            Label(top, text="Your Phone Number :").pack(pady=(10, 0))
            reserver_phoneno=Entry(top, width=30)
            reserver_phoneno.pack()

            Label(top, text="Your Gmail :").pack(pady=(10, 0))
            reserver_gmail=Entry(top, width=30)
            reserver_gmail.pack()

            conn = sq.connect("DrivingCourseRegistratiom.db")
            c = conn.cursor()
            c.execute("SELECT * FROM trainer WHERE trainer_id=?", (trainer_id,))
            t = c.fetchone()
            conn.close()

            Label(top, text=f"\nTrainer: {t[1]}").pack()
            Label(top, text=f"Vehicle: {t[4]}").pack()
            Label(top, text=f"Package: {t[5]}").pack()
            Label(top, text=f"Time Shift: {t[6]}").pack()


            def save():
                conn = sq.connect("DrivingCourseRegistratiom.db")
                c = conn.cursor()

                if not reserver_name.get() :
                    messagebox.showwarning("Input Error", "Name is required",parent=top)
                    return
                        
                if not reserver_gmail.get() :
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


     # ===================== SIDEBAR BUTTONS =====================
    icons["home"] = ImageTk.PhotoImage(Image.open("home.ico").resize((30, 30)))
    home_btn = Button(sidebar, image=icons["home"], command= onclick_home_btn)
    home_btn.place(x=50, y=100)
    Label(sidebar,text="Home",fg="#000000").place(x=50, y=150)



    icons["record"] = ImageTk.PhotoImage(Image.open("report.ico").resize((30, 30)))
    record_btn = Button(sidebar, image=icons["record"])
    record_btn.place(x=50, y=200)
    Label(sidebar,text="Reservation Records",fg="#000000").place(x=20, y=250)



    icons["trainer"] = ImageTk.PhotoImage(Image.open("table.ico").resize((30, 30)))
    trainer_btn = Button(sidebar, image=icons["trainer"])
    trainer_btn.place(x=50, y=320)
    Label(sidebar,text="Trainer Details",fg="#000000").place(x=30, y=370)

if __name__ == "__main__":
    DCR_admin()
    root.mainloop()  
                
                
            



                    
                    
                    
                    
                    



                        

        


        




            





            
        

