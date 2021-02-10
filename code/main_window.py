import tkinter as tk

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
        self.port_scanner_button = tk.Button(self)
        self.port_scanner_button["text"] = "Port Scanner"
        self.port_scanner_button.grid(row=0, column=0, sticky="ew")

        self.packet_sniff_button = tk.Button(self)
        self.packet_sniff_button["text"] = "Packet Interception"
        self.packet_sniff_button.grid(row=0, column=1, sticky="ew")

        self.bluetooth_list_button = tk.Button(self)
        self.bluetooth_list_button["text"] = "Local Bluetooth Devices"
        self.bluetooth_list_button.grid(row=1, column=0, sticky="ew")

        self.network_list_button = tk.Button(self)
        self.network_list_button["text"] = "Local WiFi Networks"
        self.network_list_button["command"] = lambda: self.master.change_frame(network_page)
        self.network_list_button.grid(row=1, column=1, sticky="ew")

        self.dictionary_attack_button = tk.Button(self)
        self.dictionary_attack_button["text"] = "Dictionary Attack"
        self.dictionary_attack_button.grid(row=2, column=0, sticky="ew")

        self.handshake_intercept_button = tk.Button(self)
        self.handshake_intercept_button["text"] = "WPA Handshake Interception"
        self.handshake_intercept_button.grid(row=2, column=1, sticky="ew")

class network_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Network List")
        self.create_window()
        self.pack()

    def create_window(self):
        self.main_label = tk.Label(self)
        self.main_label["text"] = "Network List"
        self.main_label.pack()

        self.back_button = tk.Button(self)
        self.back_button["text"] = "Go Back"
        self.back_button["command"] = lambda: self.master.change_frame(main_page)
        self.back_button.pack()

if __name__ == "__main__":
    app = app()
    app.mainloop() 