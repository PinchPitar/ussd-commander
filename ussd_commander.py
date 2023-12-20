import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import os
from string_to_pdu_converter import PDUEncoder
from pdu_to_string_converter import PDUDecoder
import re


class USSDPhoneUI(tk.Tk):
    def __init__(self, ussd_session_class):
        super().__init__()
        self.ussd_session_class = ussd_session_class
        self.ussd_session = None
        self.title("USSD Commander")
        self.geometry("300x600")  # Width x Height
        self.pdu_enabled = tk.BooleanVar(value=True)  # Add this line
        self.selected_modem = tk.StringVar()  # Add this line
        self.modem_list = self.get_modem_list()  # Add this line

        self.create_widgets()
        self.set_widgets_state('disabled')  # Initially disable widgets

    def get_modem_list(self):
        ports = serial.tools.list_ports.comports()
        return [(port.device, port.description) for port in ports]

    def create_widgets(self):

        # Add these lines to create a new frame for the dropdown menu
        self.dropdown_frame = tk.Frame(self)
        self.dropdown_frame.pack(fill=tk.X, expand=True, pady=10)

        # Add these lines to create the dropdown menu
        modem_descriptions = [desc for _, desc in self.modem_list]
        self.modem_menu = tk.OptionMenu(self.dropdown_frame, self.selected_modem, *modem_descriptions)
        self.modem_menu.grid(row=0, column=0, sticky="we")

        # Add these lines to create the refresh button
        self.refresh_button = tk.Button(self.dropdown_frame, text="Refresh", command=self.refresh_modem_list)
        self.refresh_button.grid(row=0, column=1)

        # Configure the column weights to allocate extra space to the dropdown menu
        self.dropdown_frame.grid_columnconfigure(0, weight=1)
        self.dropdown_frame.grid_columnconfigure(1, weight=0)

        # Connect, Disconnect and Clear buttons frame
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=10)

        # Clear button
        self.clear_button = tk.Button(self.buttons_frame, text="Clear", command=self.on_clear)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Connect button
        self.connect_button = tk.Button(self.buttons_frame, text="Connect", command=self.on_connect)
        self.connect_button.pack(side=tk.LEFT, padx=5)

        # Disconnect button
        self.disconnect_button = tk.Button(self.buttons_frame, text="Disconnect", command=self.on_disconnect)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)

        # Display area
        self.display = tk.Text(self, height=10, width=25)
        self.display.pack(pady=10)

        # Input field
        self.input_field = tk.Entry(self, width=25)
        self.input_field.pack(pady=10)

        # Keypad
        self.keypad_frame = tk.Frame(self)
        self.keypad_frame.pack(pady=10)

        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            '*', '0', '#'
        ]

        row = 0
        col = 0
        for button in buttons:
            btn = tk.Button(self.keypad_frame, text=button, width=5, height=2, 
                      command=lambda b=button: self.on_keypad_press(b))
            btn.grid(row=row, column=col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Send, Backspace and Cancel buttons frame
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=10)

        # Send button
        self.send_button = tk.Button(self.buttons_frame, text="Send", command=self.on_send)
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Backspace button
        self.backspace_button = tk.Button(self.buttons_frame, text='⌫', width=5, height=2, 
                                          command=self.on_backspace_press)
        self.backspace_button.pack(side=tk.LEFT, padx=5)

        # Cancel button
        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # PDU toggle
        self.pdu_toggle = tk.Checkbutton(self.buttons_frame, text="PDU", variable=self.pdu_enabled)
        self.pdu_toggle.pack(side=tk.LEFT, padx=5)


    def set_widgets_state(self, state):
        """ Enable or disable widgets """
        self.send_button['state'] = state
        self.input_field['state'] = state
        self.cancel_button['state'] = state
        for widget in self.keypad_frame.winfo_children():
            widget.configure(state=state)

    def refresh_modem_list(self):
        # Update the modem list
        self.modem_list = self.get_modem_list()

        # Clear the current menu
        self.modem_menu['menu'].delete(0, 'end')

        # Add the new modems to the menu
        for desc in self.modem_list:
            self.modem_menu['menu'].add_command(label=desc, command=tk._setit(self.selected_modem, desc))

    def on_connect(self):
        try:
            self.ussd_session = self.ussd_session_class()
            self.set_widgets_state('normal')  # Enable widgets
            self.connect_button['state'] = 'disabled'  # Disable connect button
            self.display.insert(tk.END, "Connected to modem\n\n")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def on_keypad_press(self, button):
        current_text = self.input_field.get()
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, current_text + button)

    def on_backspace_press(self):
        current_text = self.input_field.get()
        # Delete the last character if the input field is not empty
        if current_text:
            self.input_field.delete(len(current_text) - 1)

    def on_send(self):
        user_input = self.input_field.get()
        if not user_input.strip():
            messagebox.showerror("Error", "Please enter a USSD code or reply.")
            return

        # Check if a USSD session is active, if not, create a new one
        if self.ussd_session is None:
            self.ussd_session = USSDSession()

        try:
            response = self.ussd_session.start_ussd_session(user_input)
            self.display.insert(tk.END, f"Sent: {user_input}\nReceived: {response}\n\n")
            self.input_field.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_cancel(self):
        # Clear the input field
        self.input_field.delete(0, tk.END)

        # If a USSD session is active, send the USSD cancelling AT command and close it
        if self.ussd_session is not None:
            try:
                self.ussd_session.send_at_command('AT+CUSD=2')
                self.display.insert(tk.END, "USSD session cancelled\n\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.ussd_session.close()
                self.ussd_session = None

    def on_clear(self):
        self.display.delete(1.0, tk.END)

    def on_disconnect(self):
        if self.ussd_session is not None:
            try:
                # Send the USSD cancelling AT command
                self.ussd_session.send_at_command('AT+CUSD=2')
                self.display.insert(tk.END, "USSD session cancelled\n\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.ussd_session.close()
                self.ussd_session = None
                self.display.insert(tk.END, "Disconnected\n\n")
                self.connect_button['state'] = 'normal'  # Enable connect button

    def on_window_close(self):
        if self.ussd_session is not None:
            self.ussd_session.close()
        self.destroy()

    def refresh_modem_list(self):
        # Update the modem list
        self.modem_list = self.get_modem_list()

        # Clear the current menu
        self.modem_menu['menu'].delete(0, 'end')

        # Add the new modems to the menu
        for desc in self.modem_list:
            self.modem_menu['menu'].add_command(label=desc, command=tk._setit(self.selected_modem, desc))



class USSDSession:
    def __init__(self):
        self.ser = serial.Serial(self.find_modem(), baudrate=115200, timeout=2)

    def find_modem(self):
        selected_modem_desc = app.selected_modem.get()
        for port, desc in app.modem_list:
            if desc == selected_modem_desc:
                return port
        raise ValueError("Modem not found.")

    def extract_pdu_text(self, response):
        # Create an instance of the PDUEncoder class
        pdu_converter = PDUDecoder()

        match = re.search(r'\+CUSD: \d,"(.*?)",\d+', response)
        if match:
            # If a match is found, decode the PDU text and return it
            pdu_text = match.group(1)
            decoded_text = pdu_converter.pdu_to_string(pdu_text)
            return decoded_text
        else:
            # If no match is found, return None
            return None

    def send_at_command(self, command):
        self.ser.write(f"{command}\r".encode())
        read = str(self.ser.read(1200), 'utf-8')
        return read

    def get_hex_message(self, response):
        if "+CUSD: 1," in response or "+CUSD: 0," in response:
            prefix = "+CUSD: 1,\"" if "+CUSD: 1," in response else "+CUSD: 0,\""
            start_idx = response.index(prefix) + len(prefix)
            end_idx = response.index("\",", start_idx)
            hex_message = response[start_idx:end_idx]
            return hex_message
        else:
            return None

    def start_ussd_session(self, ussd_code):
        # Modify this method to use the PDU encoder only when it's enabled
        if app.pdu_enabled.get():
            pdu_converter = PDUEncoder()
            ussd_code = pdu_converter.string_to_pdu(ussd_code)

        response = self.send_at_command(f'AT+CUSD=1,"{ussd_code}",15')
        decoded_response = self.extract_pdu_text(response) if app.pdu_enabled.get() else response
        return decoded_response

    def reply_ussd_session(self, reply):
        # Modify this method to use the PDU encoder only when it's enabled
        if app.pdu_enabled.get():
            pdu_converter = PDUEncoder()
            reply = pdu_converter.string_to_pdu(reply)

        response = self.send_at_command(f'AT+CUSD=1,"{reply}",15')
        decoded_response = self.extract_pdu_text(response) if app.pdu_enabled.get() else response
        return decoded_response

    def close(self):
        if self.ser.is_open:
            self.ser.close()


if __name__ == "__main__":
    app = USSDPhoneUI(USSDSession)
    app.protocol("WM_DELETE_WINDOW", app.on_window_close)  # Handle window closing
    app.mainloop()