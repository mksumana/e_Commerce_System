import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk

# Create database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ecom2',
            user='root',
            password='mysql'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Connection Error", f"Error: {e}")
        return None

def new_user(name, pno, email, address, password, connection):
    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True to return rows as dictionaries
        # Insert the new user
        query = "INSERT INTO users (name, pno, email, address, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name.upper(), pno, email, address, password))
        connection.commit()

        cursor.execute("SELECT * FROM users WHERE id = LAST_INSERT_ID()")
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            messagebox.showinfo("Success", f"Account created successfully!\nYour User ID is: {user['user_id']}")
            return user  
        else:
            messagebox.showerror("Error", "Failed to retrieve user details.")
            return None
    except Error as e:
        messagebox.showerror("Error", f"Failed to create account: {e}")
        return None


def user_login(user_id, password, connection):
    try:
        cursor = connection.cursor(dictionary=True)  # Fetching results as a dictionary
        query = "SELECT * FROM users WHERE user_id=%s AND password=%s"
        cursor.execute(query, (user_id, password))
        result = cursor.fetchone()
        cursor.close()
        if result:
            messagebox.showinfo("Success", f"Welcome {result['name']}!")
            return result  # Return the entire user data
        else:
            messagebox.showwarning("Error", "Invalid user ID or password.")
            return None
    except Error as e:
        messagebox.showerror("Error", f"Login failed: {e}")
        return None
    
# Main Application Window
root = tk.Tk()
root.title("ZapDeal")
root.geometry("1024x768")

connection = create_connection()

# Function to switch between pages
def show_frame(frame):
    frame.tkraise()

# Frames for each page (content area)
home_frame = tk.Frame(root)
profile_frame = tk.Frame(root)
cart_frame = tk.Frame(root)
wishlist_frame = tk.Frame(root)
login_frame = tk.Frame(root)
register_frame = tk.Frame(root)
product_frame=tk.Frame(root)

current_user_id = None

for frame in (home_frame, profile_frame, cart_frame, wishlist_frame, login_frame, register_frame,product_frame):
    frame.grid(row=1, column=0, sticky="nsew")  # Keep this consistent

# Function to switch to the home page
def go_home():
    show_frame(home_frame)
    
# Function to switch to the profile page
def go_profile():
    show_frame(profile_frame)
def go_cart ():
    show_frame(cart_frame)    
# Function to switch to the cart page
def go_cart():
    show_frame(cart_frame)
    if current_user_id is not None:
        load_cart_page(current_user_id, connection)
    else:
        messagebox.showerror("Error", "No user logged in.")


def go_wishlist():
    show_frame(wishlist_frame)

# Header Frame (hidden initially)
header_frame = tk.Frame(root, bg="purple", height=50)

# Show header after login or signup
def show_header():
    header_frame.grid(row=0, column=0, sticky="ew")  # Use grid instead of pack
    logo_button.grid(row=0, column=0, padx=10, sticky="w")
    search_entry.grid(row=0, column=1, padx=10, pady=10)
    profile_button.grid(row=0, column=2, padx=10, sticky="e")
    cart_button.grid(row=0, column=3, padx=10, sticky="e")
    wishlist_button.grid(row=0, column=4, padx=10, sticky="e")

# Modify the header widget placements accordingly
logo_button = tk.Button(header_frame, text="ZapDeal", font=("Arial", 18), bg="purple", fg="white", borderwidth=0, command=go_home)
search_entry = tk.Entry(header_frame, width=50, font=("Arial", 14))
profile_button = tk.Button(header_frame, text="Profile", font=("Arial", 12), bg="purple", fg="white", borderwidth=0, command=go_profile)
cart_button = tk.Button(header_frame, text="Cart", font=("Arial", 12), bg="purple", fg="white", borderwidth=0, command=go_cart)
wishlist_button = tk.Button(header_frame, text="Wishlist", font=("Arial", 12), bg="purple", fg="white", borderwidth=0, command=go_wishlist)



# Login Function
def login():
    user_id = login_user_id_entry.get()
    password = login_password_entry.get()
    user = user_login(user_id, password, connection)
    if user:
        show_header()
        load_profile_page(user) # Pass the user data to the profile page
        load_cart_page(user_id, connection)  
        show_frame(home_frame) 
    else:
        messagebox.showerror("Error", "Password does not match. Please try again.")
        return 


login_label = tk.Label(login_frame, text="Login", font=("Arial", 18))
login_label.pack(pady=10)
tk.Label(login_frame, text="User ID").pack(anchor="w", padx=20)
login_user_id_entry = tk.Entry(login_frame, width=30)
login_user_id_entry.pack(pady=5)
tk.Label(login_frame, text="Password").pack(anchor="w", padx=20)
login_password_entry = tk.Entry(login_frame, width=30, show="*")
login_password_entry.pack(pady=5)
login_button = tk.Button(login_frame, text="Login", command=lambda: login())
login_button.pack(pady=10)
register_link = tk.Button(login_frame, text="New User? Register Here", command=lambda: show_frame(register_frame))
register_link.pack()

# Register Frame
def register():
    name = reg_name_entry.get()
    pno = reg_pno_entry.get()
    email = reg_email_entry.get()
    address = reg_address_entry.get()

    while True:
        password = reg_password_entry.get()
        re_password = reg_repassword_entry.get()
        if password == re_password:
            break
        else:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
            return

    # Create a new user and get the full user record
    user = new_user(name, pno, email, address, password, connection)  
    if user:  
        show_header()
        load_profile_page(user)  # Pass the full user record to the profile page
        load_cart_page(user['id'], connection)  # Use user['id'] for the cart page
        show_frame(home_frame)
    else:
        messagebox.showerror("Error", "User registration failed.")

register_label = tk.Label(register_frame, text="Register", font=("Arial", 18))
register_label.pack(pady=10)
tk.Label(register_frame, text="Name").pack(anchor="w", padx=20)
reg_name_entry = tk.Entry(register_frame, width=30)
reg_name_entry.pack(pady=5)
tk.Label(register_frame, text="Contact Number").pack(anchor="w", padx=20)
reg_pno_entry = tk.Entry(register_frame, width=30)
reg_pno_entry.pack(pady=5)
tk.Label(register_frame, text="Email").pack(anchor="w", padx=20)
reg_email_entry = tk.Entry(register_frame, width=30)
reg_email_entry.pack(pady=5)
tk.Label(register_frame, text="Address").pack(anchor="w", padx=20)
reg_address_entry = tk.Entry(register_frame, width=30)
reg_address_entry.pack(pady=5)
tk.Label(register_frame, text="Password").pack(anchor="w", padx=20)
reg_password_entry = tk.Entry(register_frame, width=30, show="*")
reg_password_entry.pack(pady=5)
tk.Label(register_frame, text="Confirm Password").pack(anchor="w", padx=20)
reg_repassword_entry = tk.Entry(register_frame, width=30, show="*")
reg_repassword_entry.pack(pady=5)
register_button = tk.Button(register_frame, text="Register", command=register)
register_button.pack(pady=10)

# Sample Content for Profile, Cart, Wishlist, and Home Page
home_label = tk.Label(home_frame, text="Welcome to ZapDeal", font=("Arial", 24))
home_label.pack(pady=20)

profile_label = tk.Label(profile_frame, text="Profile Page", font=("Arial", 24))
profile_label.pack(pady=20)

cart_label = tk.Label(cart_frame, text="Cart", font=("Arial", 18))
cart_label.pack(anchor="w", padx=20, pady=10)

wishlist_label = tk.Label(wishlist_frame, text="Wishlist", font=("Arial", 18))
wishlist_label.pack(anchor="w", padx=20, pady=10)

# Function to fetch products from the database based on the category (optional)
def get_products_from_db(category=None):
    try:
        cursor = connection.cursor(dictionary=True)
        if category:
            query = "SELECT product_id ,name, price, img_link, category_id, category_name FROM product WHERE category_name LIKE %s"
            cursor.execute(query, ('%' + category + '%',))
        else:
            query = "SELECT product_id ,name, price, img_link, category_id, category_name FROM product"
            cursor.execute(query)
        
        products = cursor.fetchall()
        cursor.close()
        return products
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching products: {err}")
        return []

# Function to load the home page with products based on the category filter
def load_home_page(connection, user_id=None ,category=None):
    for widget in home_frame.winfo_children():
        widget.destroy()

    # Fetch products based on the selected category
    products = get_products_from_db(category)
    #print(products)
    # Create a scrollable canvas for product display
    canvas = tk.Canvas(home_frame, width=1024, height=700)
    scrollable_frame = tk.Frame(canvas)
    scrollbar = tk.Scrollbar(home_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Display each product in the catalog
    for index, product in enumerate(products):
        try:
            img = Image.open(product["img_link"])
            img = img.resize((150, 150))  # Resize image to fit
            img = ImageTk.PhotoImage(img)
        except Exception:
            img = None  # Handle cases where the image is not available

        # Create a frame for each product
        frame = tk.Frame(scrollable_frame, relief="ridge", borderwidth=2, padx=10, pady=10)
        frame.grid(row=index // 4, column=index % 4, padx=10, pady=10)

        # Display product image
        if img:
            img_label = tk.Label(frame, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack()

        # Display product name
        name_label = tk.Label(frame, text=product["name"], font=("Arial", 12, "bold"))
        name_label.pack()

        # Display product price
        price_label = tk.Label(frame, text=f"Rs. {product['price']}", font=("Arial", 10))
        price_label.pack()

        # Add "Add to Cart" button
        tk.Button(
            frame,
            text="Add to Cart",
            bg="green",
            fg="white",
            command=lambda p_id=product["product_id"]: add_to_cart(p_id, user_id, connection)
        ).pack(pady=5)

# Search function that filters products based on the category
def search():
    category = search_entry.get()  # Get the category entered by the user
    load_home_page(category)  # Load the home page with filtered products based on category

# Bind Enter key to trigger the search function
search_entry.bind("<Return>", lambda event: search())
load_home_page(connection=connection) # type: ignore

def load_profile_page(user):
    for widget in profile_frame.winfo_children():  
        widget.destroy()

    profile_label = tk.Label(profile_frame, text="Profile Page", font=("Arial", 24))
    profile_label.pack(pady=20)

    name_label = tk.Label(profile_frame, text=f"Name: {user['name']}", font=("Arial", 14))
    name_label.pack(anchor="w", padx=20, pady=5)

    pno_label = tk.Label(profile_frame, text=f"Phone Number: {user['pno']}", font=("Arial", 14))
    pno_label.pack(anchor="w", padx=20, pady=5)

    email_label = tk.Label(profile_frame, text=f"Email: {user['email']}", font=("Arial", 14))
    email_label.pack(anchor="w", padx=20, pady=5)

    address_label = tk.Label(profile_frame, text=f"Address: {user['address']}", font=("Arial", 14))
    address_label.pack(anchor="w", padx=20, pady=5)

    back_button = tk.Button(profile_frame, text="Back to Home", command=lambda: show_frame(home_frame))
    back_button.pack(pady=10)

def add_to_cart(product_id, user_id, connection):
    if connection is None:
        messagebox.showerror("Error", "Database connection is not established.")
        return
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        existing_item = cursor.fetchone()

        if existing_item:
            cursor.execute(
                "UPDATE cart SET quantity = quantity + 1 WHERE user_id = %s AND product_id = %s",
                (user_id, product_id),
            )
        else:
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, 1)",
                (user_id, product_id),
            )
        load_cart_page(user_id, connection=connection)
        connection.commit()
        messagebox.showinfo("Success", "Product added to cart!")
    except Error as e:
        messagebox.showerror("Error", f"Failed to add to cart: {e}")

def get_cart_items(user_id, connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT p.name, p.price, p.img_link, c.quantity
            FROM cart c
            JOIN product p ON c.product_id = p.product_id
            WHERE c.user_id = %s
        """
        cursor.execute(query, (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        return cart_items
    except Error as e:
        messagebox.showerror("Error", f"Failed to fetch cart items: {e}")
        return []

def load_cart_page(user_id, connection):
    # Clear the existing widgets
    for widget in cart_frame.winfo_children():
        widget.destroy()

    # Fetch the cart items
    cart_items = get_cart_items(user_id, connection)

    # Create a scrollable canvas for cart items
    canvas = tk.Canvas(cart_frame, width=1024, height=700)
    scrollable_frame = tk.Frame(canvas)
    scrollbar = tk.Scrollbar(cart_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Display each product in the cart
    for index, item in enumerate(cart_items):
        try:
            img = Image.open(item["img_link"])
            img = img.resize((150, 150))  # Resize to fit cart item
            img = ImageTk.PhotoImage(img)
        except Exception as e:
            img = None  # Handle missing or invalid images

        frame = tk.Frame(scrollable_frame, relief="ridge", borderwidth=2, padx=10, pady=10)
        frame.grid(row=index // 4, column=index % 4, padx=10, pady=10)  # Arrange in rows of 4

        if img:
            img_label = tk.Label(frame, image=img)
            img_label.image = img  # Keep a reference
            img_label.pack()

        name_label = tk.Label(frame, text=item["name"], font=("Arial", 12, "bold"))
        name_label.pack()

        price_label = tk.Label(frame, text=f"Rs. {item['price']}", font=("Arial", 10))
        price_label.pack()

        quantity_label = tk.Label(frame, text=f"Quantity: {item['quantity']}", font=("Arial", 10))
        quantity_label.pack()

        # Remove from Cart button
        tk.Button(frame, text="Remove from Cart", bg="red", fg="white", 
        command=lambda p_id=item['product_id']: remove_from_cart(p_id, user_id, connection)).pack(pady=5)

def remove_from_cart(product_id, user_id, connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        connection.commit()
        messagebox.showinfo("Success", "Product removed from cart!")
    except Error as e:
        messagebox.showerror("Error", f"Failed to remove from cart: {e}")



# Start with Login Frame and hide header
show_frame(login_frame)
root.mainloop()
