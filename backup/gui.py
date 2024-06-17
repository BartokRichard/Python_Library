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

search_mode_label = Label(tab1, text="Choose search mode:")
search_mode_label.pack(pady=10)

search_mode_var = StringVar(search_input_frame)
search_mode_var.set("Lower")  # Alapértelmezett érték beállítása

attribute_var = StringVar(search_input_frame)
attribute_var.set("Title")  # Alapértelmezett érték beállítása a "Title"-re
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

        y_position += 220  # Image height + padding

        img_references.append(img)

    # Store the image references to prevent garbage collection
    results_canvas.img_references = img_references

    # Resize the canvas to fit the new content
    results_canvas.config(scrollregion=results_canvas.bbox("all"))


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
# search_mode_dropdown["menu"].add_command(label="Higher", command=lambda: search_mode_var.set("Higher"))

def search_books():
    search_progress_bar.start(10)
    search_result = main.handle_search(attribute_var.get(), search_entry.get(), search_mode_var.get() if attribute_var.get() in ["Price", "Rate", "Number of Pages"] else None)
    root.after(1500, lambda: search_progress_bar.stop())
    root.after(1500, lambda: search_progress_bar.config(value=100))
    search_progress_bar['value'] = 100
    root.after(1500, lambda: update_results(search_result))

search_button = Button(tab1, text="Search", bootstyle="primary outline", command=search_books)
search_button.pack(pady=5)

search_progress_bar = Progressbar(tab1, orient=HORIZONTAL, length=100, mode='determinate')
search_progress_bar.pack(pady=5) 

# A képek és az azok melletti szövegek megjelenítéséhez egy Canvas-t használunk
# A képek és az azok melletti szövegek megjelenítéséhez egy Canvas-t használunk
results_canvas = Canvas(tab1, width=400, height=600)
results_canvas.pack(pady=10, side=LEFT, fill=BOTH, expand=True)

# A scrollbar hozzáadása a Canvas-hoz
scrollbar = Scrollbar(tab1, orient=VERTICAL, command=results_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# A scrollbar beállítása a Canvas-hoz
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
progress_bar.pack(pady=5)  # A progress bar nem jelenik meg alapértelmezetten

root.mainloop()