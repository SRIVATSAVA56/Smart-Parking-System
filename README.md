# 🚗 Smart Parking System Using Stacks and Queues

A GUI-based Smart Parking System developed using Python and Tkinter that efficiently manages vehicle parking using fundamental Data Structures like Stack (LIFO) and Queue (FIFO). The system provides real-time parking status, user authentication, and administrative control.

---

## 📌 Project Overview

Urban parking management faces challenges such as congestion, inefficient slot utilization, and lack of real-time tracking. This Smart Parking System solves these issues using structured data management and an intuitive graphical interface.

The system allows users to:

- Register and login
- Book parking slots
- Remove vehicles
- View parking status
- Manage waiting queues automatically

Admin users can monitor parking activity and registered users.

---

## 🧠 Data Structures Used

| Data Structure | Purpose |
|---------------|---------|
| Stack (LIFO) | Manages parking slots |
| Queue (FIFO) | Handles waiting vehicles |
| List | Stores removed vehicle records |
| JSON | Stores registered user data |

---

## 🖥️ Features

### 👤 User Features
- User registration and login
- Book parking slot
- Remove vehicle
- View real-time parking status
- Automatic waiting queue management

### 🛠️ Admin Features
- View all parked vehicles
- View waiting queue
- View removed vehicle history
- View registered users

### ⚙️ System Features
- GUI built using Tkinter
- Automatic queue-to-parking transfer
- Entry time tracking
- Vehicle duration calculation
- Error handling and validation

---

## 🏗️ System Architecture

Main Components:

- Vehicle Class – Stores vehicle information
- ParkingLot Class – Manages parking stack and queue
- UserGUI – User interface
- AdminGUI – Admin dashboard
- LoginRegisterGUI – Authentication system

---

## 📂 Project Structure

Smart-Parking-System/
│
├── smart_parking.py
├── users.json
├── README.md
├── LICENSE
└── .gitignore
