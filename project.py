import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error




# Main Application Window
root = tk.Tk()
root.title("ZapDeal")
root.geometry("1024x768")

# Function to switch between pages
def show_frame(frame):
    frame.tkraise()

# Frames for each page (content area)
home_frame = tk.Frame(root)
profile_frame = tk.Frame(root)
cart_frame = tk.Frame(root)
wishlist_frame = tk.Frame(root)
product_frame=tk.Frame(root)

for frame in (home_frame, profile_frame, cart_frame, wishlist_frame,product_frame):
    frame.grid(row=1, column=0, sticky="nsew")  # Place below header row

# Header Frame (constant across all pages)
header_frame = tk.Frame(root, bg="purple", height=50)
header_frame.grid(row=0, column=0)

# ZapDeal Button (Home)
def go_home():
    show_frame(home_frame)

logo_button = tk.Button(header_frame, text="ZapDeal", font=("Arial", 18), bg="purple", fg="white", borderwidth=0, command=go_home)
logo_button.pack(side="left", padx=10)

# Search Bar
search_entry = tk.Entry(header_frame, width=50, font=("Arial", 14))
search_entry.pack(side="left", padx=10, pady=10)

# Profile Button
def go_profile():
    show_frame(profile_frame)

profile_button = tk.Button(header_frame, text="Profile", font=("Arial", 12), bg="purple", fg="white", borderwidth=0, command=go_profile)
profile_button.pack(side="right", padx=10)

# Cart Button
def go_cart():
    show_frame(cart_frame)

cart_button = tk.Button(header_frame, text="Cart", font=("Arial", 12), bg="purple", fg="white", borderwidth=0, command=go_cart)
cart_button.pack(side="right", padx=10)

# Wishlist Button
def go_wishlist():
    show_frame(wishlist_frame)

wishlist_button = tk.Button(header_frame, text="Wishlist", font=("Arial", 12), bg="purple", fg="white", borderwidth=0, command=go_wishlist)
wishlist_button.pack(side="right", padx=10)

# Content for Wishlist Page
def remove_item():
    messagebox.showinfo("Info", "Item removed from Wishlist")

wishlist_label = tk.Label(wishlist_frame, text="MY WISHLIST", font=("Arial", 18))
wishlist_label.pack(anchor="w", padx=20, pady=10)

wishlist_products_frame = tk.Frame(wishlist_frame)
wishlist_products_frame.pack(pady=10, padx=20)

# Example Products in Wishlist
for i in range(3):
    product_frame = tk.Frame(wishlist_products_frame, bg="lightgray", height=100)
    product_frame.pack(fill="x", pady=5)

    # Product Image Placeholder
    image_label = tk.Label(product_frame, text="product", bg="gray", width=10, height=5)
    image_label.pack(side="left", padx=10, pady=10)

    # Product Details
    details_frame = tk.Frame(product_frame, bg="white")
    details_frame.pack(side="left", fill="both", expand=True, padx=10)

    product_name_label = tk.Label(details_frame, text="product name", font=("Arial", 14), anchor="w")
    product_name_label.pack(anchor="w")
    price_label = tk.Label(details_frame, text="price", font=("Arial", 12), anchor="w")
    price_label.pack(anchor="w")

    # Remove Button
    remove_button = tk.Button(product_frame, text="remove", bg="lightgray", command=remove_item)
    remove_button.pack(side="right", padx=10, pady=10)

# Content for Cart Page
cart_label = tk.Label(cart_frame, text="CART", font=("Arial", 18))
cart_label.pack(anchor="w", padx=20, pady=10)

cart_products_frame = tk.Frame(cart_frame)
cart_products_frame.pack(pady=10, padx=20)

# Example Products in Cart
for i in range(3):
    product_frame = tk.Frame(cart_products_frame, bg="lightgray", height=100)
    product_frame.pack(fill="x", pady=5)

    # Product Image Placeholder
    image_label = tk.Label(product_frame, text="product", bg="gray", width=10, height=5)
    image_label.pack(side="left", padx=10, pady=10)

    # Product Details with Description
    details_frame = tk.Frame(product_frame, bg="white")
    details_frame.pack(side="left", fill="both", expand=True, padx=10)

    product_name_label = tk.Label(details_frame, text="PRODUCT NAME/ DESC", font=("Arial", 14), anchor="w")
    product_name_label.pack(anchor="w")
    price_label = tk.Label(details_frame, text="PRICE", font=("Arial", 12), anchor="w")
    price_label.pack(anchor="w")

# Sample Content for Profile and Home Page
home_label = tk.Label(home_frame, text="Welcome to ZapDeal", font=("Arial", 24))
home_label.pack(pady=20)

profile_label = tk.Label(profile_frame, text="Profile Page", font=("Arial", 24))
profile_label.pack(pady=20)

# Start with Home Frame
show_frame(home_frame)

root.mainloop()
