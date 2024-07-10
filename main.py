
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
from json import *

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 8)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_numbers + password_letters + password_symbols
    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def search(website):
    try:
        with open("password_details.json", mode='r') as password_file:
            data = load(password_file)
            found = False
            for key in data:
                if key == website or key == website.lower():
                    username = data[key]["username"]
                    password = data[key]["password"]
                    details = f"Username : {username}\nPassword  : {password}"
                    messagebox.showinfo(title="Website found", message=details)
                    pyperclip.copy(password)
                    found = True
            if not found:
                messagebox.showinfo(title="Not found", message="The given website not found!")

    except:
        messagebox.showinfo(title="Not found", message="The password file is empty!")


def save_details(*details_list):
    website = details_list[0]
    username = details_list[1]
    password = details_list[2]
    if website is not None and username is not None and password is not None:
        is_fine = messagebox.askyesno(title=website, message=f"Username : {username}\nPassword  : d{password}\n"
                                                             f"Are the details fine?")
        if is_fine:
            new_data = {
                website: {
                    "username": username,
                    "password": password}
            }
            try:
                with open("password_details.json", mode='r') as password_file:
                    existing_data = load(password_file)
                    existing_data.update(new_data)
                with open("password_details.json", mode='w') as password_file:
                    dump(existing_data, password_file, indent=4)
            except:
                with open("password_details.json", mode='w') as password_file:
                    dump(new_data, password_file, indent=4)
            finally:
                # deleting the entries
                website_input.delete(0, END)
                password_input.delete(0, END)
                website_input.focus_set()
    else:
        messagebox.showerror(title="Error", message="Please don't leave any fields empty!")


# ---------------------------- UI SETUP ------------------------------- #
screen = Tk()
screen.config(padx=50, pady=50, bg='yellow')
screen.title("Password Manager")

# creating canvas for image
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.pack()

# creating website, email/username, password labels
website_label = Label(text="Website:", font=("Arial", 12, "bold"))
username_label = Label(text="Email/username:", font=("Arial", 12, "bold"))
password_label = Label(text="Password:", font=("Arial", 12, "bold"))

# creating website, email/username, password entry boxes
website_input = Entry()
website_input.config(width=18)
website_input.focus_set()

username_input = Entry()
username_input.config(width=37)
username_input.insert(0, "pradhicksancm@gmail.com")

password_input = Entry()
password_input.config(width=18)

# creating generate password, add button and search button
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.config(width=15)
add_button = Button(text="Add Data", command=lambda: save_details(website_input.get(), username_input.get()
                                                                  , password_input.get()))
add_button.config(width=30)
search_button = Button(text="search", command=lambda: search(website_input.get()))
search_button.config(width=15)

# aligning all the components properly
canvas.grid(row=0, column=1)
website_label.grid(row=1, column=0)
username_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)
website_input.grid(row=1, column=1)
username_input.grid(row=2, column=1, columnspan=2)
password_input.grid(row=3, column=1)
generate_button.grid(row=3, column=2)
add_button.grid(row=4, column=1, columnspan=2)
search_button.grid(row=1, column=2)
mainloop()
