import tkinter as tk


class main_window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("WiFi Audit Device")
        self.create_window()
        self.pack()

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
        self.network_list_button.grid(row=1, column=1, sticky="ew")

        self.dictionary_attack_button = tk.Button(self)
        self.dictionary_attack_button["text"] = "Dictionary Attack"
        self.dictionary_attack_button.grid(row=2, column=0, sticky="ew")

        self.handshake_intercept_button = tk.Button(self)
        self.handshake_intercept_button["text"] = "WPA Handshake Interception"
        self.handshake_intercept_button.grid(row=2, column=1, sticky="ew")

root = tk.Tk()
main = main_window(root)
main.mainloop()