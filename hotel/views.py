from django.shortcuts import render, redirect
from hotel.models import read_csv, write_csv
from django.contrib import messages
import csv
from django.conf import settings
import pandas as pd


def login_view(request):
    return render(request, "hotel/login.html")  # Ensure this file exists

def register(request):
    return render(request, "hotel/register.html")  # Ensure this file exists

###############################
###############################
###############################
###############################
def home(request):
    # Read CSV file and convert it to a list of lists 
    df = pd.read_csv("csv_data/hotels.csv")  # Read CSV normally (keeps header)
    
    # Convert DataFrame to a list of lists (excluding header row)
    hotels = df.iloc[1:].values.tolist()  # Skip the first row

    return render(request, "hotel/home.html", {"hotels": hotels})

###############################
###############################
###############################
###############################
def read_register_csv():
    return read_csv("hotel_management/csv_data/users.csv")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = "user"

        # Read existing users to check for duplicates
        users = read_register_csv()

        # Check if the user already exists
        if any(user[0] == username for user in users):
            messages.error(request, "Username already taken!")
            return redirect("register")

        # Append new user data
        new_user = [username, email, password, role]
        write_csv("users.csv", new_user, headers=["Username", "Email", "Password", "Role"])

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")

    return render(request, "hotel/register.html")

###############################
###############################
###############################
###############################
def login_activity_read():
    """Reads user data from users.csv and returns a list of users."""
    users = []
    
    file_path = settings.BASE_DIR / "csv_data/users.csv"  # Using Django's BASE_DIR

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) >= 4:  # Ensure valid data
                    users.append([col.strip() for col in row])  # Strip spaces from values
        print("📂 Users loaded:", users)  # Debugging: print loaded users
    except FileNotFoundError:
        print(f"⚠ users.csv file not found at: {file_path}")  # Print exact path
    except Exception as e:
        print(f"⚠ Error reading users.csv: {e}")
    
    return users

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()

        users = login_activity_read()  # Use the new function

        if not users:
            print("⚠ No users found in users.csv")  # Debugging
            return render(request, "hotel/login.html", {"error": "No users registered."})

        print("🔍 Checking login credentials...")  # Debugging

        for user in users:
            print("Checking user:", user)  # Debugging

            if len(user) < 4:
                print("⚠ Skipping malformed row:", user)
                continue  

            csv_username, csv_email, csv_password, csv_role = [col.strip() for col in user]  # Strip spaces

            print(f"Comparing: {csv_username} (Role: {csv_role})")  # Debugging

            if csv_username == username and csv_password == password:
                request.session["username"] = username
                request.session["role"] = csv_role

                print(f"✅ Login successful: {username} ({csv_role})")  # Debug

                return redirect("admin_dashboard" if csv_role == "admin" else "user_dashboard")

        print("❌ Invalid credentials")
        return render(request, "hotel/login.html", {"error": "Invalid username or password."})

    return render(request, "hotel/login.html")

###############################
###############################
###############################
###############################

def read_room_data():
    file_path = settings.BASE_DIR / "csv_data/rooms.csv"
    try:
        df = pd.read_csv(file_path)

        if df.empty:
            print(f"⚠ Warning: {file_path} is empty!")
            return []

        return df.values.tolist()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return []
    
def read_hotel_data():
    file_path = settings.BASE_DIR / "csv_data/hotels.csv"
    try:
        df = pd.read_csv(file_path)

        if df.empty:
            print(f"⚠ Warning: {file_path} is empty!")
            return []

        return df.values.tolist()  # Convert DataFrame to list of lists
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return []
        
def admin_dashboard(request):
    if request.session.get("role") != "admin":
        return redirect("login")

    hotels = read_hotel_data()  # Read hotels
    rooms = read_room_data()  # Read rooms

    print("Hotels Data:", hotels)  # Debugging
    print("Rooms Data:", rooms)  # Debugging

    return render(request, "hotel/admin_dashboard.html", {"hotels": hotels, "rooms": rooms})

###############################
###############################
###############################
###############################
def add_hotel_in_csv(hotel_data):
    write_csv("hotels.csv", hotel_data, mode="a", headers=["Name", "Location"])

def add_hotel(request):
    if request.method == "POST":
        name = request.POST["name"].strip()
        location = request.POST["location"].strip()

        # Read existing hotels
        hotels = read_csv("hotels.csv")

        # Ensure CSV is not empty and does not contain invalid rows
        valid_hotels = [hotel for hotel in hotels if len(hotel) >= 2]

        # Check if the hotel already exists
        if any(hotel[0].strip().lower() == name.lower() and hotel[1].strip().lower() == location.lower() for hotel in valid_hotels):
            messages.error(request, "Hotel already exists.")
            return redirect("admin_dashboard")

        # Append new hotel using add_hotel_in_csv
        new_hotel = [name, location]
        add_hotel_in_csv(new_hotel)  # Append without overwriting

        messages.success(request, "Hotel added successfully!")

    return redirect("admin_dashboard")

###############################
###############################
###############################
###############################
def delete_hotel_in_csv(hotel_name):
    hotels = read_csv("hotels.csv")

    # Ensure only the specified hotel is removed, keeping everything else the same
    updated_hotels = [hotel for hotel in hotels if hotel and hotel[0].strip().lower() != hotel_name.strip().lower()]

    # Write back the updated list without modifying any other data
    write_csv("hotels.csv", updated_hotels, mode="w", headers=["Name", "Location"])

def delete_hotel(request, hotel_name):
    delete_hotel_in_csv(hotel_name)
    return redirect("admin_dashboard")

###############################
###############################
###############################
###############################

# def add_room_in_csv(room_data):
#     write_csv("rooms.csv", room_data, mode="a", headers=["Hotel Name", "Room Type", "Price"])

# def add_room(request):
#     if request.method == "POST":
#         hotel_name = request.POST["hotel_name"].strip()
#         room_type = request.POST["room_type"].strip()
#         price = request.POST["price"].strip()

#         # Append the new room without modifying existing data
#         new_room = [hotel_name, room_type, price]
#         add_room_in_csv(new_room)  # Appends instead of overwriting

#         messages.success(request, "Room added successfully!")

#     return redirect("admin_dashboard")



add_file_path = settings.BASE_DIR / "csv_data/rooms.csv"

def read_csv_custom():
    """Reads the CSV file and returns data excluding the header."""
    rows = []
    try:
        with open(add_file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            rows = [row for row in reader]
    except FileNotFoundError:
        pass  # If the file doesn't exist, return an empty list
    return rows

def add_room_in_csv(new_room):
    """Appends a new room row to the CSV file without modifying existing data."""
    with open(add_file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(new_room)

def add_room(request):
    if request.method == "POST":
        hotel_name = request.POST["hotel_name"].strip()
        room_type = request.POST["room_type"].strip()
        price = request.POST["price"].strip()

        # Append the new room without modifying existing data
        new_room = [hotel_name, room_type, price]
        add_room_in_csv(new_room)  # Appends instead of overwriting

        messages.success(request, "Room added successfully!")

    return redirect("admin_dashboard")

###############################
###############################
###############################
###############################

# def delete_room_in_csv(hotel_name, room_type):
#     rooms = read_csv("rooms.csv")

#     # Ensure only the specified room is removed, keeping everything else unchanged
#     updated_rooms = [room for room in rooms if room and 
#                      (room[0].strip().lower() != hotel_name.strip().lower() or 
#                       room[1].strip().lower() != room_type.strip().lower())]

#     # Write back the updated list without modifying any other data
#     write_csv("rooms.csv", updated_rooms, mode="w", headers=["Hotel Name", "Room Type", "Price"])

# def delete_room(request, hotel_name, room_type):
#     delete_room_in_csv(hotel_name, room_type)
#     return redirect("admin_dashboard")

dfile_path = settings.BASE_DIR / "csv_data/rooms.csv"

def delete_room_in_csv(hotel_name, room_type):
    """Deletes only the specified row from the CSV file without creating a temp file."""
    with open(dfile_path, mode="r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))  # Read all rows into memory

    # Filter out the row that matches hotel_name and room_type
    updated_rows = [row for row in rows if not (row and 
                      row[0].strip().lower() == hotel_name.strip().lower() and 
                      row[1].strip().lower() == room_type.strip().lower())]

    # Write back only the remaining rows (no temp file, modifying the file directly)
    with open(dfile_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

def delete_room(request, hotel_name, room_type):
    """Handles the deletion request and redirects to the admin dashboard."""
    delete_room_in_csv(hotel_name, room_type)
    return redirect("admin_dashboard")


###############################
###############################
###############################
###############################

def read_csv_rooms(filename):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data[1:]

def user_dashboard(request):
    username = request.session.get("username")

    # Use settings.BASE_DIR for the correct file path
    file_path = settings.BASE_DIR / "csv_data/rooms.csv"
    rooms = read_csv_rooms(file_path)

    bookings_file_path = settings.BASE_DIR / "csv_data/bookings.csv"
    bookings = [b for b in read_csv_rooms(bookings_file_path) if b[0] == username]

    # Debugging output
    print("All rooms loaded from CSV:")
    for room in rooms:
        print(room)  # Ensure all rooms are printed

    return render(request, "hotel/user_dashboard.html", {"rooms": rooms, "bookings": bookings})

###############################
###############################
###############################
###############################
def read_csv_book(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)


def append_csv_book(file_path, row):
    with open(file_path, "a", newline='', encoding='utf-8') as file:  # Open in append mode
        writer = csv.writer(file)
        writer.writerow(row)

def overwrite_csv_book(file_path, data):
    with open(file_path, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def book_room(request, hotel_name, room_type):
    username = request.session.get("username")
    bookings_file = settings.BASE_DIR / "csv_data/bookings.csv"

    append_csv_book(bookings_file, [username, hotel_name, room_type])  # Append new row

    return redirect("user_dashboard")


def cancel_booking(request, hotel_name, room_type):
    username = request.session.get("username")
    bookings_file = settings.BASE_DIR / "csv_data/bookings.csv"
    
    # Read the CSV and store the header
    with open(bookings_file, mode="r", newline="", encoding="utf-8") as file:
        reader = list(csv.reader(file))
        header, rows = reader[0], reader[1:]  # First row is the header, rest are data
    
    # Filter out the booking to be deleted
    updated_rows = [row for row in rows if not (row[0] == username and row[1] == hotel_name and row[2] == room_type)]
    
    # Write back only if there is a change
    if len(updated_rows) != len(rows):
        with open(bookings_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write header
            writer.writerows(updated_rows)  # Write remaining rows
    
    return redirect("user_dashboard")




###############################
###############################
###############################
###############################
# Logout
def logout_view(request):
    request.session.flush()
    return redirect("home")
