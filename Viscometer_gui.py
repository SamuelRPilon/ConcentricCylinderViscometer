import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports

def start_process():
    messagebox.showinfo("Message", "Process started")

def stop_process():
    messagebox.showinfo("Message", "Process stopped")

def validate_input(new_value):
    if new_value == "" or new_value.isdigit():
        if new_value == "" or (0 <= int(new_value) <= 30000):
            return True
    return False

def accept_input(event=None):
    value = input_text.get()
    if validate_input(value):
        current_speed_entry.config(state='normal')
        current_speed_entry.delete(0, tk.END)
        current_speed_entry.insert(0, value)
        current_speed_entry.config(state='readonly')
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid integer between 0 and 20000")

def calibrate_process():
    messagebox.showinfo("Message", "Calibration initiated")

def refresh_ports():
    ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in ports]
    port_dropdown['values'] = port_names

def on_select(event=None):
    selected_port = port_dropdown.get()
    print("Selected port:", selected_port)

def update_connection_indicator(status):
    if status:  # If connection is good
        connection_canvas.itemconfig(connection_circle, fill="green")
    else:
        connection_canvas.itemconfig(connection_circle, fill="red")

# Create main window
root = tk.Tk()
root.title("Viscometer Controller")

# Create frame for top left dropdown
dropdown_frame = tk.Frame(root)
dropdown_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

# Create dropdown for serial ports
port_label = tk.Label(dropdown_frame, text="Select Port:")
port_label.grid(row=0, column=0, sticky="w")
port_dropdown = ttk.Combobox(dropdown_frame, state="readonly", width=20)
port_dropdown.grid(row=0, column=1, padx=(0, 10), sticky="w")
port_dropdown.bind("<<ComboboxSelected>>", on_select)
refresh_button = ttk.Button(dropdown_frame, text="Refresh", command=refresh_ports)
refresh_button.grid(row=0, column=2, sticky="w")

# Create frame for connection indicator
connection_frame = tk.Frame(root)
connection_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")  # Adjusted row to 0 and column to 1 for top right corner

# Create canvas for circular indicator
connection_canvas = tk.Canvas(connection_frame, width=20, height=20, highlightthickness=0)
connection_canvas.grid(row=0, column=0, sticky="e", padx=(0, 5))

# Draw circular shape
connection_circle = connection_canvas.create_oval(2, 2, 18, 18, fill="white")

# Create frame for buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

# Create Start button
start_button = tk.Button(button_frame, text="Start", command=start_process, bg="green", fg="green", font=("Arial", 12, "bold"))
start_button.grid(row=0, column=0, padx=5, pady=10)
start_button.config(width=20, height=4)

# Create Stop button
stop_button = tk.Button(button_frame, text="Stop", command=stop_process, bg="red", fg="red", font=("Arial", 12, "bold"))
stop_button.grid(row=0, column=1, padx=5, pady=10)
stop_button.config(width=20, height=4)

# Create Calibrate button
calibrate_button = tk.Button(root, text="Calibrate", command=calibrate_process, bg="yellow", fg="yellow", font=("Arial", 12, "bold"))
calibrate_button.grid(row=7, column=0, padx=10, pady=10, sticky="w")  # Adjusted row to 7
calibrate_button.config(width=50, height=4)  # Increased width to 30

# Create label for the input text box
input_label = tk.Label(root, text="Input Speed Desired", font=("Arial", 12,"bold"))
input_label.grid(row=4, column=0, padx=10, pady=(10, 5), sticky="w")

# Create input text box
validate_cmd = root.register(validate_input)
input_text = tk.Entry(root, width=30, validate="key", validatecommand=(validate_cmd, '%P'))
input_text.grid(row=5, column=0, padx=10, pady=5, sticky="w")

# Create a frame for current speed label and entry
current_speed_frame = tk.Frame(root)
current_speed_frame.grid(row=6, column=0, padx=10, pady=5, sticky="w")

# Create title for current speed label
current_speed_title = tk.Label(current_speed_frame, text="Current Speed (RPM):", font=("Arial", 12, "bold"))
current_speed_title.grid(row=0, column=0, sticky='w')

# Create entry for displaying current speed
current_speed_entry = tk.Entry(current_speed_frame, width=30, state='readonly')
current_speed_entry.grid(row=0, column=1, sticky='w', padx=5)

# Bind Enter key to accept_input function
input_text.bind("<Return>", accept_input)

# Run the application
root.mainloop()
