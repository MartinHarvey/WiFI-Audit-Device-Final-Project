import tkinter as tk
import tkinter.filedialog
import network_list
import bluetooth_list
import port_scanner
import packet_interception
import network_dictionary_attack
import handshake_intercept
import sys
from io import StringIO
from multiprocessing import Process

class app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.change_frame(main_page)

    # Create a new frame, providing extra args if necessary, and
    # destroy current frame before replacing with new frame
    def change_frame(self, frame_type,*args):
        frame = frame_type(self, *args)
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
    
    #Creates buttons that lead to other pages
    def create_window(self):
        self.port_scanner_button = tk.Button(
            self,
            text="Port Scanner",
            command= lambda: self.master.change_frame(port_scan_opt_page)
        ).grid(row=0, column=0, sticky="ew")

        self.packet_sniff_button = tk.Button(
            self,
            text = "Packet Interception",
            command = lambda: self.master.change_frame(packet_sniff_opt_page)
        ).grid(row=0, column=1, sticky="ew")

        self.bluetooth_list_button = tk.Button(
            self,
            text="Local Bluetooth Devices",
            command = lambda: self.master.change_frame(bluetooth_opt_page)
        ).grid(row=1, column=0, sticky="ew")

        self.network_list_button = tk.Button(
            self,
            text = "Local WiFi Networks",
            command = lambda: self.master.change_frame(network_list_opts_page)
        ).grid(row=1, column=1, sticky="ew")

        self.dictionary_attack_button = tk.Button(
            self,
            text = "Dictionary Attack",
            command = lambda: self.master.change_frame(dictionary_attack_opt_page)
        ).grid(row=2, column=0, sticky="ew")

        self.handshake_intercept_button = tk.Button(
            self,
            text = "WPA Handshake Interception",
            command = lambda: self.master.change_frame(handshake_intercept_opt_page)
        ).grid(row=2, column=1, sticky="ew")

class network_list_opts_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.master = master
        self.master.title("Network List")
        self.create_window()
        self.pack()
    
    def create_window(self):
        self.main_label = tk.Label(
            self,
            text = "Network List Options"
        ).grid(row=0, column=0)

        #Allows user to select output file if they want
        #Set to None as default
        self.output = None
        self.open_file_label = tk.Label(
            self,
            text="Output to file (optional)"
        ).grid(row=1, column=0)

        self.open_file_button = tk.Button(
            self,
            text = "Choose file",
            command = lambda: self.out_file()
        ).grid(row=1, column=1)

        self.list_res_button = tk.Button(
            self,
            text = "Run Network List",
            command = lambda: self.master.change_frame(
                    network_page,
                    self.output
                    )   
        ).grid(row=2, column=1)

        self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(main_page)
            ).grid(row=2, column=0)

    def out_file(self):
        #Creates a file dialog, returns file path of selected file, used to set self.output
        self.output = tk.filedialog.asksaveasfilename(
                    title = "Where do you want to save the scan results?", 
                    filetypes = (("txt files","*.txt"), ("all files","*.*"))
                    )
                
class network_page(tk.Frame):
    def __init__(self, master, output=None):
        super().__init__(master)
        self.output = output
        self.master = master
        self.master.title("Network List")
        self.create_window()
        self.pack()

    def create_window(self):
        #If output is none, then the user hasnt selected a output file
        if(self.output is None):
            self.main_label = tk.Label(
                self,
                text = "Network List"
            ).grid(row=0, column=0)

            self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(main_page)
            ).grid(row=2, column=0)
            
            self.scrollbar = tk.Scrollbar(
                self,
            )
            self.scrollbar.grid(row=1,column=1, sticky='nsew')

            self.output_box = tk.Text(
                self,
                height = 15,
                width  = 57,
                yscrollcommand = self.scrollbar.set #This sets the position of the scrollbar
            )
            self.output_box.grid(row=1, column=0)
            self.scrollbar['command'] = self.output_box.yview #This allows the scrollbar to scroll the textbox

            #Used to collect output of network_list. Sets stdout to StringIO object, gets
            #value from that object, and resets stdout again. Results are displayed 
            sys.stdout = StringIO()
            network_list.main([""])
            self.output_box.insert(tk.END, sys.stdout.getvalue())
            sys.stdout = sys.__stdout__
        else:
            #User has selected output file, less info to display
            network_list.main(["", self.output])
            self.main_label = tk.Label(
                self,
                text = "Network List saved to \n " + self.output
            ).pack()

            self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(main_page)
            ).pack()

class bluetooth_opt_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Bluetooth List Options")
        self.create_window()
        self.pack()
    
    def create_window(self):
        self.main_label = tk.Label(
            self,
            text = "Bluetooth List Options"
        ).grid(row=0, column=0)

        #Allows user to select output file if they want
        #Set to None as default
        self.output = None
        self.open_file_label = tk.Label(
            self,
            text="Output to file (optional)"
        ).grid(row=1, column=0)

        self.open_file_button = tk.Button(
            self,
            text = "Choose file",
            command = lambda: self.out_file()
        ).grid(row=1, column=1)

        self.run_list_button = tk.Button(
            self,
            text = "Run Blueooth Device List",
            command = lambda: self.master.change_frame(
                    bluetooth_page,
                    self.output
                    )   
        ).grid(row=2, column=1)

        self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(main_page)
            ).grid(row=2, column=0)

    def out_file(self):
        #Creates a file dialog, returns file path of selected file, used to set self.output
        self.output = tk.filedialog.asksaveasfilename(
                    title = "Where do you want to save the scan results?", 
                    filetypes = (("txt files","*.txt"), ("all files","*.*"))
                    )

class bluetooth_page(tk.Frame):
    def __init__(self, master, output):
        super().__init__(master)
        self.master = master
        self.output = output
        self.master.title("Bluetooth Devices")
        self.create_window()
        self.pack()

    def create_window(self):
        if self.output is None:
            #Create the scrollbar
            self.scrollbar = tk.Scrollbar(
                self,
            )
            self.scrollbar.grid(row=1,column=1, sticky='nsew')

            self.output_box = tk.Text(
                self,
                height = 15,
                width  = 57,
                yscrollcommand = self.scrollbar.set #This sets the position of the scrollbar
            )
            self.output_box.grid(row=1, column=0)
            self.scrollbar['command'] = self.output_box.yview #This allows the scrollbar to scroll the textbox

            self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(bluetooth_opt_page)
            ).grid(row=2, column=0)

            sys.stdout = StringIO()
            bluetooth_list.main([])
            self.output_box.insert(tk.END, sys.stdout.getvalue())
            sys.stdout = sys.__stdout__
        else:
            self.main_label = tk.Label(
                self,
                text = "Bluetooth Devices"
            ).pack()
            bluetooth_list.main(["", self.output])
            self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(bluetooth_opt_page)
            ).pack()

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
        ).grid(row=0, column=0)

        #Entry box and label for address
        self.addr_label = tk.Label(
            self,
            text= "Address"
        ).grid(row=1, column=0)
        self.addr_entry = tk.Entry(
            self
        )
        self.addr_entry.grid(row=1, column=1)

        #Start Port entry box and label
        self.sport_label = tk.Label(
            self,
            text = "Start Port"
        ).grid(row=2, column=0)
        self.sport_entry = tk.Entry(
            self
        )
        self.sport_entry.grid(row=2, column=1)

        #End Port entry box and label
        self.eport_label = tk.Label(
            self,
            text = "End Port"
        ).grid(row=3, column=0)
        self.eport_entry = tk.Entry(
            self
        )
        self.eport_entry.grid(row=3, column=1)

        #Output file selection works the same as on other pages
        self.output = None
        self.open_file_label = tk.Label(
            self,
            text="Output to file (optional)"
        ).grid(row=4, column=0)

        self.open_file_button = tk.Button(
            self,
            text = "Choose file",
            command = lambda: self.out_file()
        ).grid(row=4, column=1)

        #Run button grabs extra parameters from entry boxes and output to 
        #Provide to change_frame as *args
        self.run_button = tk.Button(
            self,
            text = "Run Port Scanner",
            command = lambda: self.master.change_frame(
                    port_scan_results,
                    self.addr_entry.get(),
                    self.sport_entry.get(),
                    self.eport_entry.get(),
                    self.output
                    )   
        ).grid(row=5, column=1)

        self.back_button = tk.Button(
            self,
            text = "Go Back",
            command = lambda: self.master.change_frame(main_page)
        ).grid(row=5, column = 0)
    
    def out_file(self):
        self.output = tk.filedialog.asksaveasfilename(
                    title = "Where do you want to save the scan results?", 
                    filetypes = (("txt files","*.txt"), ("all files","*.*"))
                    )

class port_scan_results(tk.Frame):
    #Initialiser for GUI class. Takes in parameters to run port scanner from opts page
    def __init__(self, master, addr, sport, eport, output=None):
        super().__init__(master)
        self.master = master
        self.addr = addr
        self.sport = sport
        self.eport = eport
        self.output = output
        self.master.title("Port Scanner")
        self.create_window()
        self.pack()


    def create_window(self):
        #User did not select output file if self.output is None
        if(self.output is None):
            #Create the scrollbar
            self.scrollbar = tk.Scrollbar(
                self,
            )
            self.scrollbar.grid(row=1,column=1, sticky='nsew')

            self.output_box = tk.Text(
                self,
                height = 15,
                width  = 57,
                yscrollcommand = self.scrollbar.set #This sets the position of the scrollbar
            )
            self.output_box.grid(row=1, column=0)
            self.scrollbar['command'] = self.output_box.yview #This allows the scrollbar to scroll the textbox

            #Redirection of stdout to screen is done the same in other pages
            sys.stdout = StringIO()
            port_scanner.main(["", self.addr, self.sport, self.eport])
            self.output_box.insert(tk.END, sys.stdout.getvalue())
            sys.stdout = sys.__stdout__
            
            self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(port_scan_opt_page)
            ).grid(row=2, column=0)
        else:
            #If user chose to output to file
            port_scanner.main(["", self.addr, self.sport, self.eport, self.output])
            self.out_label = tk.Label(
                self,
                text = "Port scan results outputted to \n" + self.output
            ).pack()

            self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(port_scan_opt_page)
            ).pack()

class packet_sniff_opt_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Packet Interception Options")
        self.create_window()
        self.pack()
    
    def create_window(self):
        self.main_label = tk.Label(
            self,
            text = "Packet Sniffing Options"
        ).grid(row=0, column=0)

        #Allows user to select output file if they want
        #Set to None as default
        self.output = None
        self.open_file_label = tk.Label(
            self,
            text="Output to file"
        ).grid(row=1, column=0)

        self.open_file_button = tk.Button(
            self,
            text = "Choose file",
            command = lambda: self.out_file()
        ).grid(row=1, column=1)

        self.packet_count_label = tk.Label(
            self,
            text = "How many packets should be \nintercepted? Set to 0 to run infinitely"
        ).grid(row=2, column=0)
        self.count_entry = tk.Entry(
            self
        )
        self.count_entry.grid(row=2, column=1)

        self.packet_sniff_button = tk.Button(
            self,
            text = "Run Packet Sniff",
            command = lambda: self.master.change_frame(
                    packet_sniff_page,
                    self.output,
                    self.count_entry.get()
                    )   
        ).grid(row=3, column=1)

        self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(main_page)
            ).grid(row=3, column=0)

    def out_file(self):
        self.output = tk.filedialog.asksaveasfilename(
                    title = "Where do you want to save the scan results?", 
                    filetypes = (("pcap file","*.pcap"), ("all files","*.*"))
                    )

class packet_sniff_page(tk.Frame):
    def __init__(self, master, output, count):
        super().__init__(master)
        self.master = master
        self.master.title("Packet Sniffing")
        self.output = output
        self.count  = count
        self.create_window()
        self.pack()
    
    def create_window(self):
            #Create a process to run the packet sniffer on, as user can choose for it 
            #to run indefinitely
            self.packet_sniff_process = Process(
                target=packet_interception.main, 
                args=(["", self.output, self.count],)
                ) #Create the process
            self.packet_sniff_process.start() #start process
            self.page_label = tk.Label(
                self,
                text = "Packet Interception \n Saved to" + self.output
            ).pack()
            #Kill button for process
            self.kill_process_button = tk.Button(
                self,
                text = "Stop Packet Interception",
                command = lambda: self.packet_sniff_process.terminate()
            ).pack(side=tk.RIGHT)

            #Go back to option page for packet interception
            self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(packet_sniff_opt_page)
            ).pack(side=tk.LEFT)

class dictionary_attack_opt_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Dictionary Attack Options")
        self.create_window()
        self.pack()

    def create_window(self):
        self.options_label = tk.Label(
            self,
            text = "Dictionary Attack Options"
        ).grid(row = 0, column=0)

        self.wordlist_label = tk.Label(
            self,
            text = "Select Wordlist"
        ).grid(row=1, column=0)

        self.wordlist = None
        self.select_worlist_button = tk.Button(
            self,
            text = "Select Wordlist",
            command = lambda: self.get_wordlist()
        ).grid(row=1, column=1)

        self.target_label = tk.Label(
            self,
            text = "Target Network Name: "
        ).grid(row=2, column=0)
        self.target_entry = tk.Entry(
            self
        )
        self.target_entry.grid(row=2, column=1)

        self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(main_page)
            ).grid(row=3, column=0)

        self.run_button = tk.Button(
            self,
            text = "Run Dictionary Attack",
            command = lambda: self.master.change_frame(
                dictionary_attack_page, 
                self.wordlist,
                self.target_entry.get()
                )
        ).grid(row=3, column=1)
    
    def get_wordlist(self):
        self.wordlist = tk.filedialog.askopenfilename(
                            title = "Where is the wordlist?", 
                            filetypes = (("txt file","*.txt"), ("all files","*.*"))
                        )

class dictionary_attack_page(tk.Frame):
    def __init__(self, master, wordlist, target):
        super().__init__(master)
        self.master = master
        self.target = target
        self.wordlist = wordlist
        self.master.title("Dictionary Attack")
        self.create_window()
        self.pack()

    def create_window(self):
        self.results_label = tk.Label(
            self,
            text = "Dictionary Attack Results"
        ).grid(row=0, column=0)

        self.output_box = tk.Text(
            self,
            height = 15,
            width  = 57,
        )
        self.output_box.grid(row=1, column=0)

        sys.stdout = StringIO()
        network_dictionary_attack.main(["", self.target, self.wordlist])
        self.output_box.insert(tk.END, sys.stdout.getvalue())
        sys.stdout = sys.__stdout__

        self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(dictionary_attack_opt_page)
            ).grid(row=2, column=0)

class handshake_intercept_opt_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Handshake Intercept Options")
        self.create_window()
        self.pack()

    def create_window(self):
        self.main_label = tk.Label(
            self,
            text = "Handshake Interception Options"
        ).grid(row=0, column=0)
    
        self.output_label = tk.Label(
            self,
            text = "Choose output .pcap file",
        ).grid(row=1, column=0)
        self.output_button = tk.Button(
            self,
            text = "Choose file",
            command = self.out_file
        ).grid(row=1, column=1)
        self.channel_label = tk.Label(
            self,
            text = "Choose WiFi channel to listen on"
        ).grid(row=2, column=0)
        self.channel_entry = tk.Entry(
            self
        )
        self.channel_entry.grid(row=2, column=1)
        
        self.back_button = tk.Button(
                self,
                text = "Go Back",
                command = lambda: self.master.change_frame(main_page)
            ).grid(row=3, column=0)
        self.run_button = tk.Button(
            self,
            text = "Capture Handshakes",
            command = lambda: self.master.change_frame(
                handshake_intercept_page,
                self.output,
                self.channel_entry.get()
            )
        ).grid(row=3, column=1)
        
    def out_file(self):
        self.output = tk.filedialog.asksaveasfilename(
                    title = "Where do you want to save the scan results?", 
                    filetypes = (("pcap file","*.pcap"), ("all files","*.*"))
                    )

class handshake_intercept_page(tk.Frame):
    def __init__(self, master, output, channel):
        super().__init__(master)
        self.master = master
        self.master.title("Handshake Interception")
        self.output = output
        self.channel  = channel
        self.create_window()
        self.pack()
    
    def create_window(self):
        self.main_label = tk.Label(
            self,
            text = "Handshake Interception \n saved to \n" + self.output
        ).pack()
        self.interception_process = Process(
            target=handshake_intercept.main,
            args=(["", self.output, self.channel],)
        )
        self.interception_process.start()

        self.kill_process_button = tk.Button(
            self,
            text = "Stop Handshake Interception",
            command = lambda: self.interception_process.terminate()
        ).pack(side=tk.RIGHT)

        self.back_button = tk.Button(
            self,
            text = "Go Back",
            command = lambda: self.master.change_frame(handshake_intercept_opt_page)
        ).pack(side=tk.LEFT)



if __name__ == "__main__":
    #Create app object, sets its size and run it
    app = app()
    app.geometry("480x320")
    app.mainloop() 

