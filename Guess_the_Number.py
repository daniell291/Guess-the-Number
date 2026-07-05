#importing libaries
import tkinter as tk
import random
from playsound3 import playsound as snd
from datetime import datetime as dt
import os
import sys
from pygame import mixer
import ctypes
import platform

#something that pyinstaller needs
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#something for the right font
def load_font(font):
    the_font = resource_path(font)
    if not os.path.exists(the_font):
        return False
    user_os=platform.system()

    if user_os=="Windows":
        FR_PRIVATE = 0x10
        ctypes.windll.gdi32.AddFontResourceExW(the_font, FR_PRIVATE, 0)

    elif user_os == "Linux":
        libfontconfig = ctypes.CDLL("libfontconfig.so.1")
        libfontconfig.FcConfigGetCurrent.restype = ctypes.c_void_p
        libfontconfig.FcConfigAppFontAddFile.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
        ]
        libfontconfig.FcConfigAppFontAddFile.restype = ctypes.c_bool
        config = libfontconfig.FcConfigGetCurrent()
        result = libfontconfig.FcConfigAppFontAddFile(
        config, the_font.encode("utf-8")
        )
        return result
    
    elif user_os == "Darwin":
        cf = ctypes.CDLL(
            "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
        )
        ct = ctypes.CDLL(
            "/System/Library/Frameworks/CoreText.framework/CoreText"
        )
        cf.CFStringCreateWithCString.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_int32,
            ]
        cf.CFStringCreateWithCString.restype = ctypes.c_void_p
        cf.CFURLCreateWithFileSystemPath.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int32,
            ctypes.c_bool,
        ]
        cf.CFURLCreateWithFileSystemPath.restype = ctypes.c_void_p
        ct.CTFontManagerRegisterFontsForURL.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int32,
            ctypes.c_void_p,
        ]
        ct.CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool
        cf_string = cf.CFStringCreateWithCString(
            None, the_font.encode("utf-8"), 0x08000100
        )
        cf_url = cf.CFURLCreateWithFileSystemPath(
            None, cf_string, 0, False
        )
        result = ct.CTFontManagerRegisterFontsForURL(cf_url, 1, None)
        return result

load_font("VCR_OSD_MONO_1.001.ttf")

#setting up for bäckground music
mixer.init()
mixer.music.load(resource_path("Jeremy Blake - Powerup!.mp3"))
mixer.music.set_volume(1.0)
mixer.music.play(loops=-1)

#setting up for the game
def gamestart():
    global rand_num, max_num, start_time, level
    title.pack_forget()
    level=1
    max_num=[10, 100, 1000, 10000, 100000, 1000000]
    rand_num=random.randint(0,10)
    start_time=dt.now()
    game.pack(pady=20)

#level system
def guess(event=None):
    global hint, total_time, rand_num, level
    try:
        user_num = int(entry.get())
    except ValueError:
        hint.set("invalid number")
        entry.delete(0, tk.END)
        return
    if user_num < rand_num:
        hint.set("↑ HIGHER ↑")
    elif user_num > rand_num:
        hint.set("↓ LOWER ↓")
    elif user_num == rand_num:
        if level != 6:
            snd(resource_path("pokemon-red_blue_yellow-level-up-sound-effect.mp3"), block=False)
            level+=1
            rand_num=random.randint(0,max_num[level-1])
            hint.set(f"LEVEL {level}!")
        elif level == 6:
            win_text_out.set(f"Time: {dt.now() - start_time}")
            game.pack_forget()
            snd(resource_path("win31.mp3"), block=False)
            win.pack(pady=20)
    entry.delete(0, tk.END)

def play_again():
    hint.set("type your guess below")
    win.pack_forget()
    title.pack(pady=20)

#setting some tkinter thinks
root = tk.Tk()
hint = tk.StringVar()
hint.set("type your guess below")
win_text_out = tk.StringVar()
root.title("Guess the Number")
root.iconbitmap(resource_path("guess the number icon.ico"))
root.geometry("854x480")
root.config(bg="black")

#another tkinker setting but for frames
title=tk.Frame(root, bg="black")
game = tk.Frame(root, bg="black")
win = tk.Frame(root, bg="black")
title.pack(pady=20)

#title frame
title_msg=random.randint(1,9)
title_photo = tk.PhotoImage(file=resource_path(f"guess the number title {title_msg}.png"))
title_photo_smaller = title_photo.subsample(2, 2)
title_image = tk.Label(title, image=title_photo_smaller, bg="black")
title_image.pack()

start_button = tk.Button(title, text="Start!", command=gamestart, fg="black", bg="#00FF00", height=1, width=11, font=("vcr osd mono",30), justify="center")
start_button.pack(pady=50)

#game frame
photo = tk.PhotoImage(file=resource_path("guess the number logo.png"))
photo_smaller = photo.subsample(2, 2)
image = tk.Label(game, image=photo_smaller, bg="black")
image.pack()

hint_out=tk.Label(game, textvariable=hint, font=("vcr osd mono",25), bg="black", fg="#00FF00")
hint_out.pack()

guess_button = tk.Button(game, text="Guess!", command=guess, fg="black", bg="#00FF00", width=6, height=2, font=("vcr osd mono",20), justify="center")
guess_button.pack(side = tk.RIGHT)

entry = tk.Entry(game)
entry.config(font=("vcr osd mono",50), bg="black", fg="#00FF00", justify="center", width=75)
entry.pack(side=tk.LEFT)
entry.bind("<Return>", guess)

#win frame
photo_win = tk.PhotoImage(file=resource_path("guess the number logo win edition.png"))
photo_win_smaller = photo_win.subsample(3, 3)
image_win = tk.Label(win, image=photo_win_smaller, bg="black")
image_win.pack()

win_text=tk.Label(win, textvariable=win_text_out, font=("vcr osd mono",40), bg="black", fg="#00FF00")
win_text.pack(pady=20)

again_button = tk.Button(win, text="PLAY AGAIN!", command=play_again, fg="black", bg="#00FF00", font=("vcr osd mono",20), justify="center")
again_button.pack()

#the main event loop
root.mainloop()
#version 2 made by daniell291 5th july 2026