from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Driving Course Registration")
root.geometry("900x900")


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#### Heading Frame
header = Frame(root, bg="#0f1b4c")
header.pack(fill="x")

header_label = Label(header, text = "Hi User, Welcome ! ", font = ("Josefins Sans",22,"bold"), fg="#ffffff", bg="#0f1b4c")
header_label.pack(expand=True,pady=20)


#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#### Sidebar Frame
sidebar = Frame(root,bg="#ffffff",bd=1,relief="solid",width=140)
sidebar.pack(side=LEFT,fill="y")

def reset_button_color():
    home_btn.config(bg="#ffffff")
    reservation_btn.config(bg="#ffffff")
    profile_btn.config(bg="#ffffff")

def onclick_home_btn():
    reset_button_color()
    home_btn.config(bg="#6a88ff")

def onclick_reservation_btn():
    reset_button_color()
    reservation_btn.config(bg="#6a88ff")


def onclick_profile_btn():
    reset_button_color()
    profile_btn.config(bg="#6a88ff")


# Home Icon Button
home_icon = Image.open("home.ico").resize((30,30))
resized_home_icon = ImageTk.PhotoImage(home_icon)

home_btn = Button(sidebar, image= resized_home_icon, anchor=W, command=onclick_home_btn)
home_btn.place(x=50,y=100)

Label(sidebar,text="Home",font=("Inder",10,'bold'),fg="#000000",bg="#ffffff").place(x=45,y=140)


# Your Reservation Icon Button
reservation_icon = Image.open("report.ico").resize((30,30))
resized_reservation_icon = ImageTk.PhotoImage(reservation_icon)

reservation_btn = Button(sidebar, image = resized_reservation_icon, anchor=W, font=("Inder",12),command=onclick_reservation_btn)
reservation_btn.place(x=50,y=200)

Label(sidebar,text="Your\nReservation",font=("Inder",10,"bold"), fg="#000000",bg="#ffffff").place(x=28,y=240)



# Profile Button
profile_icon = Image.open("profile.ico").resize((30,30))
resized_profile_icon = ImageTk.PhotoImage(profile_icon)

profile_btn = Button(sidebar, image = resized_profile_icon, anchor=W,command=onclick_profile_btn)
profile_btn.place(x=50,y=540)

Label(sidebar,text="Profile",font=("Inder",10,"bold"),fg="#000000",bg="#ffffff").place(x=43,y=580)


#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
#### Filter Frame

filter = Frame(root,bg="#9aa728")
filter.pack(fill="x",padx=5,pady=5)

Label(filter, text="Filter :",font=("Inter",16,"bold"),bg="#9aa728",fg="#1D1D1D").pack(side=LEFT,padx=20,pady=40)



# Vehicle Choice
vehicle_options = [
    "car",
    "van",
    "scooter",
    "motorbike"
]

clicked_vehicle = StringVar()
clicked_vehicle.set("---Vehicle---")

drop_vehicles = OptionMenu(filter,clicked_vehicle,*vehicle_options)
drop_vehicles.pack(side=LEFT, padx=5)

label_vehicles= Label(filter,text="", bg="#9aa728",fg="#1D1D1D",font=("Inter",12,"bold"))
label_vehicles.pack(side=LEFT, padx=5)


# Course Package Choice 
course_package_options = [
    "7 Days",
    "15 Days",
    "30 Days",
    "3 Months"
]

clicked_course_package = StringVar()
clicked_course_package.set("---Course Package---")

drop_course_packages = OptionMenu(filter, clicked_course_package, *course_package_options)
drop_course_packages.pack(side=LEFT,padx=5)

label_course_packages = Label(filter,text="",fg="#1D1D1D",bg="#9aa728",font=("Inter",12,"bold"))
label_course_packages.pack(side=LEFT,padx=5)


# Time Shift Choice
time_shift_options = [
    "8am - 10am",
    "10am - 12 pm",
    "12pn - 2 pm",
    "2pm - 4pm"
]

clicked_time_shift = StringVar()
clicked_time_shift.set("---Time Shift---")

drop_time_shifts = OptionMenu(filter, clicked_time_shift, *time_shift_options)
drop_time_shifts.pack(side=LEFT,padx=5)

label_time_shifts = Label(filter, text="",fg="#1D1D1D", bg="#9aa728",font=("Inter",12,"bold"))
label_time_shifts.pack(side=LEFT,padx=5)



# search button
def onclick_search_btn():
    pass

search_btn = Button(filter, text="Search", font=("Inter",10,"bold"), fg="#ffffff",bg="#000000", activebackground="#AA2800", activeforeground="#FFFFFF", command=onclick_search_btn)
search_btn.pack(side=LEFT, padx=5)


#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# Content Frame
content = Frame(root,bg="#ffffff",bd=1,relief="solid")
content.pack(side=RIGHT,fill=BOTH, expand=TRUE,padx=10,pady=10)



mainloop()