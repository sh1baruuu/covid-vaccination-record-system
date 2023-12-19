#COVID VACCINATION RECORD SYSTEM
# ADVANCED DATABASE MANAGEMENT SYSTEM
# FINAL REQUIREMENTS

#ADMIN ( USERNAME: admin | PASSWORD: admin123 )

from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import datetime
from datetime import date
import time as tm
from tkinter import messagebox as msgbox
from PIL import ImageTk,Image
from tkcalendar import DateEntry

w = Tk()
w.geometry("900x540+170+25")
w.title("COVID|Vaccination Record System")
w.resizable(False, False)
img_VRS = PhotoImage(file="icon2.png")
w.iconphoto(True, img_VRS)

style = ttk.Style()
style.layout('TNotebook.Tab', [])
notebook = ttk.Notebook(w)

tab1 = Frame(notebook)
tab2 = Frame(notebook)
tab3 = Frame(notebook)
tab4 = Frame(notebook)
tab5 = Frame(notebook)
tab6 = Frame(notebook)
tab7 = Frame(notebook)
tab8 = Frame(notebook)
tab9 = Frame(notebook)

tab10 = Frame(notebook)
notebook.add(tab1)
notebook.add(tab2)
notebook.add(tab3)
notebook.add(tab4)
notebook.add(tab5)
notebook.add(tab6)
notebook.add(tab7)
notebook.add(tab8)
notebook.add(tab9)
notebook.add(tab10)

notebook.pack(expand=TRUE, fill='both')

#=======================================================================================================================

c = sql.connect('covid_vrs.db')
cur = c.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Admin (
	"AdminID"	INTEGER,
	"Username"	INTEGER,
	"Password"	TEXT,
	PRIMARY KEY("AdminID" AUTOINCREMENT)
);""")

cur.execute("""CREATE TABLE IF NOT EXISTS Individuals (
	"TrackingCode"	INTEGER,
	"LastName"	TEXT,
	"FirstName"	TEXT,
	"MiddleName"	REAL,
	"DateofBirth"	TEXT,
	"Age"	INTEGER,
	"Sex"	TEXT,
	"Address"	TEXT,
	"Contact"	INTEGER,
	"Vaccination Status"	TEXT,
	"AdminID"	INTEGER DEFAULT '1060',
	"UserID"	INTEGER,
	FOREIGN KEY("AdminID") REFERENCES "Admin"("AdminID"),
	FOREIGN KEY("UserID") REFERENCES "Users"("UserID"),
	PRIMARY KEY("TrackingCode" AUTOINCREMENT)
);""")

cur.execute("""CREATE TABLE IF NOT EXISTS Users (
	"UserID"	INTEGER,
	"FirstName"	TEXT,
	"LastName"	TEXT,
	"Sex"	TEXT,
	"Age"	INTEGER,
	"Address"	TEXT,
	"Username"	TEXT,
	"Password"	TEXT,
	"AdminID"	INTEGER DEFAULT '1060',
	PRIMARY KEY("UserID" AUTOINCREMENT),
	FOREIGN KEY("AdminID") REFERENCES "Admin"("AdminID")
);""")

cur.execute("""CREATE TABLE IF NOT EXISTS Vaccination_Details (
	"VaccinationDetailNo"	INTEGER,
	"TrackingCode"	INTEGER,
	"VaccinationRemarks"	TEXT,
	"VaccineID"	INTEGER,
	"VaccinationLocation"	TEXT,
	"VaccinatorID"	INTEGER,
	"VaccinationDate"	TEXT,
	"AdminID"	INTEGER DEFAULT '1060',
	PRIMARY KEY("VaccinationDetailNo" AUTOINCREMENT),
	FOREIGN KEY("AdminID") REFERENCES "Admin"("AdminID"),
	FOREIGN KEY("VaccinatorID") REFERENCES "Vaccinators"("VaccinatorID"),
	FOREIGN KEY("TrackingCode") REFERENCES "Individuals"("TrackingCode"),
	FOREIGN KEY("VaccineID") REFERENCES "Vaccines"("VaccineID")
);""")

cur.execute("""CREATE TABLE IF NOT EXISTS Vaccinators (
	"VaccinatorID"	INTEGER,
	"Name"	TEXT,
	"Sex"	TEXT,
	"Address"	TEXT,
	"Email"	TEXT,
	"Contact"	INTEGER,
	"AdminID"	INTEGER DEFAULT '1060',
	PRIMARY KEY("VaccinatorID" AUTOINCREMENT),
	FOREIGN KEY("AdminID") REFERENCES "Admin"("AdminID")
);""")

cur.execute("""CREATE TABLE IF NOT EXISTS Vaccines (
	"VaccineID"	INTEGER,
	"VaccineBrand"	TEXT,
	"AdminID"	INTEGER DEFAULT '1060',
	FOREIGN KEY("AdminID") REFERENCES "Admin",
	PRIMARY KEY("VaccineID" AUTOINCREMENT)
);""")

cr = c.cursor()
cr.execute("SELECT COUNT(AdminID) FROM Admin WHERE AdminID='1060'")
x = str(cr.fetchone()).strip('(,)')

if x == 0:
    cr.execute("""INSERT INTO Admin ( AdminID, Username, Password ) VALUES ( 1060, "admin", "admin123" )""")


c.commit()
c.close()



#=======================================================================================================================

today = date.today()


def clear_all():
   for item in tr_view.get_children():
      tr_view.delete(item)


def refresh():
    c = sql.connect("covid_vrs.db")
    cursor = c.cursor()
    cursor.execute("SELECT * FROM Individuals")

    data = cursor.fetchall()
    for d in data:
        tr_view.insert("", END, values=(d[0], d[1], d[2], d[9]))
    c.close()


def vaccine_change2(event):
    v = vaccine_id2.get()
    c = sql.connect('covid_vrs.db')
    cr = c.cursor()
    query = "SELECT VaccineID FROM Vaccines WHERE VaccineBrand LIKE ?"
    cr.execute(query, [v])
    vaccines = str(cr.fetchall())
    id = vaccines.strip('[(,)]')
    vaccine_id2.set(id)
    c.close()


def vaccinator_change2(event):
    vrt = vaccinator_id2.get()
    vr = vrt.strip('{}')
    c = sql.connect('covid_vrs.db')
    cr = c.cursor()
    query = "SELECT VaccinatorID FROM Vaccinators WHERE Name LIKE ?"
    cr.execute(query, [vr])
    vaccines = str(cr.fetchall())
    id = vaccines.strip('[(,)]')
    vaccinator_id2.set(id)
    c.close()


def select_tab9():
    notebook.select(tab9)


def add_vaxd2():
    c = sql.connect('covid_vrs.db')
    cr = c.cursor()
    query2 = "Select TrackingCode from Individuals Order by TrackingCode Desc limit  1"
    cr.execute(query2)
    do = cr.fetchall()
    for a in do:
        tr_code = a[0]

    un = username.get()
    cur = c.cursor()
    q1 = "SELECT UserID FROM Users WHERE Username = ?"
    cur.execute(q1, [un])
    rows = str(cur.fetchall())

    userid = rows.strip('[(,)]')  # USERID
    id = tr_code                  # TRACKING CODE
    vax_date = today.strftime("%d/%m/%Y")  # VAX DATE
    vax_remarks = remarks2.get()  # VAX REMARKS
    vax_address = address2.get()  # VAX ADDRESS
    vax_id = vaccine_id2.get()  # VAX ID
    vaxr_id = vaccinator_id2.get()  # VAXR

    c.close()

    check_counter = 0
    warn = ""

    if vax_address == "":
        warn = "Address can't be empty"
    else:
        check_counter += 1

    if vaxr_id == "":
        warn = "VaccinatorID can't be empty"
    else:
        check_counter += 1

    if vax_id == "":
        warn = "VaccineID can't be empty"
    else:
        check_counter += 1

    if vax_remarks == "":
        warn = "VaccinatorID can't be empty"
    else:
        check_counter += 1

    if check_counter == 4:

        try:
            c = sql.connect('covid_vrs.db')
            cr = c.cursor()
            insert_query = """INSERT INTO Vaccination_Details (TrackingCode, VaccinationRemarks, VaccineID,
                                VaccinationLocation, VaccinatorID, VaccinationDate, UserID )
                                    VALUES (?, ?, ?, ?, ?, ?, ?) """
            data = (id, vax_remarks, vax_id, vax_address, vaxr_id, vax_date, userid)

            cr.execute(insert_query, data)

            c.commit()
            c.close()

            msgbox.showinfo('Information', 'New Vaccinee registered!')

            select_tab4()
            clear_all()
            refresh()

        except Exception as ep:
            msgbox.showerror('', ep)

    else:
        msgbox.showerror('Error', warn)


def vaxd_back():
    individual_view()


def select_tab8():
    notebook.select(tab8)
    open_vaxd()


def open_vaxd():

    tr = trc.get()
    print(tr)
    style.configure('no.Treeview.Heading', font=f3)
    style.configure("no.Treeview", rowheight=88, font=f8)

    col_val = "REMARKS", "VACCINE", "VACCINATOR", "ADDRESS", "DATE", "ENCODER#"

    tr_view = ttk.Treeview(tr_frame, columns=col_val, selectmode='extended', show='headings', height=22, style="no.Treeview")
    tr_view.place(height=380, width=855,x=15, y=10)
    for each in col_val:
        tr_view.column(each, width=80, anchor='center')
        tr_view.heading(each, text=each.capitalize())


    c = sql.connect("covid_vrs.db")
    cur = c.cursor()
    query = """SELECT Vaccination_Details.VaccinationRemarks,
                        Vaccines.VaccineBrand,
                        Vaccinators.Name,  
                        Vaccination_Details.VaccinationLocation,
                        Vaccination_Details.VaccinationDate,
                        Users.UserID
                        FROM  Vaccines LEFT JOIN Vaccination_Details LEFT JOIN Vaccinators LEFT JOIN Users
                        WHERE  Vaccination_Details.VaccineID = Vaccines.VaccineID AND Vaccination_Details.TrackingCode = ?
                        AND Vaccination_Details.VaccinatorID = Vaccinators.VaccinatorID AND Vaccination_Details.UserID = Users.UserID """

    cur.execute(query, [tr])

    data = cur.fetchall()
    for d in data:
        tr_view.insert("", END, values=(d[0],d[1],d[2],d[3],d[4],d[5]))


def select_tab7():
    notebook.select(tab7)


def vaccine_change(event):
    v = vaccine_id.get()
    c = sql.connect('covid_vrs.db')
    cr = c.cursor()
    query = "SELECT VaccineID FROM Vaccines WHERE VaccineBrand LIKE ?"
    cr.execute(query, [v])
    vaccines = str(cr.fetchall())
    id = vaccines.strip('[(,)]')
    vaccine_id.set(id)
    c.close()


def vaccinator_change(event):
    vrt = vaccinator_id.get()
    vr = vrt.strip('{}')
    c = sql.connect('covid_vrs.db')
    cr = c.cursor()
    query = "SELECT VaccinatorID FROM Vaccinators WHERE Name LIKE ?"
    cr.execute(query, [vr])
    vaccines = str(cr.fetchall())
    id = vaccines.strip('[(,)]')
    vaccinator_id.set(id)
    c.close()


def add_vaxd():
    selection = tr_view.selection()[0]
    un = username.get()

    c = sql.connect('covid_vrs.db')
    cr = c.cursor()
    q1 = "SELECT UserID FROM Users WHERE Username = ?"
    cr.execute(q1, [un])
    rows = str(cr.fetchall())

    userid = rows.strip('[(,)]')                            #USERID
    id = tr_view.item(selection)['values'][0]               #TRACKING CODE
    vax_date = today.strftime("%d/%m/%Y")                   #VAX DATE
    vax_remarks =  remarks.get()                            #VAX REMARKS
    vax_address = address.get()                             #VAX ADDRESS
    vax_id = vaccine_id.get()                               #VAX ID
    vaxr_id = vaccinator_id.get()                           #VAXR

    check_counter = 0
    warn = ""

    if vax_address == "":
        warn = "Address can't be empty"
    else:
        check_counter += 1

    if vaxr_id == "":
        warn = "VaccinatorID can't be empty"
    else:
        check_counter += 1

    if vax_id == "":
        warn = "VaccineID can't be empty"
    else:
        check_counter += 1

    if vax_remarks == "":
        warn = "VaccinatorID can't be empty"
    else:
        check_counter += 1


    if check_counter == 4:

        try:
            c = sql.connect('covid_vrs.db')
            cr = c.cursor()
            insert_query = """INSERT INTO Vaccination_Details (TrackingCode, VaccinationRemarks, VaccineID,
                                VaccinationLocation, VaccinatorID, VaccinationDate, UserID )
                                    VALUES (?, ?, ?, ?, ?, ?, ?) """
            data = ( id, vax_remarks, vax_id, vax_address, vaxr_id, vax_date, userid )

            cr.execute(insert_query, data)

            c.commit()
            c.close()

            msgbox.showinfo('Information', 'Vaccination Details Added!')
            select_tab4()
            vaccinator_id.set("")
            vaccine_id.set("")
            remarks.set("")
            address.delete(0, END)

        except Exception as ep:
            msgbox.showerror('', ep)

    else:
        msgbox.showerror('Error', warn)


def back_to_view():
    individual_view()
    vaccinator_id.set("")
    vaccine_id.set("")
    remarks.set("")
    address.delete(0,END)


def back_searching():
    search_vaccinee()
    code_entry.focus()
    code_entry.delete(0,END)


def create_id():
    c = sql.connect('covid_vrs.db')
    user = username_entry.get()
    get_id = "Select UserID From Users Where Username = ? "
    cr = c.cursor()
    cr.execute(get_id, [user])
    retrieve = cr.fetchall()
    for x in retrieve:
        uiid = x[0]

    insert_query = """INSERT INTO Individuals (LastName, FirstName, MiddleName, DateofBirth, Age, Sex, Address, Contact, VaccinationStatus, UserID )
                                               VALUES ("","","","","","","","","",?) """
    cr.execute(insert_query, [uiid])
    c.commit()


def next():
    check_counter = 0
    warn = ""
    if reg_lname.get() == "":
        warn = "Lastname can't be empty"
    else:
        check_counter += 1

    if reg_fname.get() == "":
        warn = "Firstname can't be empty"
    else:
        check_counter += 1

    if reg_mname.get() == "":
        warn = "Middlename can't be empty"
    else:
        check_counter += 1

    if reg_dob.get() == "":
        warn = "Date of Birth can't be empty"
    else:
        check_counter += 1

    if reg_age.get() == "":
        warn = "Age can't be empty"
    else:
        check_counter += 1

    if reg_sex.get() == "":
        warn = "Please select your sex"
    else:
        check_counter += 1

    if reg_address.get() == "":
        warn = "Address can't be empty"
    else:
        check_counter += 1

    if reg_con.get() == "":
        warn = "Contact can't be empty"
    else:
        check_counter += 1


    if check_counter == 8:

        c = sql.connect("covid_vrs.db")
        check = c.cursor()
        query = "SELECT EXISTS(SELECT * from Individuals WHERE FirstName LIKE ? AND LastName LIKE ?)"
        val = (reg_fname.get(), reg_lname.get())
        check.execute(query, val)
        if check.fetchone() == (1,):
            msgbox.showerror('Error', 'The is already registered!')
            reg_lname.delete(0, END)
            reg_fname.delete(0, END)
            reg_mname.delete(0, END)
            reg_address.delete(0, END)
            reg_con.delete(0, END)
            reg_age.set("")
        else:
            try:
                c = sql.connect('covid_vrs.db')
                cr = c.cursor()
                query2 = "Select TrackingCode from Individuals Order by TrackingCode Desc limit  1"
                cr.execute(query2)
                do = cr.fetchall()
                for a in do:
                    tr_code = a[0]
                print(tr_code)




                d1 = (reg_lname.get(), tr_code)
                d2 = (reg_fname.get(), tr_code)
                d3 = (reg_mname.get(), tr_code)
                d4 = (reg_dob.get(), tr_code)
                d5 = (reg_age.get(), tr_code)
                d6 = (reg_sex.get(), tr_code)
                d7 = (reg_address.get(), tr_code)
                d8 = (reg_con.get(), tr_code)
                d9 = ("VACCINATED", tr_code)

                q1 = "UPDATE Individuals SET LastName = ? WHERE TrackingCode = ?"
                q2 = "UPDATE Individuals SET FirstName = ? WHERE TrackingCode = ?"
                q3 = "UPDATE Individuals SET MiddleName = ? WHERE TrackingCode = ?"
                q4 = "UPDATE Individuals SET DateofBirth = ? WHERE TrackingCode = ?"
                q5 = "UPDATE Individuals SET Age = ? WHERE TrackingCode = ?"
                q6 = "UPDATE Individuals SET Sex = ? WHERE TrackingCode = ?"
                q7 = "UPDATE Individuals SET Address = ? WHERE TrackingCode = ?"
                q8 = "UPDATE Individuals SET Contact = ? WHERE TrackingCode = ?"
                q9 = "UPDATE Individuals SET VaccinationStatus = ? WHERE TrackingCode = ?"

                cr.execute(q1, d1)
                cr.execute(q2, d2)
                cr.execute(q3, d3)
                cr.execute(q4, d4)
                cr.execute(q5, d5)
                cr.execute(q6, d6)
                cr.execute(q7, d7)
                cr.execute(q8, d8)
                cr.execute(q9, d9)

                c.commit()
                select_tab9()

            except Exception as ep:
                msgbox.showerror('', ep)
    else:
        msgbox.showerror('Error', warn)


def tab6_return():
    yes = msgbox.askyesno('Ask', 'Do you want to discard registration?')
    if yes == 1:
        reg_lname.delete(0, END)
        reg_fname.delete(0, END)
        reg_mname.delete(0, END)
        reg_address.delete(0, END)
        reg_con.delete(0, END)
        reg_sex.set('')
        reg_age.set('')

        c = sql.connect('covid_vrs.db')
        cr = c.cursor()
        cr.execute("SELECT TrackingCode FROM Individuals ORDER BY TrackingCode DESC LIMIT 1")
        get_id= str(cr.fetchall())
        id = get_id.strip('[(,)]')
        query = "Delete From Individuals Where TrackingCode = ? "

        cr.execute(query, [id])
        c.commit()

        select_tab4()


def select_tab6():
    create_id()
    notebook.select(tab6)


def select_tab1():
    notebook.select(tab1)
    start()
    code_entry.delete(0, END)


def search_vaccinee():
    select_tab5()
    staff_back_btn.place(x=200, y=450)
    staff_btn3.place(x=0, y=485)


def select_tab5_n():
    select_tab5()
    code_entry.delete(0, END)
    code_entry.focus()


def select_tab5():
    notebook.select(tab5)
    code_entry.focus()


def find():
    notebook.select(tab3)
    id = tracking_code.get()
    trc.set(id)
    query = "Select * From Individuals Where TrackingCode = ? "

    iid = StringVar()
    fn = StringVar()
    ln = StringVar()
    mn = StringVar()
    idob = StringVar()
    iage = StringVar()
    iadd = StringVar()
    isex = StringVar()
    icon = StringVar()
    vaxstat = StringVar()

    c = sql.connect('covid_vrs.db')
    cr = c.cursor()
    cr.execute(query, [id])
    rows = cr.fetchall()
    for i in rows:
        iid.set(i[0])
        fn.set(i[1])
        ln.set(i[2])
        mn.set(i[3])
        idob.set(i[4])
        iage.set(i[5])
        isex.set(i[6])
        iadd.set(i[7])
        icon.set(i[8])
        vaxstat.set(i[9])

        vaxs = Label(top_level3, textvariable=vaxstat, font=('Courier', 8, 'bold'), width=25, bg=c3, fg=c4)
        status = Label(top_level3, text="VACCINATION STATUS:", font=('Courier', 7, 'bold'), width=20, bg=c3, fg=c4)
        no = Label(top_level3, text="#", font=('Courier', 15, 'bold'), width=1, bg=c3, fg=c4)
        l1 = Label(top_level3, textvariable=iid, font=('Courier', 15, 'bold'), width=8, bg=c3, fg=c4)
        l2 = Label(top_level3, textvariable=fn, font=f4, width=66, bg=c3, fg=c4)
        l3 = Label(top_level3, textvariable=ln, font=f4, width=20, bg=c3, fg=c4)
        l4 = Label(top_level3, textvariable=mn, font=f4, width=15, bg=c3, fg=c4)
        l5 = Label(top_level3, textvariable=iadd, font=f4, width=35, bg=c3, fg=c4)
        l6 = Label(top_level3, textvariable=icon, font=f4, width=13, bg=c3, fg=c4)
        l7 = Label(top_level3, textvariable=idob, font=f4, width=18, bg=c3, fg=c4)
        l8 = Label(top_level3, textvariable=iage, font=f4, width=5, bg=c3, fg=c4)
        l9 = Label(top_level3, textvariable=isex, font=f4, width=15, bg=c3, fg=c4)

        l1.place(x=143, y=225)
        l2.place(x=350, y=146)
        l3.place(x=355, y=146)
        l4.place(x=692, y=146)
        l5.place(x=407, y=199)
        l6.place(x=723, y=199)
        l7.place(x=439, y=246)
        l8.place(x=618, y=246)
        l9.place(x=705, y=246)

        no.place(x=130, y=225)
        vaxs.place(x=100, y=368)
        status.place(x=140, y=355)
        Guest_back_btn.place(x=200, y=450)

        iiage = int(iage.get())
        if isex.get() == "Male":
            if iiage < 60:
                guest = Label(top_level3, image=male, bg=c3)
            else:
                guest = Label(top_level3, image=old_m, bg=c3)
        else:
            if iiage < 60:
                guest = Label(top_level3, image=female, bg=c3)
            else:
                guest = Label(top_level3, image=old_f, bg=c3)

        guest.place(x=113, y=68)

        c.close()


def limitSize(*args):
    value3 = tracking_code.get()
    if len(value3) > 8: tracking_code.set(value3[:8])


def logout():
    notebook.select(tab1)
    start()
    username_entry.delete(0, END)
    password_entry.delete(0, END)


def guestpage():
    guest_btn3.place(x=0, y=485)
    select_tab5()


def staff_view():

    uid = StringVar()
    fname = StringVar()
    lname = StringVar()
    sex = StringVar()
    age = StringVar()
    ads = StringVar()
    un = StringVar()
    up = StringVar()

    u_name = username.get()
    u_pass = password.get()
    query = "Select * From Users Where Username = ? And Password = ?"
    u_info = (u_name, u_pass)
    c = sql.connect("covid_vrs.db")
    cc = c.cursor()
    cc.execute(query, u_info)
    rows = cc.fetchall()
    for i in rows:
        uid.set(i[0])
        fname.set(i[1])
        lname.set(i[2])
        sex.set(i[3])
        age.set(i[4])
        ads.set(i[5])
        un.set(i[6])
        up.set(i[7])

    if sex.get() == "Male":
        worker = Label(top_level2, image=doctor, bg=c3)
    else:
        worker = Label(top_level2, image=nurse, bg=c3)

    worker.place(x=55, y=100)

    ln12 = Label(top_level2, text="\t    Last Name\t\t\t     First Name\t    ", font=f2, bg=c3, fg=c4)
    ln3 = Label(top_level2, text="__________________________________________________________________", font=f2, bg=c3,
                fg=c4)
    ln45 = Label(top_level2, text="Address: _________________________________________________________", font=f2, bg=c3,
                 fg=c4)
    ln6 = Label(top_level2, text="Age: ___________________________  Sex: ___________________________", font=f2, bg=c3,
                fg=c4)
    ln7 = Label(top_level2, text=("USER_"), font=('Courier', 18, 'bold'), width=5, bg=c3, fg=c2)
    ln8 = Label(top_level2, text="USERNAME: ", font=f4, bg=c3, fg=c4)
    ln9 = Label(top_level2, text="PASSWORD: ", font=f4, bg=c3, fg=c4)
    ln77 = Label(top_level2, textvariable=uid, font=('Courier', 18, 'bold'), width=4, bg=c3, fg=c2)
    ln88 = Label(top_level2, textvariable=un, width=15, font=f4, bg=c3, fg=c4)
    ln99 = Label(top_level2, text="----------", width=15, font=f4, bg=c3, fg=c4)

    ln12.place(x=315, y=192)
    ln3.place(x=315, y=172)
    ln45.place(x=315, y=245)
    ln6.place(x=315, y=310)
    ln7.place(x=85, y=310)
    ln8.place(x=60, y=355)
    ln9.place(x=60, y=374)
    ln77.place(x=158, y=310)
    ln88.place(x=125, y=355)
    ln99.place(x=125, y=374)

    l1 = Label(top_level2, textvariable=fname, font=f3, width=25, bg=c3, fg=c4)
    l2 = Label(top_level2, textvariable=lname, font=f3, width=25, bg=c3, fg=c4)
    l3 = Label(top_level2, textvariable=ads, font=f3, width=45, bg=c3, fg=c4)
    l4 = Label(top_level2, textvariable=age, font=f3, width=21, bg=c3, fg=c4)
    l5 = Label(top_level2, textvariable=sex, font=f3, width=20, bg=c3, fg=c4)

    l1.place(x=550, y=166)
    l2.place(x=308, y=166)
    l3.place(x=375, y=239)
    l4.place(x=352, y=304)
    l5.place(x=592, y=304)

    print("staff view")


def selected():
    try:
        selection = tr_view.selection()[0]
        id = tr_view.item(selection)['values'][0]
        trc.set(id)
    except:
        msgbox.showinfo('Information', "Please select first at the table!")
    else:
        individual_view()


def delete_records():
    try:
        selection = tr_view.selection()[0]
        id = tr_view.item(selection)['values'][0]
    except:
        msgbox.showinfo('Information', "Please select first at the table!")
    else:
       query = "Delete From Individuals Where TrackingCode = ? "
       print(id)
       c = sql.connect('covid_vrs.db')
       cr = c.cursor()
       cr.execute(query, [id])
       c.commit()
       tr_view.delete(selection)


def select_tab4():
    notebook.select(tab4)
    add_btn_frame.place(x=350, y=350)


def individual_view():

    notebook.select(tab3)
    selection = tr_view.selection()[0]
    id = tr_view.item(selection)['values'][0]
    query = "Select * From Individuals Where TrackingCode = ? "

    iid = StringVar()
    fn = StringVar()
    ln = StringVar()
    mn = StringVar()
    idob = StringVar()
    iage = StringVar()
    iadd = StringVar()
    isex = StringVar()
    icon = StringVar()
    vaxstat = StringVar()

    c = sql.connect('covid_vrs.db')
    cr = c.cursor()
    cr.execute(query, [id])
    rows = cr.fetchall()
    for i in rows:
        iid.set(i[0])
        fn.set(i[1])
        ln.set(i[2])
        mn.set(i[3])
        idob.set(i[4])
        iage.set(i[5])
        isex.set(i[6])
        iadd.set(i[7])
        icon.set(i[8])
        vaxstat.set(i[9])


        vaxs = Label(top_level3, textvariable=vaxstat, font=('Courier', 8, 'bold'), width=25, bg=c3, fg=c4)
        status = Label(top_level3, text="VACCINATION STATUS:", font=('Courier', 7, 'bold'), width=20, bg=c3, fg=c4)
        no = Label(top_level3, text="#", font=('Courier', 15, 'bold'), width=1, bg=c3, fg=c4)
        l1 = Label(top_level3, textvariable=iid, font=('Courier', 15, 'bold'), width=8, bg=c3, fg=c4)
        l2 = Label(top_level3,  textvariable=fn, font=f4, width=66, bg=c3, fg=c4)
        l3 = Label(top_level3, textvariable=ln, font=f4, width=20, bg=c3, fg=c4)
        l4 = Label(top_level3,  textvariable=mn, font=f4, width=15, bg=c3, fg=c4)
        l5 = Label(top_level3,  textvariable=iadd, font=f4, width=35, bg=c3, fg=c4)
        l6 = Label(top_level3,  textvariable=icon, font=f4, width=13, bg=c3, fg=c4)
        l7 = Label(top_level3,  textvariable=idob, font=f4, width=18, bg=c3, fg=c4)
        l8 = Label(top_level3, textvariable=iage, font=f4, width=5, bg=c3, fg=c4)
        l9 = Label(top_level3, textvariable=isex, font=f4, width=15, bg=c3, fg=c4)

        l1.place(x=143, y=225)
        l2.place(x=350, y=146)
        l3.place(x=355, y=146)
        l4.place(x=692, y=146)
        l5.place(x=407, y=199)
        l6.place(x=723, y=199)
        l7.place(x=439, y=246)
        l8.place(x=618, y=246)
        l9.place(x=705, y=246)

        no.place(x=130, y=225)
        vaxs.place(x=100, y=368)
        status.place(x=140, y=355)
        Lst_back_btn.place(x=200, y=450)


        if isex.get() == "Male":
            guest = Label(top_level3, image=male, bg=c3)
        else:
            guest = Label(top_level3, image=female, bg=c3)
        guest.place(x=113, y=68)

        c.close()


def limitSize(*args):
    value1 = username.get()
    value2 = password.get()
    if len(value1) > 20: username.set(value1[:20])
    if len(value2) > 20: password.set(value2[:20])


def enter_login():
    u_name = username.get()
    u_pass = password.get()
    u_info = (u_name, u_pass)
    c = sql.connect("covid_vrs.db")
    query1 =  "SELECT EXISTS(SELECT UserID from Users where Username = ?)"
    user = c.cursor()
    user.execute(query1, [u_name])
    if len(u_name) == 0:
        msgbox.showerror('Attention', 'Please enter your Username!')
    elif user.fetchone()==(1,):
        check = c.cursor()
        query1 = "Select COUNT(UserID) From Users where Username = ? and Password = ?"
        check.execute(query1, u_info)
        if check.fetchone()==(1,):
            staff_page1()
        else:
            password_entry.delete(0, END)
            msgbox.showerror('Warning', 'Incorrect Password! Try again')
    else:
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        msgbox.showerror('Attention', 'Username not found!')


def enter_staff():
    staff.place_forget()
    guest.place_forget()
    line.place_forget()
    staff_btn.place_forget()
    guest_btn.place_forget()
    back_btn.place(x=15, y=265)
    login_btn.place(x=256, y=265)
    username_frame.place(x=24, y=80)
    username_entry.place(relwidth=0.3, height=40, width=303,  relx=0.01)
    password_frame.place(x=24, y=165)
    password_entry.place(relwidth=0.3, height=40, width=303, relx=0.01)
    staff_label.place(x=23, y=15)
    username_entry.focus()


def start():
    title.destroy()
    start_button.destroy()
    tagline.destroy()
    staff.place(x=25, y=30)
    guest.place(x=266, y=30)
    line.place(x=244, height=1000)
    staff_btn.place(x=15, y=265)
    guest_btn.place(x=256, y=265)
    back_btn.place_forget()
    login_btn.place_forget()
    username_frame.place_forget()
    password_frame.place_forget()
    staff_label.place_forget()


def select_tab11():
    notebook.select(tab10)
    top1f()


def show_vaccinators():
    c = sql.connect("covid_vrs.db")
    cursor = c.cursor()
    cursor.execute("SELECT * FROM Vaccinators")

    data = cursor.fetchall()
    for d in data:
        vaxr_tree.insert("", END, values=d)
    c.close()


def delete_vaccinator():
    try:
        selection = vaxr_tree.selection()[0]
        id = vaxr_tree.item(selection)['values'][0]
    except:
        msgbox.showinfo('Information', "Please select first at the vaccinators table!")
    else:
        query = "Delete From Vaccinators Where VaccinatorID = ? "
        print(id)
        c = sql.connect('covid_vrs.db')
        cr = c.cursor()
        cr.execute(query, [id])
        c.commit()
        vaxr_tree.delete(selection)


def clear_vaxr_tree():
   for item in vaxr_tree.get_children():
      vaxr_tree.delete(item)


def add_new_vaccinator():
    name = vaxrn_e.get()
    sex = vaxsex.get()
    address = vaxadd_e.get()
    email = vaxem_e.get()
    contact = vaxcon_e.get()


    check_counter = 0
    warn = ""

    if name == "":
        warn = "Name can't be empty "
    else:
        check_counter += 1

    if sex == "":
        warn = "Sex can't be empty "
    else:
        check_counter += 1

    if address == "":
        warn = "Address can't be empty "
    else:
        check_counter += 1

    if email == "":
        warn = "Email can't be empty "
    else:
        check_counter += 1

    if contact == "":
        warn = "Contact can't be empty "
    else:
        check_counter += 1

    if check_counter==5:
        try:
            c = sql.connect('covid_vrs.db')
            cr = c.cursor()
            insert_query = """INSERT INTO Vaccinators (Name, Sex, Address, Email, Contact )
                                               VALUES (?, ?, ?, ?, ?) """

            data = (name, sex, address, email, contact )

            cr.execute(insert_query, data)

            c.commit()
            c.close()

            after_add_vaccinator()

            msgbox.showinfo('Information', 'New Vaccinator added!')

        except Exception as ep:
            msgbox.showerror('', ep)

    else:
        msgbox.showerror('Error', warn)


def after_add_vaccinator():
    vaxem_e.delete(0,END)
    vaxrn_e.delete(0, END)
    vaxcon_e.delete(0,END)
    vaxsex.set("")
    vaxadd_e.delete(0,END)
    clear_vaxr_tree()
    show_vaccinators()


def show_users():
    c = sql.connect("covid_vrs.db")
    cursor = c.cursor()
    cursor.execute("SELECT * FROM Users")

    data = cursor.fetchall()
    for d in data:
        user_tree.insert("", END, values=d)
    c.close()


def delete_user():
    try:
        selection = user_tree.selection()[0]
        id = user_tree.item(selection)['values'][0]
    except:
        msgbox.showinfo('Information', "Please select first at the users table!")
    else:
        query = "Delete From Users Where UserID = ? "
        print(id)
        c = sql.connect('covid_vrs.db')
        cr = c.cursor()
        cr.execute(query, [id])
        c.commit()
        user_tree.delete(selection)


def clear_user_tree():
   for item in user_tree.get_children():
      user_tree.delete(item)


def add_new_user():
    ln = ln_e.get()
    fn = fn_e.get()
    age = age_e.get()
    sex = sex_value.get()
    address = address_e.get()
    username = un_e.get()
    password = pass_e.get()


    check_counter = 0
    warn = ""

    if ln == "":
        warn = "Lastname can't be empty "
    else:
        check_counter += 1

    if fn == "":
        warn = "Firstname can't be empty "
    else:
        check_counter += 1

    if sex == "":
        warn = "Sex can't be empty "
    else:
        check_counter += 1

    if age == "":
        warn = "Age can't be empty "
    else:
        check_counter += 1

    if address == "":
        warn = "Address can't be empty "
    else:
        check_counter += 1

    if username == "":
        warn = "Username can't be empty "
    else:
        check_counter += 1

    if password == "":
        warn = "Password can't be empty "
    else:
        check_counter += 1

    if check_counter==7:
        try:
            c = sql.connect('covid_vrs.db')
            cr = c.cursor()
            insert_query = """INSERT INTO Users (FirstName, LastName, Sex, Age, Address, Username, Password )
                                               VALUES (?, ?, ?, ?, ?, ?, ?) """

            data = (fn, ln, sex, age, address, username, password)

            cr.execute(insert_query, data)

            c.commit()
            c.close()
            after_add_user()

            msgbox.showinfo('Information', 'New User registered!')

        except Exception as ep:
            msgbox.showerror('', ep)

    else:
        msgbox.showerror('Error', warn)


def after_add_user():
    ln_e.delete(0,END)
    fn_e.delete(0,END)
    age_e.delete(0,END)
    address_e.delete(0,END)
    un_e.delete(0,END)
    pass_e.delete(0,END)
    sex_value.set("")
    clear_user_tree()
    show_users()


def show_vaccines():
    c = sql.connect("covid_vrs.db")
    cursor = c.cursor()
    cursor.execute("SELECT * FROM Vaccines")

    data = cursor.fetchall()
    for d in data:
        vax_tree.insert("", END, values=d)
    c.close()


def delete_vaccines():
    try:
        selection = vax_tree.selection()[0]
        id = vax_tree.item(selection)['values'][0]
    except:
        msgbox.showinfo('Information', "Please select first at the vaccines table!")
    else:
        query = "Delete From Vaccines Where VaccineID = ? "
        print(id)
        c = sql.connect('covid_vrs.db')
        cr = c.cursor()
        cr.execute(query, [id])
        c.commit()
        vax_tree.delete(selection)


def clear_vaccines_tree():
    for item in vax_tree.get_children():
        vax_tree.delete(item)


def add_new_vaccines():
    brand = vaxbrand_e.get()

    check_counter = 0
    warn = ""

    if brand == "":
        warn = "Enter vaccine brand first!"
    else:
        check_counter += 1

    if check_counter == 1:
        try:
            c = sql.connect('covid_vrs.db')
            cr = c.cursor()
            insert_query = """INSERT INTO Vaccines (VaccineBrand)
                                               VALUES (?) """

            data = ([brand])

            cr.execute(insert_query, data)

            c.commit()
            c.close()
            after_add_vaccines()

            msgbox.showinfo('Information', 'New Vaccine added!')

        except Exception as ep:
            msgbox.showerror('', ep)

    else:
        msgbox.showerror('Error', warn)


def after_add_vaccines():
    vaxbrand_e.delete(0, END)
    clear_vaccines_tree()
    show_vaccines()


def top3f():  # vaccines back #goto vaccinator
    top3.pack(expand=TRUE, fill="both")
    clear_vaxr_tree()
    show_vaccinators()
    top2.pack_forget()
    top1.pack_forget()


def top2f():  # Vaccines
    top2.pack(expand=TRUE, fill="both")
    clear_vaccines_tree()
    show_vaccines()
    top3.pack_forget()


def top1f():  # vaccinator back
    top1.pack(expand=TRUE, fill="both")
    top3.pack_forget()
    clear_user_tree()
    show_users()


def unlock(*args):
    code = passcode.get()
    if code == "admin123":
        print("open")
        passcode.set("")
        admin_e.place_forget()
        select_tab11()


def staff_page1():
    notebook.select(tab2)
    staff_view()
    print("staffpage")
    add_btn_frame.place_forget()


def show_passcode_e():
    admin_e.place(x=60, y=10)
    admin_b2.place(x=10)
    admin_b.place_forget()


def hide_passcode_e():
    admin_b.place(x=10)
    admin_b2.place_forget()
    admin_e.place_forget()


def homepage():
    notebook.select(tab1)
    title.place(x=7, y=90)
    tagline.place(x=16, y=230)
    start_button.place(x=11, y=265)

image1 = Image.open('staff.png')
image2 = Image.open('guests.png')
image3 = Image.open('nurse.png')
image4 = Image.open('doctor.png')
image5 = Image.open('male.png')

image7= Image.open('female.png')
image9 = Image.open('shield.png')
image10 = Image.open('add_vax3.png')
image11 = Image.open('rec.png')
image12 = Image.open('edit.png')

image13 = Image.open('s8.png')
search = ImageTk.PhotoImage(image13.resize((33, 33)))
image15 = Image.open('admin4.png')
img1 = ImageTk.PhotoImage(image1.resize((200, 200)))
img2 = ImageTk.PhotoImage(image2.resize((200, 200)))
nurse = ImageTk.PhotoImage(image3.resize((200, 200)))
doctor = ImageTk.PhotoImage(image4.resize((200, 200)))
male = ImageTk.PhotoImage(image5.resize((150, 150)))
female = ImageTk.PhotoImage(image7.resize((150, 150)))
vac_stat = ImageTk.PhotoImage(image9.resize((50, 50)))
add_rec = ImageTk.PhotoImage(image10.resize((30, 30)))
view_rec = ImageTk.PhotoImage(image11.resize((30, 30)))
edit = ImageTk.PhotoImage(image12.resize((30, 30)))

admin = ImageTk.PhotoImage(image15.resize((40, 40)))

c1 = "#EFEFEF"
c2 = "#FF4155"
c3 = "#FFFFFF"
c4 = "#56415E"
c5 = "#56415E"


f1 = ('Calibri', 20, 'bold')
f2 = ('Courier', 9, 'normal')
f3 = ('Courier', 11, 'bold')
f4 = ('Courier', 8, 'bold')
f5 = ('Calibri', 15, 'bold')
f6 = ('Courier', 7, 'bold')
f7 = ('Calibri', 10, 'bold')
f8 =  ('Courier', 8, 'bold')
f9 =  ('Arial', 15, 'bold')
f10 = ('Calibri', 11, 'bold')
#=======================================================================================================================



top_level1 = Frame(tab1, relief="ridge", background=c1)
top_level1.pack(expand=TRUE, fill="both")

menu = Frame(top_level1, background=c2, relief="groove", bd=2, width=1010, height=50)
menu.place(x=-5)


admin_b = Button(menu, height=40, width=40, cursor="hand2", image=admin, relief="flat", activebackground=c2, bg=c2, command=show_passcode_e)



admin_b2 = Button(menu, height=40, width=40, cursor="hand2", image=admin, relief="flat", activebackground=c2, bg=c2, command=hide_passcode_e)


passcode = StringVar()
passcode.trace('w', unlock)
admin_e = Entry(menu, justify="center", font=f3, show='*', width=10, textvariable=passcode)

hide_passcode_e()


main_bd = Frame(top_level1, background=c4, relief="raised", width=500, height=350)
main_bd.place(x=195, y=100)
main_frame = Frame(main_bd, background=c3, relief="ridge", bd=3, width=497, height=346)
main_frame.place(x=2, y=2)

title = Label(main_frame, text="COVID|Vaccination Records", font=('Sitka Display', 25, 'bold'),
              foreground=c4, justify="center", background=c3, width=26)
title.place(x=7, y=90)
tagline = Label(main_frame, text="#GetVax to celebrate a healthier future", font=('System', 10), width=55,
                foreground=c4, justify="center", background=c3)
tagline.place(x=16, y=230)
start_button = Button(main_frame, text="GET STARTED", relief="groove", cursor="hand2", bd=2, font=f1, foreground=c3,
                      background=c2, width=33, command=start)
start_button.place(x=11, y=265)

staff = Label(main_frame, image=img1, bg=c3)
guest = Label(main_frame, image=img2, bg=c3)
line = ttk.Separator(main_frame)
staff_btn = Button(main_frame, text="STAFF", relief="groove", cursor="hand2", bd=2, font=f1, foreground=c3,
                   background=c2, width=15, command=enter_staff)
guest_btn = Button(main_frame, text="GUESTS", relief="groove", cursor="hand2", bd=2, font=f1, foreground=c3,
                   background=c2, width=15, command=guestpage)

back_btn = Button(main_frame, text="BACK", relief="groove", cursor="hand2", bd=2, font=f1, foreground=c3,
                  background=c2, width=15, command=start)
login_btn = Button(main_frame, text="LOGIN", relief="groove", cursor="hand2", bd=2, font=f1, foreground=c3,
                   background=c2, width=15, command=enter_login)

style.configure('Red.TLabelframe.Label', font=('courier', 15, 'bold'))
style.configure('Red.TLabelframe', background=c3)
style.configure('Red.TLabelframe',relief="sunken")
style.configure('Red.TLabelframe.Label', background=c3)
style.configure('Red.TLabelframe.Label', foreground=c4)

username_frame = ttk.Labelframe(main_frame, labelanchor="nw", relief="groove", style = "Red.TLabelframe", text="USERNAME",
                                 height=80, width=450)
username = StringVar()
username.trace('w', limitSize)
username_entry = Entry(username_frame, font=('Courier', 17, 'bold'), justify="center", textvariable=username)
password_frame = ttk.Labelframe(main_frame, labelanchor="nw", relief="groove", style = "Red.TLabelframe",
                                text="PASSWORD", height=80, width=450)
password = StringVar()
password.trace('w', limitSize)
password_entry = Entry(password_frame, font=('Courier', 17, 'bold'), show="*", justify="center", textvariable=password)


staff_label = Label(main_frame, text="STAFF", font=('Calibri', 26, 'bold'), justify="center", width=25,
                    fg=c4,background=c3)

#================================================TAB_2==================================================================

top_level2 = Frame(tab2, relief="ridge", background=c3)
top_level2.pack(expand=TRUE, fill="both")

bd1 = Label(top_level2, text="_______________________________________________________________",
            font=('calibri', 20, 'bold'),bg=c3,fg=c5)
bd2 = Label(top_level2, text="__________________________________________",
            font=('calibri', 20, 'bold'),bg=c3,fg=c5)
bd3 = Label(top_level2, text="_______________________________________________________________",
            font=('calibri', 20, 'bold'),bg=c3,fg=c5)
hd1 = Label(top_level2, text="YOUR INFORMATION", font=('Courier', 23, 'bold'),bg=c3,fg=c2)

bd1.place(x=40, y=30)
bd2.place(x=315, y=90)
bd3.place(x=40, y=380)
hd1.place(x=450, y=75)

logout_btn = Button(top_level2, text="LOGOUT", relief="groove", cursor="hand2", bd=2, font=f5, foreground=c3,
                   background=c2, width=15, command=logout)


list_btn = Button(top_level2, text="VACCINEE LIST", relief="groove", cursor="hand2", bd=2, font=f5, foreground=c3,
                   background=c2, width=20, command=select_tab4)

logout_btn.place(x=40, y=450)
list_btn.place(x=650, y=450)

menu2 = Frame(top_level2, background=c2, relief="groove", bd=2, width=1010, height=50)
menu2.place(x=-5)

#===================================================== INDIVIDUAL TAB ==================================================




top_level3 = Frame(tab3, relief="ridge", background=c3)
top_level3.pack(expand=TRUE, fill="both")

vax = Label(top_level3, image=vac_stat, bg=c3)
vax.place(x=165, y=290)

bd1 = Label(top_level3, text="____________________________________________________________________",
            font=('calibri', 18, 'bold'), bg=c3, fg=c5)
bd2 = Label(top_level3, text="_____________________________________________",
            font=('calibri', 18, 'bold'), bg=c3, fg=c5)
bd3 = Label(top_level3, text="_____________________________________________",
            font=('calibri', 18, 'normal'), bg=c3, fg=c5)

bd4 = Label(top_level3, text="____________________________________________________________________",
            font=('calibri', 18, 'bold'), bg=c3, fg=c5)
hd1 = Label(top_level3, text="PROFILE", font=('Courier', 18, 'bold'), bg=c3, fg=c2)

edit_profile = Button(top_level3, width=30, height=30, relief="flat", image=edit, bg=c3)

bd1.place(x=40, y=30)
bd2.place(x=315, y=70)
bd3.place(x=315, y=300)
bd4.place(x=40, y=380)
hd1.place(x=536, y=65)

edit_profile.place(x=800, y=61)

name_lbl = Label(top_level3, text="\tLast Name\t\t\tFirst Name\t\t\tMiddle Name", font=f6, bg=c3, fg=c4)
name_line = Label(top_level3, text="___________________________________________________________________________________________",
            font=f6, bg=c3, fg=c4)
add_line = Label(top_level3, text="Address: _________________________________________________  Contact No: ___________________",
             font=f6, bg=c3, fg=c4)
das_line = Label(top_level3, text="Date of Birth: __________________________  Age: _____________  Sex: _______________________",
            font=f6, bg=c3, fg=c4 )

name_lbl.place(x=360, y=167)
name_line.place(x=360, y=152)
add_line.place(x=361, y=205)
das_line.place(x=361, y=253)

menu2 = Frame(top_level3, background=c2, relief="groove", bd=2, width=1010, height=50)
menu2.place(x=-5)

style.configure('Tab3.TLabelframe.Label', font=('courier', 9, 'bold'))
style.configure('Tab3.TLabelframe',relief="raise")

view_btn_frame = ttk.Labelframe(top_level3, labelanchor="e", relief="groove", style = "Tab3.TLabelframe",
                                 height=40, width=180, text="VACCINATION HISTORY ")
add_btn_frame = ttk.Labelframe(top_level3, labelanchor="e", relief="groove", style = "Tab3.TLabelframe",
                                 height=40, width=155, text="NEW VACCINATION ")

view_rec_btn = Button(view_btn_frame, relief="flat", cursor="hand2",
                    width=30, height=30, command=select_tab8, image=view_rec)
add_rec_btn= Button(add_btn_frame, relief="flat", cursor="hand2",
                    width=30, height=30, command=select_tab7, image=add_rec)

add_rec_btn.place(x=0, y=-1)
view_btn_frame.place(x=630, y=350)
view_rec_btn.place(x=0, y=-1)


Lst_back_btn = Button(top_level3, text="RETURN", relief="groove", cursor="hand2", bd=2, font=f5, foreground=c3,
                      background=c2, width=50, command=select_tab4)
Guest_back_btn = Button(top_level3, text="RETURN", relief="groove", cursor="hand2", bd=2, font=f5, foreground=c3,
                        background=c2, width=50, command=select_tab5_n)

staff_back_btn = Button(top_level3, text="RETURN", relief="groove", cursor="hand2", bd=2, font=f5, foreground=c3,
                   background=c2, width=50, command=back_searching)


#===================================== INDIVIDUAL LIST=============================================================


top_level4 = Frame(tab4, relief="ridge", background=c1)
top_level4.pack(expand=TRUE, fill="both")

frame4 = Frame(top_level4, relief="raised",bd=5, background=c3, height=340, width=580)
frame4.place(x=160, y=100)

col_val = "Tracking_Code", "LastName", "Firstname", "Status"


tr_view = ttk.Treeview(frame4, columns=col_val, selectmode='extended', show='headings', height=22)
tr_view.place(height=210, width=550, y=50)
for each in col_val:
    tr_view.column(each, width=80, anchor='center')
    tr_view.heading(each, text=each.capitalize())

verscrlbar = ttk.Scrollbar(frame4, orient="vertical", command=tr_view.yview)
verscrlbar.place(x=550, y=50, height=210)
tr_view.configure(xscrollcommand=verscrlbar.set)

c = sql.connect("covid_vrs.db")
cursor = c.cursor()
cursor.execute("SELECT * FROM Individuals")

data = cursor.fetchall()
for d in data:
    tr_view.insert("", END, values=(d[0],d[1],d[2],d[9]))



back_btn2 = Button(frame4, text="BACK", relief="groove", cursor="hand2", bd=2, font=f7, foreground=c3,
                   background=c2, width=15, command=staff_page1)
add_btn = Button(frame4, text="ADD", relief="groove", cursor="hand2", bd=2, font=f7, foreground=c3,
                 background=c2, width=10, command=select_tab6)
view_btn = Button(frame4, text="VIEW", relief="groove", cursor="hand2", bd=2, font=f7, foreground=c3,
                  background=c2, width=10, command=selected)
delete_btn = Button(frame4, text="DELETE", relief="groove", cursor="hand2", bd=2, font=f7, foreground=c3,
                    background=c2, width=10, command=delete_records)

back_btn2.place(x=30, y=280)
add_btn.place(x=360, y=280)
view_btn.place(x=270, y=280)
delete_btn.place(x=450, y=280)

menu2 = Frame(frame4, background=c2, relief="groove", bd=2, width=570, height=50)
menu2.place(x=0)

ind_lbl = Label(menu2, text="INDIVIDUAL'S LIST", fg=c3, width=30, font=f9, bg=c2)
ind_lbl.place(x=105, y=5)

#=======================================================================================================================

top_level5 = Frame(tab5, relief="ridge", background=c1)
top_level5.pack(expand=TRUE, fill="both")

style.configure('tab5.TLabelframe.Label', font=('courier', 15, 'bold'))
style.configure('tab5.TLabelframe', background=c1)
style.configure('tab5.TLabelframe',relief="sunken")
style.configure('tab5.TLabelframe.Label', background=c1)
style.configure('tab5.TLabelframe.Label', foreground=c4)

code_frame = ttk.Labelframe(top_level5, labelanchor="n", relief="groove", style ="tab5.TLabelframe", text="ENTER YOUR TRACKING CODE",
                            height=80, width=450)

tracking_code = StringVar()
tracking_code.trace('w', limitSize)
code_entry = Entry(code_frame, font=('Courier', 17, 'bold'), justify="center", textvariable=tracking_code)

code_frame.place(x=223, y=200)
code_entry.place(relwidth=0.3, height=40, width=303, relx=0.01)
find_btn = Button(code_frame, width=35, height=33, relief="flat", cursor="hand2", bd=1, image=search, bg=c3, command=find)
find_btn.place(x=399, y=2)
menu = Frame(top_level5, background=c2, relief="groove", bd=2,width=1010, height=30)
menu.place(x=-5)

guest_btn3 = Button(top_level5, text="RETURN", relief="groove", cursor="hand2", bd=2, font=('Calibri', 17, 'bold'), foreground=c3,
                   background=c2, width=75, command=select_tab1)

staff_btn3 = Button(top_level5, text="RETURN", relief="groove", cursor="hand2", bd=2, font=('Calibri', 17, 'bold'), foreground=c3,
                   background=c2, width=75, command=staff_page1)

#=======================================================================================================================

top_level6 = Frame(tab6, relief="ridge", background=c3)
top_level6.pack(expand=TRUE, fill="both")

menu6 = Frame(top_level6, background=c2, relief="groove", bd=2, width=1010, height=80)
menu6.place(x=-5)

reg_title = Label(menu6, text="REGISTRATION FORM", width=34, justify='center', font=('Courier', 30, 'bold'), fg=c3, bg=c2).place(x=50, y=10)
tab6_line2 = Label(top_level6, text="_____________________________________________________", font=('Courier', 20, 'bold'), fg=c4, bg=c3)
tab6_line2.place(x=20, y=390)

name_lbl = Label(top_level6, text="\t    Last Name                   \t\tFirst Name\t\t\t\t Middle Name",
                 font=f2, fg=c4, bg=c3)
name_line = Label(top_level6, text="________________________________________________________________________________________________________________________",
                  font=f2, fg=c4, bg=c3)
address_line = Label(top_level6, text="Address: ______________________________________________________________________  Contact No: ___________________________",
                     font=f2, fg=c4, bg=c3)
dob_line = Label(top_level6, text="Date of Birth: _______________________________  Age: ______________________________  Sex: _______________________________",
                 font=f2, fg=c4, bg=c3)

name_line.place(x=21, y=170)
name_lbl.place(x=35, y=193)
address_line.place(x=21, y=250)
dob_line.place(x=21, y=330)

reg_lname = Entry(top_level6, font=f3, justify='center', width=29, fg=c4, bg=c3)
reg_lname.place(x=23, y=165)

reg_fname = Entry(top_level6, font=f3, justify='center', width=36, fg=c4, bg=c3)
reg_fname.place(x=288, y=165)

reg_mname = Entry(top_level6, font=f3, justify='center', width=29, fg=c4, bg=c3)
reg_mname.place(x=600, y=165)

reg_address = Entry(top_level6, font=f3, justify='center', width=54, fg=c4, bg=c3)
reg_address.place(x=87, y=246)

reg_con = Entry(top_level6, font=f3, justify='center', width=20, fg=c4, bg=c3)
reg_con.place(x=678, y=246)

reg_dob = DateEntry(top_level6, width=21, year=2022, month=5, day=7, date_pattern='mm/dd/y', justify='center', font=f3, borderwidth=2,
                    selectbackground='white',
                    selectforeground='red',
                    normalbackground='white',
                    normalforeground='black',
                    background='white',
                    foreground='black',
                    bordercolor='black',
                    othermonthforeground=c3,
                    othermonthbackground=c3,
                    othermonthweforeground=c3,
                    othermonthwebackground=c3,
                    weekendbackground='white',
                    weekendforeground='red',
                    headersbackground=c2,
                    headersforeground='black')
reg_dob.place(x=131, y=324)

reg_sex = StringVar()
sex_box= ttk.Combobox(top_level6, width=21, justify='center', font=f3, textvariable=reg_sex)
sex_box.place(x=656, y=324)
sex_box['values'] = ['Male', 'Female']
sex_box['state'] = 'readonly'

reg_age = StringVar()
age_ent = Entry(top_level6, font=f3, justify='center', width=20, textvariable=reg_age, fg=c4, bg=c3)
age_ent.place(x=408, y=326)

return_btn4 = Button(top_level6, text="RETURN", relief="groove", cursor="hand2", bd=2, font=('Calibri', 15, 'bold'), foreground=c3,
                   background=c2, width=15, command=tab6_return)
return_btn4.place(x=55, y=460)

next_btn = Button(top_level6, text="NEXT", relief="groove", cursor="hand2", bd=2, font=('Calibri', 15, 'bold'), foreground=c3,
                   background=c2, width=15, command=next)
next_btn.place(x=680, y=460)

#=======================================================================================================================

top_level7 = Frame(tab7, relief="ridge", background=c3)
top_level7.pack(expand=TRUE, fill="both")

c = sql.connect('covid_vrs.db')

vax = c.cursor()
vax.execute("SELECT VaccineBrand FROM Vaccines")
vaccines = vax.fetchall()

vaxr = c.cursor()
vaxr.execute("SELECT Name FROM Vaccinators")
vaccinators = vaxr.fetchall()

form1 = Frame(top_level7, bg=c5)
form1.place(height="184", width="714", x="93", y="146")

form1 = Frame(top_level7, bg=c3)
form1.place(height="180", width="710", x="95", y="148")

form = Frame(top_level7, bg=c4)
form.place(height="176", width="706", x="97", y="150")

new_vaccination = ttk.Labelframe(form, style = "Red.TLabelframe")

remarks = ttk.Combobox(new_vaccination, font=f3)
remarks.configure(justify="right")
remarks.place(anchor="nw", height="25", width="220", x="0", y="0")
remarks['values']=['First Dose', 'Second Dose', 'Booster 1', 'Booster 2']
remarks['state'] = 'readonly'

vaccine_id = ttk.Combobox(new_vaccination, font=f3)
vaccine_id.configure(justify="right")
vaccine_id.place(anchor="nw", height="25", width="220", x="220", y="0")
vaccine_id['values']=vaccines
vaccine_id['state'] = 'readonly'
vaccine_id.bind('<<ComboboxSelected>>', vaccine_change)

vaccinator_id = ttk.Combobox(new_vaccination, font=f3)
vaccinator_id.configure(justify="right")
vaccinator_id.place(anchor="nw", height="25", width="220", x="440", y="0")
vaccinator_id['values']=vaccinators
vaccinator_id['state'] = 'readonly'
vaccinator_id.bind('<<ComboboxSelected>>', vaccinator_change)

address = Entry(new_vaccination, font=f3)
address.configure(exportselection="false", justify="center")
address.place(anchor="nw", height="30", width="660", x="0", y="40")

label3 = Label(new_vaccination)
label3.configure(background=c3, font="{courier} 11 {bold}", relief="flat", text=" ADDRESS:")
label3.place(anchor="nw", height="25", relx="0.01", rely="0.03", x="0", y="40" )

remark_lbl = Label(new_vaccination)
remark_lbl.configure( background=c3, font="{Courier} 10 {bold}", relief="flat",state="normal")
remark_lbl.configure(text="REMARKS:")
remark_lbl.place(anchor="nw", relx="0.00", rely="0.02", x="1", y="0")

vaccine_id_lbl = Label(new_vaccination)
vaccine_id_lbl.configure(background=c3, font="{Courier} 10 {bold}", relief="flat", state="normal")
vaccine_id_lbl.configure(text="VACCINE ID:")
vaccine_id_lbl.place(anchor="nw", relx="0.33", rely="0.02", x="6", y="0")

vaccinator_id_lbl = Label(new_vaccination)
vaccinator_id_lbl.configure( background=c3, font="{Courier} 10 {bold}", relief="flat", state="normal")
vaccinator_id_lbl.configure(text="VACCINATOR ID:")
vaccinator_id_lbl.place(anchor="nw", relx="0.67", rely="0.02", x="1", y="0")

separator1 = ttk.Separator(new_vaccination)
separator1.configure(orient="horizontal")
separator1.place(anchor="nw", relx="0.0", rely="0.0", width="660", x="0", y="-7")

bbtn1 = Button(new_vaccination, bg=c2, fg=c3, font=f7, command=back_to_view)
bbtn1.configure(cursor="hand2", text="BACK")
bbtn1.place(anchor="nw", width="150", y="89")

bbtn2 = Button(new_vaccination, bg=c2, fg=c3, font=f7, command=add_vaxd)
bbtn2.configure(cursor="hand2", text="ADD")
bbtn2.place(anchor="nw", width="150", x="510", y="89")

separator2 = ttk.Separator(new_vaccination)
separator2.configure(orient="horizontal")
separator2.place( anchor="nw", relx="0.0", rely="0.68", width="660", x="0", y="0")

separator3 = ttk.Separator(new_vaccination)
separator3.configure(orient="horizontal")
separator3.place(anchor="nw", relx="0.0", rely="0.31", width="660", x="0", y="0")

new_vaccination.configure( height="0", labelanchor="n", padding="20", relief="groove")
new_vaccination.configure(text="NEW VACCINATION DETAILS")
new_vaccination.place( height="170", width="700", x="3", y="3")

#======================================================================================================================

trc = StringVar()


top_level8 = Frame(tab8, relief="ridge", background=c3)
top_level8.pack(expand=TRUE, fill="both")


tr_frame = ttk.Labelframe(top_level8, labelanchor="n", padding=10, relief="groove", text="VACCINATION HISTORY", style='Red.TLabelframe')
tr_frame.place(height=500, width=910, x=-5, y=20)

vax_back = Button(tr_frame, text="BACK", foreground="black", bg=c3, font=f1, cursor="hand2",
                  relief="flat", overrelief="flat", command=vaxd_back)
vax_back.place(rely="0.89", x=-10, height=62, width=900)

#=======================================================================================================================


top_level9 = Frame(tab9, relief="ridge", background=c3)
top_level9.pack(expand=TRUE, fill="both")

form3 = Frame(top_level9, bg=c5)
form3.place(height="184", width="714", x="93", y="146")
form3 = Frame(top_level9, bg=c3)
form3.place(height="180", width="710", x="95", y="148")
form2 = Frame(top_level9, bg=c4)
form2.place(height="176", width="706", x="97", y="150")
new_vaccination2 = ttk.Labelframe(form2, style ="Red.TLabelframe")
remarks2 = ttk.Combobox(new_vaccination2, font=f3)
remarks2.configure(justify="right")
remarks2.place(anchor="nw", height="25", width="220", x="0", y="0")
remarks2['values']=['First Dose']
remarks2['state'] = 'readonly'

vaccine_id2 = ttk.Combobox(new_vaccination2, font=f3)
vaccine_id2.configure(justify="right")
vaccine_id2.place(anchor="nw", height="25", width="220", x="220", y="0")
vaccine_id2['values']=vaccines
vaccine_id2['state'] = 'readonly'
vaccine_id2.bind('<<ComboboxSelected>>', vaccine_change2)

vaccinator_id2 = ttk.Combobox(new_vaccination2, font=f3)
vaccinator_id2.configure(justify="right")
vaccinator_id2.place(anchor="nw", height="25", width="220", x="440", y="0")
vaccinator_id2['values']=vaccinators
vaccinator_id2['state'] = 'readonly'
vaccinator_id2.bind('<<ComboboxSelected>>', vaccinator_change2)

address2 = Entry(new_vaccination2, font=f3)
address2.configure(exportselection="false", justify="center")
address2.place(anchor="nw", height="30", width="660", x="0", y="40")

label4 = Label(new_vaccination2)
label4.configure(background=c3, font="{courier} 11 {bold}", relief="flat", text=" ADDRESS:")
label4.place(anchor="nw", height="25", relx="0.01", rely="0.03", x="0", y="40")

remark_lbl2 = Label(new_vaccination2)
remark_lbl2.configure(background=c3, font="{Courier} 10 {bold}", relief="flat", state="normal")
remark_lbl2.configure(text="REMARKS:")
remark_lbl2.place(anchor="nw", relx="0.00", rely="0.02", x="1", y="0")

vaccine_id_lbl2 = Label(new_vaccination2)
vaccine_id_lbl2.configure(background=c3, font="{Courier} 10 {bold}", relief="flat", state="normal")
vaccine_id_lbl2.configure(text="VACCINE ID:")
vaccine_id_lbl2.place(anchor="nw", relx="0.33", rely="0.02", x="6", y="0")

vaccinator_id_lbl = Label(new_vaccination2)
vaccinator_id_lbl.configure( background=c3, font="{Courier} 10 {bold}", relief="flat", state="normal")
vaccinator_id_lbl.configure(text="VACCINATOR ID:")
vaccinator_id_lbl.place(anchor="nw", relx="0.67", rely="0.02", x="1", y="0")

separator6 = ttk.Separator(new_vaccination2)
separator6.configure(orient="horizontal")
separator6.place(anchor="nw", relx="0.0", rely="0.0", width="660", x="0", y="-7")

bbtn3 = Button(new_vaccination2, bg=c2, fg=c3, font=f7, command=add_vaxd2)
bbtn3.configure(cursor="hand2", text="REGISTER")
bbtn3.place(anchor="nw", width="150", x="510", y="89")

separator4 = ttk.Separator(new_vaccination2)
separator4.configure(orient="horizontal")
separator4.place(anchor="nw", relx="0.0", rely="0.68", width="660", x="0", y="0")

separator5 = ttk.Separator(new_vaccination2)
separator5.configure(orient="horizontal")
separator5.place(anchor="nw", relx="0.0", rely="0.31", width="660", x="0", y="0")

new_vaccination2.configure(height="0", labelanchor="n", padding="20", relief="groove")
new_vaccination2.configure(text="NEW VACCINATION DETAILS")
new_vaccination2.place(height="170", width="700", x="3", y="3")

#=======================================================================================================================
style.configure('Treeview.Heading', font=f8)
style.configure("Treeview", rowheight=40, font=f8)
#=======================================================================================================================


style.configure('ad.TLabelframe.Label', font=('courier', 10, 'bold'))
style.configure('ad.TLabelframe', background=c1)
style.configure('ad.TLabelframe',relief="sunken")
style.configure('ad.TLabelframe.Label', background=c1)
style.configure('ad.TLabelframe.Label', foreground=c4)


adminpage = Frame(tab10, relief="ridge", background=c1)
adminpage.pack(expand=TRUE, fill="both")

top1 = Frame(adminpage, relief="ridge", background=c1)

update_frame = ttk.Labelframe(top1, height=200, labelanchor="n", text="NEW USER", width=200, style="ad.TLabelframe")
update_frame.place(relheight=0.21, relwidth=0.94, relx=0.03, rely=0.74)

ln_e = Entry(update_frame, justify="right", font=f3)
ln_e.place( relheight=0.29,relwidth=0.3, relx=0.01 )

account_frame = ttk.Labelframe(update_frame, height=200, labelanchor="n",width=200, style="ad.TLabelframe")
account_frame.place(relheight=0.66, relwidth=0.98, relx=0.01, rely=0.29)

address_e = Entry(account_frame, font=f3, justify="right")
address_e.place( relheight=0.70, relwidth=0.42, relx=0.01, rely=0.07)

address_lbl = Label(account_frame, font=f8, text="ADDRESS:",bg=c3)
address_lbl.place( relwidth=0.1, relx=0.0, rely=0.15, x=10)

un_e = Entry(account_frame, font=f3, justify="right")
un_e.place(relheight=0.70, relwidth=0.27, relx=0.44, rely=0.07)

pass_e = Entry(account_frame, font=f3, justify="right")
pass_e.place(relheight=0.70, relwidth=0.27,  relx=0.72,rely=0.07)

un_lbl = Label(account_frame, font=f8, text="USERNAME:",bg=c3)
un_lbl.place(relwidth=0.1, relx=0.44, rely=0.15, x=3, y=0)

pass_lbl = Label(account_frame, font=f8, text="PASSWORD:",bg=c3)
pass_lbl.place( relwidth=0.13, relx=0.72, rely=0.15, x=3, y=0 )


ln_lbl = Label(update_frame, font="{courier} 11 {bold}", text="Lastname:",bg=c3)
ln_lbl.place(relwidth=0.1, relx=0.01, rely=0.03, x=3)

fn_e = Entry(update_frame, justify="right", font=f3)
fn_e.place( relheight=0.29,relwidth=0.3, relx=0.32)

fn_lbl = Label(update_frame, font="{courier} 11 {bold}", text="Firstname:",bg=c3)
fn_lbl.place(relwidth=0.12, relx=0.32, rely=0.03, x=3 )

age_e = Entry(update_frame, justify="right", font=f3)
age_e.place(relheight=0.29, relwidth=0.12, relx=0.63)

age_lbl = Label(update_frame, font="{courier} 11 {bold}", text="Age:",bg=c3)
age_lbl.place( relwidth=0.05, relx=0.63, rely=0.03, x=3, y=0)

sex_value = StringVar()
sex_c = ttk.Combobox(update_frame, justify="right", font=f3, textvariable=sex_value)
sex_c.place(relheight=0.29, relwidth=0.16, relx=0.76 )
sex_c['values'] = ['Male', 'Female']
sex_c['state'] = 'readonly'

sex_lbl = Label(update_frame, font="{courier} 11 {bold}", text="Sex:",bg=c3)
sex_lbl.place( relwidth=0.05, relx=0.76, rely=0.03, x=3)

add_b = Button(update_frame, text="ADD", font=f8, bg=c2, fg=c3, command=add_new_user)
add_b.place(relwidth=0.06, relx=0.92, rely=0.0, x=7)

large_frame = Frame(top1, height=200, relief="groove", bd=3, width=200)
large_frame.place(relheight=0.68, relwidth=0.94, relx=0.03, rely=0.04)

del_b = Button(large_frame, text="DELETE", font=f3, bg=c2, fg=c3, command=delete_user)
del_b.place( relwidth=0.12, relx=0.86, rely=0.65)


vaxr_b = Button(large_frame, text="VACCINATORS", font=f3, bg=c2, fg=c3, command=top3f)
vaxr_b.place(relwidth=0.12, relx=0.86, rely=0.30)

back_b = Button(large_frame, text="BACK", font=f3, bg=c2, fg=c3, command=homepage)
back_b.place( relwidth=0.12, relx=0.86, rely=0.82)

user_lbl = Label(large_frame,font="{courier} 24 {bold}", text="USERS")
user_lbl.place(relx=0.45, rely=0.04)

style.configure('users.Treeview.Heading', font=f10)
style.configure("users.Treeview", rowheight=50, font=f7)

col_val2 = "UserID", "Firstname","Lastname", "Sex", "Age", "Address", "Username", "Password"

user_tree = ttk.Treeview(top1, columns=col_val2, show='headings', style="users.Treeview", selectmode='extended')
user_tree.place( relheight=0.53, relwidth=0.757, relx=0.054, rely=0.16)

for each in col_val2:
    user_tree.column(each, width=80, anchor='center')
    user_tree.heading(each, text=each.capitalize())

sc_bar = ttk.Scrollbar(large_frame, orient="vertical" , command=user_tree.yview)
sc_bar.place( relheight=0.78, relx=0.829, rely=0.177, x=0, y=0)
user_tree.configure(xscrollcommand=sc_bar.set)

sep_1 = ttk.Separator(top1, orient="horizontal")
sep_1.place( relwidth=0.755, relx=0.06, rely=0.21, x=-5)

top3 = Frame(adminpage, relief="ridge", background=c1)

vaxrupdate_frame = ttk.Labelframe(top3, style='ad.TLabelframe')

vaxrn_e = Entry(vaxrupdate_frame, justify="center", font=f3)
vaxrn_e.place(relheight=0.29, relwidth=0.66, relx=0.01)

vaxrsmall_frame = ttk.Labelframe(vaxrupdate_frame)

vaxadd_e = Entry(vaxrsmall_frame, font=f3, justify="right")
vaxadd_e.place(relheight=0.70, relwidth=0.42, relx=0.01, rely=0.08)

vaxadd_lbl = Label(vaxrsmall_frame, font=f3, text="Address:",bg=c3)
vaxadd_lbl.place(relwidth=0.1, rely=0.16, x=10)

vaxem_e = Entry(vaxrsmall_frame, font=f3, justify="right")
vaxem_e.place(relheight=0.70, relwidth=0.27, relx=0.44, rely=0.08)

vaxcon_e = Entry(vaxrsmall_frame, font=f3, justify="right")
vaxcon_e.place(relheight=0.70, relwidth=0.27, relx=0.72, rely=0.08)

vaxem_lbl = Label(vaxrsmall_frame, font=f3, text="Email:",bg=c3)
vaxem_lbl.place(relwidth=0.07, relx=0.44, rely=0.16, x=3)

vaxcon_lbl = Label(vaxrsmall_frame, font=f3, text="Contact:",bg=c3)
vaxcon_lbl.place(relwidth=0.10, relx=0.72, rely=0.16, x=3)

vaxrsmall_frame.configure(labelanchor="n")
vaxrsmall_frame.place(relheight=0.66, relwidth=0.98, relx=0.01, rely=0.29)

vaxn_lbl = Label(vaxrupdate_frame, font=f3, text="Name:",bg=c3)
vaxn_lbl.place(relwidth=0.1, relx=0.01, rely=0.03, x=3)

vaxsex = StringVar()
vaxsex_c = ttk.Combobox(vaxrupdate_frame, justify="right", font=f3, textvariable=vaxsex)
vaxsex_c.place(relheight=0.29, relwidth=0.16, relx=0.69)
vaxsex_c['values'] = ['Male', 'Female']
vaxsex_c['state'] = 'readonly'

vaxsex_lbl = Label(vaxrupdate_frame, font=f3, text="Sex:",bg=c3)
vaxsex_lbl.place(relwidth=0.05, relx=0.69, rely=0.03, x=3)

vaxradd_b = Button(vaxrupdate_frame, text="ADD", font=f3, bg=c2, fg=c3, command=add_new_vaccinator)
vaxradd_b.place(relwidth=0.13, relx=0.85, x=7)

vaxrupdate_frame.configure(labelanchor="n", text="NEW VACCINATOR")
vaxrupdate_frame.place(relheight=0.21, relwidth=0.94, relx=0.03, rely=0.74)

vaxrlarge_frame = Frame(top3, relief="groove", bd=3)
vaxrlarge_frame.place(relheight=0.68, relwidth=0.94, relx=0.03, rely=0.04)

vax_b = Button(vaxrlarge_frame, text="VACCINES", font=f3, bg=c2, fg=c3, command=top2f)
vax_b.place(relwidth=0.12, relx=0.86, rely=0.30)

vaxrdel_b = Button(vaxrlarge_frame, text="DELETE", font=f3, bg=c2, fg=c3, command=delete_vaccinator)
vaxrdel_b.place(relwidth=0.12, relx=0.86, rely=0.65)

vaxrback_b = Button(vaxrlarge_frame, text="BACK", font=f3, bg=c2, fg=c3, command=top1f)
vaxrback_b.place(relwidth=0.12, relx=0.86, rely=0.82)

vaccinator_lbl = Label(vaxrlarge_frame, font="{courier} 24 {bold}", text="VACCINATORS")
vaccinator_lbl.place(relx=0.39, rely=0.03)

style.configure('users.Treeview.Heading', font=f10)
style.configure("users.Treeview", rowheight=50, font=f7)

col_val3 = "Vaccinator_id", "Name", "Sex", "Address", "Email", "Contact"

vaxr_tree = ttk.Treeview(top3, columns=col_val3, show='headings', style="users.Treeview", selectmode='extended')
vaxr_tree.place(relheight=0.53, relwidth=0.757, relx=0.054, rely=0.16)

for each in col_val3:
    vaxr_tree.column(each, width=80, anchor='center')
    vaxr_tree.heading(each, text=each.capitalize())

vaxr_sc_bar = ttk.Scrollbar(vaxrlarge_frame, cursor="hand2", orient="vertical", command=vaxr_tree.yview)
vaxr_sc_bar.place(relheight=0.78, relx=0.829, rely=0.177)
vaxr_tree.configure(xscrollcommand=vaxr_sc_bar.set)

sep_2 = ttk.Separator(top3, orient="horizontal")
sep_2.place(relwidth=0.755, relx=0.11, rely=0.21, x=-50)

top2 = Frame(adminpage, relief="ridge", background=c1)

vaxlarge_frame = Frame(top2, relief="groove", bd=3)
vaxlarge_frame.place(relheight=0.71,relwidth=0.28,relx=0.03, rely=0.04, x=310, y=20)

vaccines_lbl = Label(vaxlarge_frame, font="{courier} 15 {bold}", text="VACCINES")
vaccines_lbl.place(relx=0.3, rely=0.05, x=0, y=0)

vaxdelete_b = Button(vaxlarge_frame, text="DELETE", font=f3, bg=c2, fg=c3, command=delete_vaccines)
vaxdelete_b.place( relwidth=0.3,relx=0.62, rely=0.9)

vaxback_b = Button(vaxlarge_frame, text="BACK", font=f3, bg=c2, fg=c3, command=top3f)
vaxback_b.place( relwidth=0.3, relx=0.07, rely=0.9)

vaxadd_frame = ttk.Labelframe(top2, labelanchor="n", text="NEW VACCINE", style='ad.TLabelframe')
vaxadd_frame.place( relheight=0.21, relwidth=0.24, relx=0.05, rely=0.46, x=310, y=10)

vaxbrand_e = Entry(vaxadd_frame, justify="right", font=f3)
vaxbrand_e.place(relheight=0.29, relwidth=0.975, relx=0.01)

vaxsmall_frame = ttk.Labelframe(vaxadd_frame, labelanchor="n")
vaxsmall_frame.place(relheight=0.66, relwidth=0.98, relx=0.01, rely=0.29)

vaxadd_b = Button(vaxsmall_frame,text="ADD ", font=f3, bg=c2, fg=c3, command=add_new_vaccines )
vaxadd_b.place(relwidth=0.96, relx=0.02, rely=0.09)

vaxn_lbl = Label(vaxadd_frame, font=f3, text="Brand:", bg=c3)
vaxn_lbl.place(relwidth= 0.31,  relx=0.01, rely=0.02, x=3)

style.configure('vax.Treeview.Heading', font=f3)
style.configure("vax.Treeview", rowheight=40, font=f7)

col_val4 = "ID", "Brand"

vax_tree = ttk.Treeview(top2, columns=col_val4, show='headings', style="vax.Treeview", selectmode='extended')
vax_tree.place(relheight=0.3, relwidth=0.235, relx=0.054, rely=0.14, x=310, y=20)
vax_tree.column('ID', width=80, anchor='center', stretch='false')
vax_tree.column('Brand', width=80, anchor='center')

for each in col_val4:
    vax_tree.heading(each, text=each.capitalize())

vax_sc_bar = ttk.Scrollbar(vaxlarge_frame,cursor="hand2", orient="vertical", command=vax_tree.yview)
vax_sc_bar.place(relheight=0.44,relwidth=0.07, relx=0.93, rely=0.13)
vax_tree.configure(xscrollcommand=vax_sc_bar.set)

sep_1 = ttk.Separator(top2, orient="horizontal")
sep_1.place(relwidth=0.235, relx=0.06, rely=0.19, x=305, y=20)


w.mainloop()