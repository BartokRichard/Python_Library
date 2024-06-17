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

def handle_search(attribute, value, search_mode=None):
    attribute = clean_string(attribute)
    value = clean_string(value)

    found_books = []

    # Végigiterálunk az összes könyven
    for book in books_list:
        # Ellenőrizzük, hogy az aktuális könyv attribútuma megfelel-e az általunk kiválasztottnak
        if attribute == "title" and book.title == value:
            found_books.append(book)
        elif attribute == "author" and book.author == value:
            found_books.append(book)
        elif attribute == "category" and book.category == value:
            found_books.append(book)
        elif attribute == "price":
            try:
                if search_mode == "Lower" and book.price < float(value):
                    print(book.price, value)
                    found_books.append(book)
                elif search_mode == "Higher" and book.price > float(value):
                    found_books.append(book)
            except ValueError:
                pass
        elif attribute == "rate":
            try:
                if search_mode == "Lower" and book.rate < int(value):
                    found_books.append(book)
                elif search_mode == "Higher" and book.rate > int(value):
                    found_books.append(book)
            except ValueError:
                pass
        elif attribute == "number of pages":
            try:
                if search_mode == "Lower" and book.pages < int(value):
                    found_books.append(book)
                elif search_mode == "Higher" and book.pages > int(value):
                    found_books.append(book)
            except ValueError:
                pass
        elif attribute == "characters type" and value in book.characters:
            found_books.append(book)

    return format_book_info(found_books)

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
    return formatted_books