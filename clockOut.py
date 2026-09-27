from datetime import datetime
from tkinter import *
from tkinter import ttk
import sqlite3

connection = sqlite3.connect("User.db")
cursor = connection.cursor()
many_workers = [ ('Lebron James', 1234, ' ', ' ',' '),
                 ('Kobe Bryant', 4147, ' ', ' ',' '),
                 ('Steff Curry', 3146, ' ', ' ',' '),
                 ('Micheal Jordan', 2424, ' ', ' ',' ')
                ]

#cursor.execute("""CREATE TABLE workers (
#        username text,
#        password text,
#        timeIn text,
#        timeOut text,
#        hoursworked integer
#    )""")

#cursor.executemany("INSERT INTO workers VALUES (?,?,?,?,?)", many_workers)

cursor.execute("SELECT * FROM workers")
allRows = cursor.fetchall()
Users = [row[0] for row in allRows]
Passwords = [row[1] for row in allRows]
timeIn = [row[2]for row in allRows]
timeOut = [row[3]for row in allRows]
hoursWorked = [row[4] for row in allRows]
connection.commit()

SignInWindow = Tk()                #creates signin window
SignInWindow.geometry("1200x1000")
SignInWindow.title("Sign In")

ClockWindow = Toplevel(SignInWindow) #creates new window above the SignIn Window
ClockWindow.geometry("1200x1000")
ClockWindow.title("ClockIn")
ClockWindow.withdraw()

AdminWin = Toplevel(SignInWindow) #creates new window above the SignIn Window
AdminWin.geometry("1200x1000")
AdminWin.title("Admin")
AdminWin.withdraw()

CenterFrame0 = Frame(SignInWindow)  #creates a frame to center widgets on Signinwindow
CenterFrame0.pack(expand=True)

CenterFrame1 = Frame(ClockWindow)  #creates a frame to center widgets on ClockWindow
CenterFrame1.pack(expand=True)

CenterFrame2 = Frame(AdminWin)  #creates a frame to center widgets on AdminWin
CenterFrame2.pack(expand=True)

index = 0

Error = Label(CenterFrame0,         #creates a label that says "Enter a Valid Username and Password"
              fg = "#FF0000",
              text = "Enter a Valid Username and Password")

Error2 = Label(CenterFrame1,         #creates a label that says "Enter a Valid Username and Password"
              fg = "#FF0000",
              text = "You already clocked in today")

Error3 = Label(CenterFrame1,         #creates a label that says "Enter a Valid Username and Password"
              fg = "#FF0000",
              text = "You either didnt clock in or already clocked out")

Correct = Label(CenterFrame1,         #creates a label that says "Enter a Valid Username and Password"
              fg = "#00FF00",
              text = "You are clocked in :)")
Correct1 = Label(CenterFrame1,         #creates a label that says "Enter a Valid Username and Password"
              fg = "#00FF00",
              text = "Enjoy the rest of your day :)")

def update():
    now = datetime.now()
    currentTime = now.strftime("%I:%M %p")
    Time.config(text = "It is " + currentTime)
    Time.after(1000,update)

def CheckUser():
    tValue = False
    global index
    index = 0
    for i in Users:
        if i == UserEntry.get():
            if Passwords[index] == PasswordEntry.get():
                tValue = True
                return tValue
                break
        index += 1

def SignInCheck():
    if UserEntry.get() == "ADMIN" and PasswordEntry.get() == "ADMIN228928834":
        Error.pack_forget()
        SignInWindow.withdraw()
        AdminWin.deiconify()
    elif CheckUser():  #temporary (When finished will check database for Correct UserName and Password)
        Error.pack_forget()
        Correct.pack_forget()
        Correct1.pack_forget()
        SignInWindow.withdraw()
        ClockWindow.deiconify()
        YourName.config(text="Hello "+ UserEntry.get())
        UserEntry.delete(0,END)
        PasswordEntry.delete(0,END)
    else:
        Error.pack(pady=10)

def ClockIn():
    if timeIn[index]!= ' ':
        Error2.pack(pady=10)
    else:
        Correct.pack()
        now = datetime.now()
        ClockInTime = now.strftime("%I:%M %p")
        cursor.execute("""UPDATE workers SET timeIn = ?
                        WHERE rowid = ? """, (ClockInTime, index + 1))
        connection.commit()
        timeIn[index] = ClockInTime
    Error3.pack_forget()
    #print(timeIn[index])

def ClockOut():
    if timeIn[index] == ' ':
        Error3.config(text="You have to clock in first")
        Error3.pack(pady=10)
        return

    if hoursWorked[index] != ' ':
        Error3.config(text="You already clocked out today")
        Error3.pack(pady=10)
    else:
        Correct1.pack()
        now = datetime.now()
        ClockOutTime = now.strftime("%I:%M %p")

        intTimeOut = datetime.strptime(ClockOutTime,"%I:%M %p")
        intTimeIn = datetime.strptime(timeIn[index],"%I:%M %p")

        diff = intTimeOut - intTimeIn

        timeWorked = diff.total_seconds() / 3600
        cursor.execute("""UPDATE workers SET timeOut = ?
                        WHERE rowid = ? """, (ClockOutTime, index + 1))
        cursor.execute("""UPDATE workers SET hoursWorked = ?
                        WHERE rowid = ? """, (timeWorked, index + 1))
        connection.commit()
    Error2.pack_forget()
    #print(hoursWorked[index])

def Return():
    ClockWindow.withdraw()
    AdminWin.withdraw()
    SignInWindow.deiconify()
    UserEntry.delete(0,END)
    PasswordEntry.delete(0,END)
    Error2.pack_forget()
    Error3.pack_forget()
    TableRefresh()

def TableRefresh():
    for item in WorkerTable.get_children():
        WorkerTable.delete(item)
    cursor.execute("SELECT * FROM workers")
    fresh_rows = cursor.fetchall()
    for i, row in enumerate(fresh_rows):
        WorkerTable.insert(parent="", index="end", values=row)


UserEntry = Entry(CenterFrame0,     #creates Username entrybox
                 font = ("Arial",20),
                 fg = "#000000",
                 bg = "#AAAAAA",
                 )

UserEntry.pack(pady = 10)

PasswordEntry = Entry(CenterFrame0,  #creates password entrybox
                      font = ("Arial",20),
                      fg = "#000000",
                      bg = "#AAAAAA",
                      )

PasswordEntry.pack(pady=10)

SignInButton = Button(CenterFrame0,
                      text = "Sign In",
                      font = ("Arial", 20),
                      fg = "#000000",
                      bg = "#FFFFFF",
                      command = SignInCheck)
SignInButton.pack(pady=10)

YourName = Label(CenterFrame1,
                 text = ("Hello"),
                 font = ("Arial",30),
                 fg = "#FFFFFF")
YourName.pack()

Time = Label(CenterFrame1,
            font =("Arial",30),
            fg = "#FFFFFF")
Time.pack(pady = 30)

update()

Clock_In = Button(CenterFrame1,
                 text = "Clock In",
                 font=("Arial",20),
                 fg = "#FFFFFF",
                 command = ClockIn)

Clock_In.pack()

Clock_Out = Button(CenterFrame1,
                 text = "Clock Out",
                 font=("Arial",20),
                 fg = "#000000",
                 bg = "#FF0000",
                 command = ClockOut)
Clock_Out.pack()

Return_Btn = Button(CenterFrame1,
                text = "return",
                font=("Arial",20),
                fg = "#000000",
                command = Return)
Return_Btn.pack()

Return_Btn = Button(CenterFrame2,
                text = "return",
                font=("Arial",20),
                fg = "#000000",
                command = Return)
Return_Btn.pack()

WorkerTable = ttk.Treeview(CenterFrame2,columns=("Username", "Password", "TimeIn", "TimeOut", "HoursWorked"))

WorkerTable.pack(fill="both", expand=True)

WorkerTable.column("#0", width=0, stretch=NO)
WorkerTable.column("Username", anchor=W, width=180)
WorkerTable.column("Password", anchor=W, width=120)
WorkerTable.column("TimeIn", anchor=CENTER, width=120)
WorkerTable.column("TimeOut", anchor=CENTER, width=120)
WorkerTable.column("HoursWorked", anchor=CENTER, width=120)

WorkerTable.heading("Username", text="Username", anchor=W)
WorkerTable.heading("Password", text="Password", anchor=W)
WorkerTable.heading("TimeIn", text="Time In", anchor=CENTER)
WorkerTable.heading("TimeOut", text="Time Out", anchor=CENTER)
WorkerTable.heading("HoursWorked", text="Hours Worked", anchor=CENTER)

for i, row in enumerate(allRows):
    WorkerTable.insert(parent="", index="end",values=row)

SignInWindow.mainloop()
