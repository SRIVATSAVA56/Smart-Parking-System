import tkinter as tk
from tkinter import messagebox
import json
import time
from datetime import datetime
from collections import deque

# ---------------------------- Data Classes ----------------------------
class Vehicle:
    def __init__(self, vehicle_number):
        self.vehicle_number = vehicle_number
        self.entry_time = time.time()
        self.entry_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ParkingLot:
    def __init__(self, capacity=3):
        self.capacity = capacity
        self.stack = []
        self.waiting_queue = deque()
        self.removed = []

    def park_vehicle(self, vehicle):
        if any(v.vehicle_number == vehicle.vehicle_number for v in self.stack + list(self.waiting_queue)):
            return "Vehicle already exists!"

        if len(self.stack) < self.capacity:
            self.stack.append(vehicle)
            return f"{vehicle.vehicle_number} parked successfully."
        else:
            self.waiting_queue.append(vehicle)
            return f"Parking full. {vehicle.vehicle_number} added to waiting queue."

    def remove_vehicle(self, vehicle_number):
        temp = []
        found = False
        while self.stack:
            v = self.stack.pop()
            if v.vehicle_number == vehicle_number:
                duration = time.time() - v.entry_time
                self.removed.append((v.vehicle_number, duration))
                found = True
                break
            else:
                temp.append(v)
        while temp:
            self.stack.append(temp.pop())

        msg = ""
        if found:
            msg += f"{vehicle_number} removed. Duration: {duration:.2f}s\n"
            if self.waiting_queue:
                next_v = self.waiting_queue.popleft()
                self.stack.append(next_v)
                msg += f"{next_v.vehicle_number} moved from waiting queue to parking.\n"
        else:
            msg = f"{vehicle_number} not found in parking."
        return msg

    def get_status(self):
        return {
            "parked": self.stack,
            "waiting": list(self.waiting_queue),
            "removed": self.removed,
            "available_slots": self.capacity - len(self.stack)
        }

# ---------------------------- File I/O ----------------------------
USER_FILE = 'users.json'

def load_users():
    try:
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# ---------------------------- Shared Instance ----------------------------
parking_lot = ParkingLot()

# ---------------------------- User Interface ----------------------------
class UserGUI:
    def __init__(self, Title, window, username, vehicle_number, go_back):
        self.Title = "Smart Parking System"
        self.window = window
        self.username = username
        self.vehicle_number = vehicle_number
        self.go_back = go_back

        window.title("Smart Parking - User")
        window.geometry("800x600")

        frame = tk.Frame(window)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text=f"Welcome {username} | Car: {vehicle_number}", font=("Arial", 16)).pack(pady=10)

        tk.Button(frame, text="Book Slot", command=self.book_slot, width=25).pack(pady=5)
        tk.Button(frame, text="Remove Vehicle", command=self.remove_vehicle, width=25).pack(pady=5)
        tk.Button(frame, text="View Parking Status", command=self.show_status, width=25).pack(pady=5)
        tk.Button(frame, text="⬅️ Back to Login", command=self.back_to_login, width=25, bg="lightgray").pack(pady=5)

        self.output = tk.Text(frame, height=10, width=70)
        self.output.pack(pady=10)

    def book_slot(self):
        v = Vehicle(self.vehicle_number)
        msg = parking_lot.park_vehicle(v)
        self.output.insert(tk.END, msg + "\n")

    def remove_vehicle(self):
        msg = parking_lot.remove_vehicle(self.vehicle_number)
        self.output.insert(tk.END, msg + "\n")

    def show_status(self):
        status = parking_lot.get_status()
        self.output.insert(tk.END, f"\n--- Parking Lot Status ---\n")
        for v in status['parked']:
            self.output.insert(tk.END, f"Parked: {v.vehicle_number} at {v.entry_datetime}\n")
        self.output.insert(tk.END, f"Waiting: {[v.vehicle_number for v in status['waiting']]}\n")
        self.output.insert(tk.END, f"Available Slots: {status['available_slots']}\n")

    def back_to_login(self):
        self.window.destroy()
        self.go_back()

# ---------------------------- Admin Interface ----------------------------
class AdminGUI:
    def __init__(self, window, go_back):
        self.window = window
        self.go_back = go_back

        window.title("Admin Dashboard - Smart Parking")
        window.geometry("800x600")

        frame = tk.Frame(window)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="Admin Dashboard", font=("Arial", 18)).pack(pady=10)
        tk.Button(frame, text="Show All Parking Info", command=self.show_all_info, width=30).pack(pady=5)
        tk.Button(frame, text="Show Registered Users", command=self.show_users, width=30).pack(pady=5)
        tk.Button(frame, text="⬅️ Back to Login", command=self.back_to_login, width=30, bg="lightgray").pack(pady=5)

        self.output = tk.Text(frame, height=15, width=70)
        self.output.pack(pady=10)

    def show_all_info(self):
        status = parking_lot.get_status()
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "\n--- Admin Parking Report ---\n")
        for v in status['parked']:
            self.output.insert(tk.END, f"{v.vehicle_number} - Parked at {v.entry_datetime}\n")
        self.output.insert(tk.END, f"Waiting Queue: {[v.vehicle_number for v in status['waiting']]}\n")
        self.output.insert(tk.END, f"Removed Vehicles:\n")
        for v, dur in status['removed']:
            self.output.insert(tk.END, f"  {v} - {dur:.2f}s\n")
        self.output.insert(tk.END, f"Available Slots: {status['available_slots']}\n")

    def show_users(self):
        users = load_users()
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "\n--- Registered Users ---\n")
        for username, data in users.items():
            self.output.insert(tk.END, f"{username} | Password: {data['password']} | Car: {data['car_number']}\n")

    def back_to_login(self):
        self.window.destroy()
        self.go_back()

# ---------------------------- Login/Register Interface ----------------------------
class LoginRegisterGUI:
    def __init__(self, root):
        self.root = root
        self.users = load_users()

        root.title("Login / Register - Smart Parking")
        root.geometry("800x600")

        frame = tk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="Username").grid(row=0, column=0, pady=5)
        tk.Label(frame, text="Password").grid(row=1, column=0, pady=5)
        tk.Label(frame, text="Car Number (Users Only)").grid(row=2, column=0, pady=5)

        self.username_entry = tk.Entry(frame)
        self.password_entry = tk.Entry(frame, show="*")
        self.car_number_entry = tk.Entry(frame)

        self.username_entry.grid(row=0, column=1, pady=5)
        self.password_entry.grid(row=1, column=1, pady=5)
        self.car_number_entry.grid(row=2, column=1, pady=5)

        tk.Button(frame, text="Login", command=self.login, width=20).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Register (User)", command=self.register, width=20).grid(row=3, column=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin123":
            self.root.withdraw()
            new_window = tk.Toplevel()
            AdminGUI(new_window, self.restart_app)
        elif username in self.users and self.users[username]["password"] == password:
            car_no = self.users[username]["car_number"]
            self.root.withdraw()
            new_window = tk.Toplevel()
            UserGUI(new_window, username, car_no, self.restart_app)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        car_no = self.car_number_entry.get()

        if username in self.users:
            messagebox.showerror("Error", "User already exists.")
            return
        if not username or not password or not car_no:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.users[username] = {"password": password, "car_number": car_no}
        save_users(self.users)
        messagebox.showinfo("Success", "Registered successfully!")
        self.restart_app()

    def restart_app(self):
        self.root.deiconify()

# ---------------------------- Main Function ----------------------------
def main():
    root = tk.Tk()
    LoginRegisterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
