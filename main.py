import pickle
from book import Book

# Az összes könyv adatait tároló lista
books_list = []

def save_books():
    with open("books_data.pkl", "wb") as file:
        pickle.dump(books_list, file)

def load_books():
    try:
        with open("books_data.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# Betöltés az előző mentett adatokból (ha vannak)
books_list = load_books()

def clean_string(input_str):
    return input_str.lower()

def process_entry(title, author, category, price, rate, pages, characters):
    og_title = title
    title = clean_string(title)
    author = clean_string(author)
    category = clean_string(category)
    characters = [clean_string(char.strip()) for char in characters.split(',')] if characters else []

    try:
        price = float(price)
        if price <= 0:
            return "Price must be greater than 0."
    except ValueError:
        return "Price must be a number."

    try:
        rate = int(rate)
        if not (1 <= rate <= 10):
            return "Rate must be between 1 and 10."
    except ValueError:
        return "Rate must be a number between 1 and 10."
    
    try:
        pages = int(pages)
        if pages <= 0:
            return "Pages must be greater than 0."
    except ValueError:
        return "Pages must be a number."

    # A kép nevének beállítása a könyv címe alapján
    image_name = title.replace(" ", "_") + ".jpg"
    new_book = Book(title, author, category, price, rate, pages, characters, image_name)  # Image attribútum hozzáadása
    books_list.append(new_book)
    save_books()  
    print("Books list content after adding new book:")
    for book in books_list:
        print(book.title)
    return f"New book added: {og_title}"

def handle_search(search_attributes):
    # A teljes könyvlistából indulunk ki
    all_books = set(books_list)
    for attr_var, entry, mode_var in search_attributes:
        attribute = clean_string(attr_var.get())
        value = clean_string(entry.get())
        search_mode = mode_var.get() if attribute in ["price", "rate", "number of pages"] else None
        
        # Külön szűrjük minden egyes feltétel szerint a könyveket
        matching_books = set()
        for book in all_books:
            if attribute == "title" and book.title == value:
                matching_books.add(book)
            elif attribute == "author" and book.author == value:
                matching_books.add(book)
            elif attribute == "category" and book.category == value:
                matching_books.add(book)
            elif attribute == "price":
                try:
                    if search_mode == "Lower" and book.price < float(value):
                        matching_books.add(book)
                    elif search_mode == "Higher" and book.price > float(value):
                        matching_books.add(book)
                except ValueError:
                    pass
            elif attribute == "rate":
                try:
                    if search_mode == "Lower" and book.rate < int(value):
                        matching_books.add(book)
                    elif search_mode == "Higher" and book.rate > int(value):
                        matching_books.add(book)
                except ValueError:
                    pass
            elif attribute == "number of pages":
                try:
                    if search_mode == "Lower" and book.pages < int(value):
                        matching_books.add(book)
                    elif search_mode == "Higher" and book.pages > int(value):
                        matching_books.add(book)
                except ValueError:
                    pass
            elif attribute == "characters type" and value in book.characters:
                matching_books.add(book)
        
        # A metszet kiszámítása az eddigi és az aktuális szűrt könyvek között
        all_books = all_books & matching_books
    
    print('A kereses lefutott')
    return format_book_info(list(all_books))


def format_book_info(found_books):
    formatted_books = []
    for book in found_books:
        formatted_info = []
        formatted_info.append(f"Title: {book.title}")
        formatted_info.append(f"Author: {book.author}")
        formatted_info.append(f"Category: {book.category}")
        formatted_info.append(f"Price: {book.price}")
        formatted_info.append(f"Rate: {book.rate}")
        formatted_info.append(f"Pages: {book.pages}")
        formatted_info.append(f"Characters: {', '.join(book.characters)}")
        formatted_books.append((", ".join(formatted_info), book.image))
        
    print(f"Talált könyvek száma: {len(formatted_books)}")  
    return formatted_books