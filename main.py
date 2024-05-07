import sqlite3
import tkinter
from tkinter import *
from PIL import Image, ImageTk

def concert(window2, c, name, age, phone):
    global photo
    conn = sqlite3.connect('concert_ticket_system.db')
    cursor = conn.cursor()
    customer_id = f"C{phone[::-1]}"

    sql1 = "INSERT INTO customer(customer_id,name,phone,age) VALUES(?,?,?,?)"
    sql2 = "INSERT INTO ticket(concert_id,customer_id) VALUES(?,?)"

    customer = (customer_id,name,phone,age)
    ticket = (c[0],customer_id)
    try:
        cursor.execute(sql1,customer)
    except sqlite3.IntegrityError:
        print("")
    cursor.execute(sql2, ticket)

    conn.commit()
    conn.close()

    window3 = Toplevel(window2)
    window3.minsize(width=960, height=400)
    window3.title("TICKET")

    image_file = "Images/ticket.png"
    img = Image.open(image_file)
    img = img.resize((960, 400))
    photo = ImageTk.PhotoImage(img)

    canvas = Canvas(window3,bg='black')
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.create_text(585, 235, text=c[5], fill="white", font=('Broadway', 20, 'bold'))
    canvas.create_text(585, 320, text=f"{c[6]}₺",fill="white", font=('Broadway', 20, 'bold'))
    canvas.create_text(815, 235, text=c[4], fill="white", font=('Broadway', 20, 'bold'))
    canvas.create_text(820, 315, text=f"{c[1]}\n({c[2]})", fill="white", font=('Broadway', 15, 'bold'))
    canvas.pack(fill="both", expand=True)

def ok(name,age,phone):
    conn = sqlite3.connect('concert_ticket_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM concert WHERE age_rating <= ?",(age_entry.get(),))
    concerts = cursor.fetchall()
    conn.commit()
    conn.close()
    window2 = tkinter.Toplevel(window)
    window2.minsize(width=200, height=300)
    window2.title("CONCERTS")
    d=len(concerts)/2
    for y in range(int(len(concerts)/d)):
        for x in range(y*int(d),int(d)*(y+1)):
            image_file = f"Images/{concerts[x][1]}.png"

            img = Image.open(image_file)
            img = img.resize((200, 350))
            photo = ImageTk.PhotoImage(img)

            image_label1 = Label(window2, image=photo, width=200, height=350)
            image_label1.image = photo
            image_label1.grid(row=3*y+1, column=concerts.index(concerts[x])%int(d))

            time_label = Label(window2,text=f"{concerts[x][4]} | {concerts[x][5]}\n {concerts[x][6]}₺")
            time_label.grid(row=3*y+2, column=concerts.index(concerts[x])%int(d))

            concert_button = Button(window2, text=concerts[x][1], command=lambda x=x :concert(window2,concerts[x],name,age,phone))
            concert_button.grid(row=3*y+3, column=concerts.index(concerts[x])%int(d))

window = Tk()
window.minsize(width=350, height=400)
window.title("CONCERT TICKET SYSTEM")

image1 = PhotoImage(file="Images/concert3.png")
image_label = Label(window, image=image1, width=250, height=200)

name_label = Label(text="Name and Surname")
name_entry = Entry(width=25)

age_label = Label(text="Age")
age_entry = Entry(width=25)

phone_label = Label(text="Phone Number")
phone_entry = Entry(width=25)

image_label.pack()

name_label.pack()
name_entry.pack()

age_label.pack()
age_entry.pack()

phone_label.pack()
phone_entry.pack()

ok_button = Button(window, text="OK", command=lambda :ok(name_entry.get(),age_entry.get(),phone_entry.get()))
ok_button.pack()

window.mainloop()






