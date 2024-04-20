# ConcentricCylinderViscometer
# Viscometer Controller

This is a Python application for controlling a viscometer device via a serial connection. The application provides a graphical user interface (GUI) for selecting serial ports, setting speed options, starting and stopping the process, and displaying current and actual speeds.

## Features

- Select serial port from a dropdown list
- Choose from predefined speed options
- Start and stop the process
- Display current and actual speeds in real-time
- Automatic refresh of available serial ports
- Error handling for serial port connection issues

## Requirements

- Python 3.x
- tkinter (included with Python standard library)
- pySerial library (`pip install pyserial`)

## Usage

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/yourusername/viscometer-controller.git
    ```

2. Navigate to the project directory:

    ```
    cd viscometer-controller
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Run the application:

    ```
    python viscometer_controller.py
    ```

5. Select the serial port from the dropdown list.
6. Choose the desired speed option.
7. Click the Start button to begin the process.
8. Click the Stop button to stop the process.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
