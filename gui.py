import os
from tkinter import *
from tkinter import messagebox
from ttkbootstrap import *
from PIL import Image, ImageTk
import main 

root = Window(themename="superhero")
root.title("Books")
root.geometry("550x690")

my_notebook = Notebook(root, bootstyle="dark")
my_notebook.pack(pady=20)

tab1 = Frame(my_notebook)
tab2 = Frame(my_notebook)

search_label = Label(tab1, text="Choose the attribute to search:")
search_label.pack(pady=10)

book_attributes = ["", "Title", "Author", "Category", "Price", "Rate", "Number of Pages", "Characters type"]

search_input_frame = Frame(tab1)
search_input_frame.pack(pady=10)

attributes_frame = Frame(tab1)
attributes_frame.pack(pady=10)


search_mode_label = Label(tab1, text="Choose search mode:")
search_mode_label.pack(pady=10)

search_mode_var = StringVar(search_input_frame)
search_mode_var.set("Lower") 

attribute_var = StringVar(search_input_frame)
attribute_var.set("Title")
attribute_dropdown = OptionMenu(search_input_frame, attribute_var, *book_attributes)
attribute_dropdown.pack(side=LEFT, padx=5, pady=5)

search_entry = Entry(search_input_frame)
search_entry.pack(side=LEFT, padx=5, pady=5)

def update_results(result_texts):
    results_canvas.delete("all")

    y_position = 10
    img_references = [] 
    for result, image_path in result_texts:
        formatted_result = result.replace(", ", "\n")

        try:
            img = Image.open(os.path.join("images", image_path))
        except FileNotFoundError:
            img = Image.open(os.path.join("images/defbookcover.jpg"))  
        img = img.resize((150, 200), Image.LANCZOS) 
        img = ImageTk.PhotoImage(img)
        results_canvas.create_image(10, y_position, anchor=NW, image=img)

        result_label = Label(results_canvas, text=formatted_result, wraplength=350, anchor="w", justify="left")
        result_label_window = results_canvas.create_window(170, y_position, anchor=NW, window=result_label)

        y_position += 220  

        img_references.append(img)

    results_canvas.img_references = img_references

    results_canvas.config(scrollregion=results_canvas.bbox("all"))

additional_attributes_frames = []

def update_attribute_search_mode(new_attribute_row, new_attribute_var, search_modes):
    # Létrehozzuk a keresési feltétel változót és legördülő menüt, de még nem jelenítjük meg
    new_search_mode_var = StringVar(new_attribute_row)
    new_search_mode_var.set(search_modes[0])  # Alapértelmezett érték
    new_search_mode_dropdown = OptionMenu(new_attribute_row, new_search_mode_var, *search_modes)
    
    # Ez a belső függvény frissíti a megjelenítést az attribútum változásakor
    def on_attribute_change(*args):
        if new_attribute_var.get() in ["Price", "Rate", "Number of Pages"]:
            new_search_mode_dropdown.pack(side=LEFT, padx=5, pady=5)
        else:
            new_search_mode_dropdown.pack_forget()
    
    # Követjük az attribútum változását
    new_attribute_var.trace('w', on_attribute_change)


search_attributes = []
def add_attribute_input():
    new_attribute_row = Frame(attributes_frame)
    new_attribute_row.pack(fill='x', pady=5)

    new_attribute_var = StringVar(new_attribute_row)
    new_attribute_var.set("Title")  # Alapértelmezett érték
    new_option_menu = OptionMenu(new_attribute_row, new_attribute_var, *book_attributes)
    new_option_menu.pack(side=LEFT, padx=5, pady=5)

    new_search_entry = Entry(new_attribute_row)
    new_search_entry.pack(side=LEFT, padx=5, pady=5)

    new_search_mode_var = StringVar(new_attribute_row)  # Itt hozzuk létre
    new_search_mode_var.set("Lower")  # Beállítjuk az alapértelmezett értéket "Lower"-re
    new_search_mode_dropdown = OptionMenu(new_attribute_row, new_search_mode_var, "Lower", "Higher")
    new_search_mode_dropdown.pack(side=LEFT, padx=5, pady=5)  # Most már megjelenítjük

    # Frissítjük az opciókat az új változóban
    new_search_mode_dropdown["menu"].add_command(label="Lower", command=lambda: new_search_mode_var.set("Lower"))

    # Figyeljük az attribútum változását és ennek megfelelően frissítjük a keresési módokat
    def on_attribute_change(*args):
        if new_attribute_var.get() in ["Price", "Rate", "Number of Pages"]:
            new_search_mode_dropdown.pack(side=LEFT, padx=5, pady=5)
        else:
            new_search_mode_dropdown.pack_forget()

    new_attribute_var.trace('w', on_attribute_change)
    on_attribute_change()  # Kezdeti állapot beállítása

    additional_attributes_frames.append(new_attribute_row)
    search_attributes.append((new_attribute_var, new_search_entry, new_search_mode_var))  # Hozzáadjuk a listához



# Ezzel a gomb megnyomására jelenik meg egy új input mező
add_atr_button = Button(tab1, text="Add Search Attribute", command=add_attribute_input)
add_atr_button.pack(pady=20)

def pack_search_mode():
    search_mode_label.pack_forget()
    search_mode_dropdown.pack_forget()
    search_mode_label.pack(side=LEFT, padx=5, pady=5)
    search_mode_dropdown.pack(side=LEFT, padx=5, pady=5)

def update_search_mode_options(*args):
    attribute = attribute_var.get()
    if attribute in ["Price", "Rate", "Number of Pages"]:
        search_mode_label.pack(pady=10)
        search_mode_dropdown.pack(side=LEFT, padx=5, pady=5)
    else:
        search_mode_label.pack_forget()
        search_mode_dropdown.pack_forget()

attribute_var.trace("w", update_search_mode_options)

search_mode_dropdown = OptionMenu(search_input_frame, search_mode_var, "Lower", "Higher")
search_mode_dropdown["menu"].add_command(label="Lower", command=lambda: search_mode_var.set("Lower"))

def search_books():
    search_progress_bar.start(10)

    results_canvas.delete("all")

    primary_search_attribute = (
        attribute_var,  
        search_entry, 
        search_mode_var 
    )

    all_search_attributes = [primary_search_attribute] + search_attributes

    search_result = main.handle_search(all_search_attributes)
    
    root.after(1500, lambda: update_results(search_result))

    root.after(1500, lambda: search_progress_bar.stop())
    root.after(1500, lambda: search_progress_bar.config(value=100))
    search_progress_bar['value'] = 100


search_button = Button(tab1, text="Search", bootstyle="primary outline", command=search_books)
search_button.pack(pady=5)

search_progress_bar = Progressbar(tab1, orient=HORIZONTAL, length=100, mode='determinate')
search_progress_bar.pack(pady=5) 

results_canvas = Canvas(tab1, width=400, height=600)
results_canvas.pack(pady=10, side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(tab1, orient=VERTICAL, command=results_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
results_canvas.config(yscrollcommand=scrollbar.set)

my_notebook.add(tab1, text="Search")

add_label = Label(tab2, text="Fill the fields to add:")
add_label.pack(pady=10)

title_label = Label(tab2, text="Title:")
title_label.pack()
title_entry = Entry(tab2, width=50)  
title_entry.pack(pady=5)

author_label = Label(tab2, text="Author:")
author_label.pack()
author_entry = Entry(tab2, width=50) 
author_entry.pack(pady=5)

category_label = Label(tab2, text="Category:")
category_label.pack()
category_entry = Entry(tab2, width=50) 
category_entry.pack(pady=5)

price_label = Label(tab2, text="Price:")
price_label.pack()
price_entry = Entry(tab2, width=50) 
price_entry.pack(pady=5)

rate_label = Label(tab2, text="Rate:")
rate_label.pack()
rate_entry = Entry(tab2, width=50) 
rate_entry.pack(pady=5)

pages_label = Label(tab2, text="Number of Pages:")
pages_label.pack()
pages_entry = Entry(tab2, width=50) 
pages_entry.pack(pady=5)

characters_label = Label(tab2, text="Characters type:")
characters_label.pack()
characters_entry = Entry(tab2, width=50)  
characters_entry.pack(pady=5)

def handle_result(result):
    if result.startswith("New book added"):
        progress_bar.start(10)
        root.after(1500, lambda: progress_bar.stop()) 
        root.after(1500, lambda: progress_bar.config(value=100))
        root.after(1500, lambda: messagebox.showinfo("Success", result))
    else:
        messagebox.showerror("Error", result)

add_button = Button(tab2, text="Add Book", bootstyle="success outline", command=lambda: handle_result(
    main.process_entry(title_entry.get(), author_entry.get(), category_entry.get(), price_entry.get(), rate_entry.get(), pages_entry.get(), characters_entry.get())))

add_button.pack(pady=10)

my_notebook.add(tab2, text="Add")

progress_bar = Progressbar(tab2, orient=HORIZONTAL, length=100, mode='determinate')
progress_bar.pack(pady=5) 

root.mainloop()