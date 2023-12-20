# USSD Commander

USSD Commander is a Python-based application designed for interacting with USSD (Unstructured Supplementary Service Data) sessions using a modem. It provides a graphical user interface (GUI) built with Tkinter, allowing users to send and receive USSD codes, manage modem connections, and handle responses in both plain text and PDU (Protocol Data Unit) format.

## Features

- **Modem Management**: Detects and manages multiple modems connected to the system.
- **USSD Session Handling**: Initiate, respond, and close USSD sessions.
- **PDU and Text Mode**: Supports both PDU and plain text formats for USSD communication.
- **Interactive GUI**: A user-friendly interface for interacting with USSD codes and responses.
- **Serial Communication**: Utilizes the serial library for modem communication.

## Installation

To use the USSD Commander, you need to have Python installed on your system. Additionally, the application depends on several Python libraries like `tkinter`, `serial`, and custom PDU converters.

1. **Install Python**: Ensure that Python is installed. You can download it from [Python's official website](https://www.python.org/downloads/).

2. **Install Dependencies**: Run the following command to install necessary libraries:

    ```bash
    pip install pyserial
    ```

    Note: `tkinter` usually comes pre-installed with Python. If it's missing, you may need to install it separately based on your operating system.

3. **Clone Repository or Download Code**: Get the application code by cloning the repository or downloading the source code.

4. **Run the Application**: Navigate to the directory containing the script and run:

    ```bash
    python ussd_commander.py
    ```

## Usage

1. **Start the Application**: Run the script to launch the USSD Commander GUI.
2. **Select Modem**: Use the dropdown menu to select the connected modem.
3. **Connect**: Click the 'Connect' button to establish a connection with the selected modem.
4. **Send USSD Code**: Enter a USSD code in the input field and press 'Send'.
5. **Manage Session**: Use the GUI buttons to respond, cancel, or clear USSD sessions.

## Example

Here's a simple example of how to use the application:

1. Launch the USSD Commander.
2. Select your modem from the dropdown list.
3. Click 'Connect' to initiate a connection.
4. Enter a USSD code (e.g., `*123#`) in the input field.
5. Click 'Send' to transmit the code.
6. View the response in the display area.

## Contributing

Contributions to the USSD Commander are welcome. Please feel free to fork the repository, make changes, and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
