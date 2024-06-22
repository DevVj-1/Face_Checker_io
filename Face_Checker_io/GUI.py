"""
Project developed under Gurugram Police Cyber Security GPCSSI Program, June 2024, by Dev Vijay ,cyber warrior (CW-129)
"""
"""
#For Windows
##########################################################
You can run this script by writing " python .\GUI.py "
##########################################################
"""

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Toplevel, simpledialog
from PIL import Image, ImageTk
import face_recognition
import numpy as np
import webbrowser
import requests
from io import BytesIO
from threading import Thread
import cv2



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")

# ------------------------------------------------------------------------------------Face_comparison

# Function to load image from a file path or URL
def load_image(path_or_url):
    if path_or_url.startswith('http'):
        response = requests.get(path_or_url)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(path_or_url)
    return img


# Function to detect faces and prompt user to select one
def detect_and_draw_faces(image, label, crop_label, title):
    img_np = np.array(image)
    face_locations = face_recognition.face_locations(img_np)
    if not face_locations:
        messagebox.showinfo("No Face Detected", "No face detected in the image.")
        return

    if len(face_locations) > 1:
        # Create a dialog for selecting the face
        face_selection_dialog(img_np, face_locations, label, crop_label, title)
    else:
        draw_face(img_np, face_locations[0], label, crop_label)


# Function to draw face on the image and display it
def draw_face(img_np, face_location, label, crop_label):
    top, right, bottom, left = face_location
    img_with_boxes = img_np.copy()
    cv2.rectangle(img_with_boxes, (left, top), (right, bottom), (0, 255, 0), 2)

    face_img = img_np[top:bottom, left:right]
    img_with_face = Image.fromarray(face_img)
    img_with_face.thumbnail((190, 190)) #small face
    img_tk_face = ImageTk.PhotoImage(img_with_face)
    crop_label.config(image=img_tk_face)
    crop_label.image = img_tk_face

    img_with_boxes = Image.fromarray(img_with_boxes)
    img_with_boxes.thumbnail((300, 300)) #big face
    img_tk = ImageTk.PhotoImage(img_with_boxes)
    label.config(image=img_tk)
    label.image = img_tk
  #  show_popup(img_tk_face, root, 1216, 145)
    show_popup(img_tk_face, root, 1216, 145)

#pop up face location after upload
def show_popup(image, root, x, y):
    # Create a new Toplevel window (a dialog box)
    popup = Toplevel(root)
    popup.title("Face Image")

    # Set the position of the popup window
    popup.geometry(f"+{x}+{y}")

    # Set the background color of the popup window
    popup.configure(bg='green')

    # Add the image to the dialog box
    label = tk.Label(popup, image=image)
    label.pack()

#new]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

# Function to create a face selection dialog
def face_selection_dialog(img_np, face_locations, label, crop_label, title):
    dialog = Toplevel(root)
    dialog.title(title)

    label_text = tk.Label(dialog, text="Select a face to use:")
    label_text.pack()

    for i, (top, right, bottom, left) in enumerate(face_locations):
        face_img = img_np[top:bottom, left:right]
        face_img_pil = Image.fromarray(face_img)
        face_img_pil.thumbnail((100, 100))
        face_tk = ImageTk.PhotoImage(face_img_pil)

        btn = tk.Button(dialog, image=face_tk, command=lambda loc=(top, right, bottom, left): on_select(loc, img_np, label, crop_label,dialog))
        btn.image = face_tk
        btn.pack(side=tk.LEFT, padx=5, pady=5)


def on_select(face_location, img_np, label, crop_label, dialog):
    draw_face(img_np, face_location, label, crop_label)
    dialog.destroy()


# Function to open file dialog and display the image
def open_file(entry, label, crop_label, title):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.webp")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    if file_path:
        image = load_image(file_path)
        detect_and_draw_faces(image, label, crop_label, title)



# Function to handle URL input and display the image
def open_url(entry, label, crop_label, title):
    url = simpledialog.askstring("Input", "Enter image URL:")
    entry.delete(0, tk.END)
    entry.insert(0, url)
    if url:
        image = load_image(url)
        detect_and_draw_faces(image, label, crop_label, title)

# Function to compare faces and display the result
def compare_faces():
    img1_path = entry1.get()
    img2_path = entry2.get()

    if not img1_path or not img2_path:
        messagebox.showerror("Error", "Both image paths are required")
        return

    loading_label.pack()
    root.update_idletasks()

    def compare_thread():
        try:
            img1 = load_image(img1_path)
            img2 = load_image(img2_path)

            img1_np = np.array(img1)
            img2_np = np.array(img2)

            face_locations1 = face_recognition.face_locations(img1_np)
            face_locations2 = face_recognition.face_locations(img2_np)

            if not face_locations1 or not face_locations2:
                messagebox.showinfo("Comparison Result", "No face detected in one or both images.")
                return

            face_encodings1 = face_recognition.face_encodings(img1_np, face_locations1)
            face_encodings2 = face_recognition.face_encodings(img2_np, face_locations2)

            results = face_recognition.compare_faces(face_encodings1, face_encodings2[0], tolerance=0.6)
            if True in results:
                messagebox.showinfo("Comparison Result", "Is same person Probability: High")
            else:
                messagebox.showinfo("Comparison Result", "Is same person Probability: Low")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            loading_label.pack_forget()

    thread = Thread(target=compare_thread)
    thread.start()


# ------------------------------------------------------------------------------------Face_comparison

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#----------------------____________---------------00000--Main() <---------
root = tk.Tk()
root.title("Face Checker Tool v1.0")
root.geometry("1452x600")
root.configure(bg = "#FFFFFF")
root.iconbitmap(r's.ico')



# Create a canvas to add a scrollbar
canvas = tk.Canvas(root, bg='black')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a vertical scrollbar linked to the canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas
frame = tk.Frame(canvas, bg='black')
canvas.create_window((0, 0), window=frame, anchor="nw")

# Loading label
loading_label = Label(root, text="Loading...", fg='green', bg='black')

#00000000000000000000---IMPORTENT <---

img_label1 = tk.Label(frame, bg='black')
img_label1.grid(row=2, column=0, columnspan=3, pady=5)

crop_label1 = tk.Label(frame, bg='black')
crop_label1.grid(row=3, column=0, columnspan=3, pady=5)


img_label2 = tk.Label(frame, bg='black')
img_label2.grid(row=6, column=0, columnspan=3, pady=5)

crop_label2 = tk.Label(frame, bg='black')
crop_label2.grid(row=7, column=0, columnspan=3, pady=5)


canvas = Canvas(
    root,
    bg = "#FFFFFF",
    height = 600,
    width = 1452,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1452.0,
    600.0,
    fill="#1C2526",
    outline="")

canvas.create_text(
    591.0,
    299.0,
    anchor="nw",
    text="IMAGE INFO:",
    fill="#FFFFFF",
    font=("Poppins Medium", 18 * -1)
)

canvas.create_text(
    590.0,
    340.0,
    anchor="nw",
    text="Age",
    fill="#FFFFFF",
    font=("Poppins Regular", 16 * -1)
)

canvas.create_text(
    704.0,
    340.0,
    anchor="nw",
    text="---",
    fill="#FFFFFF",
    font=("Poppins Light", 16 * -1)
)

canvas.create_text(
    590.0,
    384.0,
    anchor="nw",
    text="Dimension:",
    fill="#FFFFFF",
    font=("Poppins Regular", 16 * -1)
)

canvas.create_text(
    704.0,
    384.0,
    anchor="nw",
    text="1366x768 px - 1366x768 px",
    fill="#FFFFFF",
    font=("Poppins Light", 16 * -1)
)

canvas.create_text(
    590.0,
    428.0,
    anchor="nw",
    text="Faces:",
    fill="#FFFFFF",
    font=("Poppins Regular", 16 * -1)
)

canvas.create_text(
    704.0,
    428.0,
    anchor="nw",
    text="1 person face detacted",
    fill="#FFFFFF",
    font=("Poppins Light", 16 * -1)
)

canvas.create_text(
    1037.0,
    299.0,
    anchor="nw",
    text="IMAGE INFO:",
    fill="#FFFFFF",
    font=("Poppins Medium", 18 * -1)
)

canvas.create_text(
    1036.0,
    340.0,
    anchor="nw",
    text="Age",
    fill="#FFFFFF",
    font=("Poppins Regular", 16 * -1)
)

canvas.create_text(
    1150.0,
    340.0,
    anchor="nw",
    text="---",
    fill="#FFFFFF",
    font=("Poppins Light", 16 * -1)
)

canvas.create_text(
    1036.0,
    384.0,
    anchor="nw",
    text="Dimension:",
    fill="#FFFFFF",
    font=("Poppins Regular", 16 * -1)
)

canvas.create_text(
    1150.0,
    384.0,
    anchor="nw",
    text="1366x768 px - 1366x768 px",
    fill="#FFFFFF",
    font=("Poppins Light", 16 * -1)
)

canvas.create_text(
    1036.0,
    428.0,
    anchor="nw",
    text="Faces:",
    fill="#FFFFFF",
    font=("Poppins Regular", 16 * -1)
)

canvas.create_text(
    1150.0,
    428.0,
    anchor="nw",
    text="1 person face detacted",
    fill="#FFFFFF",
    font=("Poppins Light", 16 * -1)
)

canvas.create_rectangle(
    580.0,
    68.0,
    960.0,
    272.0,
    fill="#000000",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    770.0,
    169.800048828125,
    image=image_image_1
)

canvas.create_rectangle(
    1026.0,
    68.0,
    1406.0,
    272.0,
    fill="#000000",
    outline="")

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    1216.0,
    169.800048828125,
    image=image_image_2
)

#-------------------------- GITHUB --------------------------------------

def open_github():
    url = "https://github.com/DevVj-1"
    webbrowser.open_new(url)
def open_Linkedin():
    url = "https://www.linkedin.com/in/dev-vj1/"
    webbrowser.open_new(url)
#------------------

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_github(),
    relief="flat"
)
button_1.place(
    x=40.0,
    y=68.0,
    width=121.0,
    height=35.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_Linkedin(),
    relief="flat"
)
button_2.place(
    x=181.0,
    y=68.0,
    width=121.0,
    height=35.0
)

canvas.create_text(
    256.0,
    349.0,
    anchor="nw",
    text="OR",
    fill="#FFFFFF",
    font=("Poppins Regular", 20 * -1)
)

canvas.create_text(
    40.0,
    256.0,
    anchor="nw",
    text="Search With 2 Image Url",
    fill="#FFFFFF",
    font=("Poppins Light", 16 * -1)
)

canvas.create_text(
    40.0,
    166.0,
    anchor="nw",
    text="Search With 1 Image Url",
    fill="#FFFFFF",
    font=("Poppins Light", 16 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_file(entry2, img_label2, crop_label2, title="image") ,
    relief="flat"
                              )
button_3.place(
    x=40.0,
    y=409.0,
    width=460.0,
    height=50.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_file(entry1, img_label1, crop_label1, title="image"),
    relief="flat"
)
button_4.place(
    x=40.0,
    y=482.0,
    width=460.0,
    height=50.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    726.0,
    576.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    1301.0,
    576.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    1365.0,
    576.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    1402.0,
    576.0,
    image=image_image_6
)
"""
image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(                     #girl face
    770.0,
    170.0,
    image=image_image_7

)
"""

#compare button
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=compare_faces,
    relief="flat"
)
button_5.place(
    x=907.0,
    y=478.0,
    width=180.0,
    height=50.0
)
"""
image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(               # girl face 2
    1216.0,
    170.0,
    image=image_image_8
)
"""
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    270.0,
    302.0,
    image=entry_image_1
)
entry1 = Entry(
    bd=0,
    bg="#202D2D",
    fg="#FFFFFF",
    highlightthickness=0


)
entry1.place(
    x=43.0,
    y=282.0,
    width=454.0,
    height=38.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    270.0,
    212.0,
    image=entry_image_2
)
entry2 = Entry(
    bd=0,
    bg="#202D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
entry2.place(
    x=43.0,
    y=192.0,
    width=454.0,
    height=38.0
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    726.0,
    24.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    1333.0,
    576.0,
    image=image_image_10
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_url(entry2, img_label2, crop_label2,title="url"),
    relief="flat"
)
button_6.place(
    x=510.0,
    y=197.0,
    width=32.0,
    height=31.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_url(entry1, img_label1, crop_label1,title="url"),
    relief="flat"
)
button_7.place(
    x=510.0,
    y=287.0,
    width=32.0,
    height=31.0
)



root.resizable(False, False)
root.mainloop()
