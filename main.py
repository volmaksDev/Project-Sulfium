### BASIC INFO ###

__title__ = 'Discord Sender.py'
__author__ = 'volmaks'
__version__ = '1.0.0'

### MODULES ###

import customtkinter
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import asyncio
import discord
from discord.ext import tasks, commands
from discord import *
import configparser
import threading
import time

### VARIABLES ###

client = discord.Client()
# MESSAGE = config.get('DEFAULT', 'MESSAGE').strip()
config = configparser.ConfigParser()
with open("Config.properties", "r") as f:
    config.read_file(f)

TOKEN = config.get('DEFAULT', 'TOKEN').strip()
CHANNEL_IDS = [int(channel_id.strip()) for channel_id in config.get('DEFAULT', 'CHANNEL_IDS').split(',')]
FILE_PATH = config.get('DEFAULT', 'FILE_PATH').strip()

### FUNCTIONS / EVENTS ###

@client.event
async def on_ready():
    Cmd_box.configure(placeholder_text=f"logged in as: {client.user}")

def Browse_Files():
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {file_path}")
        update_config_file(file_path)
        display_image(file_path)
    else:
        print("No file selected")

def update_config_file(new_path):
    config = configparser.ConfigParser()
    config.read('config.properties')
    if 'DEFAULT' not in config:
        config['DEFAULT'] = {}
    config['DEFAULT']['FILE_PATH'] = new_path
    with open('config.properties', 'w') as configfile:
        config.write(configfile)
    print(f"Updated config file with new path: {new_path}")
    Cmd_box.configure(placeholder_text=f"Updated config file with new path {new_path} ")

def display_image(file_path):
    image = Image.open(file_path)
    image = image.resize((300, 300), Image.Resampling.LANCZOS)  # Змінити розмір зображення
    imagepreview.configure(width=300, height=300)
    photo = ImageTk.PhotoImage(image)
    imagepreview.config(image=photo)
    imagepreview.image = photo

@tasks.loop(minutes=1) # You can change amount of minutes here.
async def Start_callback():
    for channel_id in CHANNEL_IDS:
        channel = client.get_channel(channel_id)
        if channel:
            # await channel.send(MESSAGE) - Remove "#" if you need message
            with open(FILE_PATH, "rb") as f:
                picture = discord.File(f)
                await channel.send(file=picture)

def Check_command():
    command = Cmd_box.get()
    pass

def Submit_Command():
    print("Command submitted")
    Check_command()

### APP INTERFACE ###

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.title("Discord Sender")
app.geometry("1000x600")
app.resizable(False,False)

channel_list = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=25, height=20, state=tk.DISABLED)
channel_list.place(x=770, y=50)
channel_list.configure(bg="#3e3e42")

Cmd_box = customtkinter.CTkEntry(app, placeholder_text="Enter Commands", placeholder_text_color="white", width=708, height=50)
Cmd_box.place(x=5,y=480)

imagepreview = tk.Label(app, width=100, height=27)
imagepreview.place(x=5, y=50)
imagepreview.config(bg="#3e3e42")

ImageLabel = customtkinter.CTkLabel(app, text="Image preview", font=('Arial Bold', 25))
ImageLabel.place(x=10,y=10)

BrowseButton = customtkinter.CTkButton(app, text="Select Image", command=Browse_Files, font=('Arial', 20), border_color="white", border_width=1, fg_color="#3e3e42")
BrowseButton.place(x=660, y=550)

Startbutton = customtkinter.CTkButton(app, text="Start", command=Start_callback, font=('Arial', 20), border_color="white", border_width=1, fg_color="#3e3e42")
Startbutton.place(x=850, y=550)

SubmitCommandButton = customtkinter.CTkButton(app, text="Submit Command", command=Submit_Command, font=('Arial', 20), border_color="white", border_width=1, fg_color="#3e3e42")
SubmitCommandButton.place(x=450, y=550)

app.mainloop()
