import tkinter as tk
from tkinter import ttk
from tkinter import font
import os
from PIL import Image, ImageTk

def fade_in_animation():
    alpha = 0
    while alpha < 1:
        alpha += 0.005
        root.attributes('-alpha', alpha)
        root.update_idletasks()
        root.update()
    root.attributes('-alpha', 1)

def display_shortcuts():
    shortcut_text = """
    Tools:
    - Ad Blocker (Ctrl + B)
    - Password Manager (Ctrl + P)
    - Text Enc/Decryptor (Ctrl + E)
    
    Tab Management:
    - Open new Tab (Ctrl + N)
    - Close last Tab (Ctrl + M)
      
    Additional Features:
    - Search with DuckDuckGo (Toggle with '?')
    - Panic Button (F1)
    """

    custom_font = font.nametofont("TkDefaultFont")
    custom_font.configure(size=14)

    style = ttk.Style()
    style.configure("TLabel", foreground="white", background="#333333")
    
    shortcut_label = ttk.Label(root, text=shortcut_text, justify=tk.LEFT, style="TLabel", font=custom_font)
    shortcut_label.pack(padx=20, pady=20)

def setico(file_path):
    try:
        icon_image = Image.open(file_path)

        icon_image = ImageTk.PhotoImage(icon_image)

        root.tk.call('wm', 'iconphoto', root._w, icon_image)

    except Exception as e:
        print(f"Error setting window icon: {e}")

root = tk.Tk()
root.title("All available shortcuts")
root.geometry("450x450")
root.configure(bg="#333333")  
root.attributes('-alpha', 0)  

icon_path = os.path.join("home","assets", "icon.ico")
setico(icon_path)

display_shortcuts()

fade_in_animation()

root.mainloop()
