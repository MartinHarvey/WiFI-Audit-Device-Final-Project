import tkinter as tk
import network_list
import bluetooth_list
import sys
from io import StringIO

class app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.change_frame(main_page)

    def change_frame(self, frame_type):
        frame = frame_type(self)
        if self._frame != None:
            self._frame.destroy()
        self._frame = frame
        self._frame.pack()

class main_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("WiFi Audit Device")
        self.create_window()
    

    def create_window(self):
        self.port_scanner_button = tk.Button(
            self,
            text="Port Scanner",
            command= lambda: self.master.change_frame(port_scan_opt_page)
        ).grid(row=0, column=0, sticky="ew")

        self.packet_sniff_button = tk.Button(
            self,
            text = "Packet Interception",
        ).grid(row=0, column=1, sticky="ew")

        self.bluetooth_list_button = tk.Button(
            self,
            text="Local Bluetooth Devices",
            command = lambda: self.master.change_frame(bluetooth_page)
        ).grid(row=1, column=0, sticky="ew")

        self.network_list_button = tk.Button(
            self,
            text = "Local WiFi Networks",
            command = lambda: self.master.change_frame(network_page)
        ).grid(row=1, column=1, sticky="ew")

        self.dictionary_attack_button = tk.Button(
            self,
            text = "Dictionary Attack",
        ).grid(row=2, column=0, sticky="ew")

        self.handshake_intercept_button = tk.Button(
            self,
            text = "WPA Handshake Interception"
        ).grid(row=2, column=1, sticky="ew")

class network_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.master = master
        self.master.title("Network List")
        self.create_window()
        self.pack()

    def create_window(self):
        self.main_label = tk.Label(
            self,
            text = "Network List"
        ).pack()

        self.back_button = tk.Button(
            self,
            text = "Go Back",
            command = lambda: self.master.change_frame(main_page)
        ).pack()

        sys.stdout = StringIO()
        network_list.main([])
        self.output = tk.Label(
            self,
            text = sys.stdout.getvalue()
        ).pack()
        sys.stdout = sys.__stdout__
        
class bluetooth_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Bluetooth Devices")
        self.create_window()
        self.pack()

    def create_window(self):
        self.main_label = tk.Label(self)
        self.main_label["text"] = "Bluetooth Devices"
        self.main_label.pack()

        self.back_button = tk.Button(
            self,
            text = "Go Back",
            command = lambda: self.master.change_frame(main_page)
        ).pack()

        
        sys.stdout = StringIO()
        bluetooth_list.main([])
        self.output = tk.Label(
            self,
            text = sys.stdout.getvalue()
        ).pack()
        sys.stdout = sys.__stdout__
class port_scan_opt_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Port Scanner Options")
        self.create_window()
        self.pack()
    
    def create_window(self):
        self.main_label = tk.Label(
            self,
            text = "Port Scanner Options"
        ).pack()

        self.address_entry = tk.Entry(
            self
        ).pack()
        self.sport_entry = tk.Entry(
            self
        ).pack()
        self.eport_entry = tk.Entry(
            self
        ).pack()

        self.run_button = tk.Button(
            self,
            text = "Run Port Scanner",
        ).pack()

        self.back_button = tk.Button(
            self,
            text = "Go Back",
            command = lambda: self.master.change_frame(main_page)
        ).pack()

    
if __name__ == "__main__":
    app = app()
    app.geometry("480x320")
    app.mainloop() 