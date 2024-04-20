import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports
import serial
import threading

class ViscometerController:
    def __init__(self, root):
        self.root = root
        self.ser = None  # Global variable to hold the serial connection
        self.current_speed = None  # Variable to hold the current speed
        self.current_command = None  # Variable to hold the current command
        self.speed_to_command = {
            5000: 5,
            10000: 6,
            15000: 7,
            17000: 8,
            20000: 9
        }

        # Set the geometry of the root window
        self.root.geometry("1100x700")

        # Create main window
        self.root.title("Viscometer Controller")

        # Create frame for top left dropdown
        self.dropdown_frame = tk.Frame(root)
        self.dropdown_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # Create dropdown for serial ports
        self.port_label = tk.Label(self.dropdown_frame, text="Select Port:")
        self.port_label.grid(row=0, column=0, sticky="w")
        self.port_dropdown = ttk.Combobox(self.dropdown_frame, state="readonly", width=30)
        self.port_dropdown.grid(row=0, column=1, padx=(0, 20), sticky="w")
        self.port_dropdown.bind("<<ComboboxSelected>>", self.on_select)
        self.refresh_button = ttk.Button(self.dropdown_frame, text="Refresh", command=self.refresh_ports)
        self.refresh_button.grid(row=0, column=2, sticky="w")

        # Create frame for buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Create Start button
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_process, bg="green", fg="white", font=("Arial", 18, "bold"))
        self.start_button.grid(row=0, column=0, padx=10, pady=20)
        # Initially disable the Start button
        self.start_button.config(state='disabled')
        self.start_button.config(width=40, height=8)

        # Create Stop button
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_process, bg="red", fg="white", font=("Arial", 18, "bold"))
        self.stop_button.grid(row=0, column=1, padx=10, pady=20)
        self.stop_button.config(width=40, height=8)

        # Create a label for the speed options
        self.speed_option_label = tk.Label(root, text="Select Speed Option", font=("Arial", 18, "bold"))
        self.speed_option_label.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="w")

        # Create input buttons
        self.input_buttons_frame = tk.Frame(root)
        self.input_buttons_frame.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="w")

        # Add buttons for different speeds
        speeds = [5000, 10000, 15000, 17000, 20000]
        for idx, speed in enumerate(speeds):
            button = tk.Button(self.input_buttons_frame, text=str(speed), command=lambda s=speed: self.set_speed(s), bg="blue", fg="white", font=("Arial", 18, "bold"))
            button.grid(row=0, column=idx, padx=10, pady=10)
            button.config(width=10, height=4)

        # Create a frame for current speed label and entry
        self.current_speed_frame = tk.Frame(root)
        self.current_speed_frame.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        # Create title for current speed label
        self.current_speed_title = tk.Label(self.current_speed_frame, text="Current Speed (RPM):", font=("Arial", 18, "bold"))
        self.current_speed_title.grid(row=0, column=0, sticky='w')

        # Create entry for displaying current speed
        self.current_speed_entry = tk.Entry(self.current_speed_frame, width=50, font=("Arial", 18), state='readonly')
        self.current_speed_entry.grid(row=0, column=1, sticky='w', padx=10)

        # Create a frame for actual speed label and entry
        self.actual_speed_frame = tk.Frame(root)
        self.actual_speed_frame.grid(row=8, column=0, padx=20, pady=10, sticky="w")

        # Create title for actual speed label
        self.actual_speed_title = tk.Label(self.actual_speed_frame, text="Actual Speed (RPM):", font=("Arial", 18, "bold"))
        self.actual_speed_title.grid(row=0, column=0, sticky='w')

        # Create entry for displaying actual speed
        self.actual_speed_entry = tk.Entry(self.actual_speed_frame, width=50, font=("Arial", 18), state='readonly')
        self.actual_speed_entry.grid(row=0, column=1, sticky='w', padx=10)

        # Start updating actual speed
        self.root.after(1000, self.update_rpm)

    def start_process(self):
        # Send the current speed command over serial
        if self.ser and self.current_command is not None:
            self.ser.write(str(self.current_command).encode())  # Convert command to bytes and send it
            messagebox.showinfo("Message", "Process started")

    def stop_process(self):
        # Send the 0 command over serial to stop the process
        if self.ser:
            self.ser.write(b'0')  # Send the command '0' as bytes to stop the process
        
        # Set speed to 0
        self.set_speed(0)
        
        # Disable the Start button
        self.start_button.config(state='disabled')
        
        # Display a message indicating the process has stopped
        messagebox.showinfo("Message", "Process stopped")

    def set_speed(self, speed):
        # Set the current speed
        self.current_speed = speed
        
        # Look up the command associated with the speed
        self.current_command = self.speed_to_command.get(speed, 0)

        # Update the current speed entry with the selected speed
        self.current_speed_entry.config(state='normal')
        self.current_speed_entry.delete(0, tk.END)
        self.current_speed_entry.insert(0, str(speed))
        self.current_speed_entry.config(state='readonly')

        # Enable/disable the Start button based on the selected speed
        if speed == 0:
            self.start_button.config(state='disabled')
        else:
            self.start_button.config(state='normal')

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        port_names = [port.device for port in ports]
        self.port_dropdown['values'] = port_names

    def on_select(self, event=None):
        if self.ser:
            self.ser.close()
        selected_port = self.port_dropdown.get()
        try:
            self.ser = serial.Serial(selected_port, 9600)  # Adjust baud rate as per your requirement
            self.serial_thread = threading.Thread(target=self.update_rpm)
            self.serial_thread.daemon = True
            self.serial_thread.start()
        except serial.SerialException:
            messagebox.showerror("Error", "Failed to open selected port.")
            return
        print("Selected port:", selected_port)

    def update_rpm(self):
        while True:
            try:
                rpm_data = self.ser.readline().decode().strip()
                self.actual_speed_entry.config(state='normal')
                self.actual_speed_entry.delete(0, tk.END)
                self.actual_speed_entry.insert(0, rpm_data)
                self.actual_speed_entry.config(state='readonly')
            except serial.SerialException:
                print("Serial port disconnected.")
                break

# Create main window
root = tk.Tk()
app = ViscometerController(root)
root.mainloop()
