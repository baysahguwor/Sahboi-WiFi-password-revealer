import subprocess
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

# Create a new tkinter window
root = tk.Tk()

# Set window size and title
root.geometry("500x600")
root.title("Sahboi WiFi password revealer")

# Define style for the window
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Add a label to the window
label = ttk.Label(root, text="Sahboi WiFi password revealer")
label.pack(pady=10)

# Add a listbox to the window to display the profiles
listbox = tk.Listbox(root, font=("Arial", 12), height=15)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Define a function to scan for the profiles
def scan_network_profiles():
    # Clear the listbox
    listbox.delete(0, tk.END)
    # Scan for profiles
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profiles"], shell=True)
        output = output.decode("utf-8")
        lines = output.split("\n")
        profile_names = []
        for line in lines:
            if "All User Profile" in line:
                profile_names.append(line.split(":")[1].strip())
        for profile_name in profile_names:
            listbox.insert(tk.END, profile_name)
    except Exception as e:
        messagebox.showerror(title="Error", message=str(e))

# Define a function to retrieve and display the password for the selected profile
# Add a label to display the password
password_label = ttk.Label(root, font=("Arial", 12), text="")
password_label.pack(pady=10)

def show_password():
    # Get the selected item from the listbox
    selected_item = listbox.get(listbox.curselection())
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profile", selected_item, "key=clear"], shell=True)
        output = output.decode("utf-8")
        password_line = [line.strip() for line in output.split("\n") if "Key Content" in line][0]
        password = password_line.split(":")[1].strip()
        password_label.config(text=f"The password for {selected_item} is {password}", background="#ffff00")
        copy_button = ttk.Button(password_label, text="Copy", command=lambda: root.clipboard_append(password))
        #copy_button.pack(side="right", padx=10)
    except Exception as e:
        messagebox.showerror(title=selected_item, message=str(e))


# Add a button to the window to start the scan
button = ttk.Button(root, text="Scan for Network Profiles", command=scan_network_profiles)
button.pack(side=tk.TOP, pady=10)

# Add a button to the window to display the password for the selected profile
button2 = ttk.Button(root, text="Show Password", command=show_password)
button2.pack(side=tk.BOTTOM, pady=10)

# Run the tkinter event loop
root.mainloop()
