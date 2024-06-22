"""
Project developed under Gurugram Police Cyber Security GPCSSI Program, June 2024, by Dev Vijay ,cyber warrior (CW-129)
"""
"""
#For Windows
##########################################################
You can run this script by writing " python .\face_comparison_tool.py "
##########################################################
"""

import tkinter as tk
from tkinter import filedialog, messagebox, Label, Toplevel, simpledialog
from PIL import Image, ImageTk
import face_recognition
import webbrowser
import numpy as np
import requests
from io import BytesIO
from threading import Thread
import cv2


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
    img_with_face.thumbnail((130, 130))  #small face
    img_tk_face = ImageTk.PhotoImage(img_with_face)
    crop_label.config(image=img_tk_face)
    crop_label.image = img_tk_face

    img_with_boxes = Image.fromarray(img_with_boxes)
    img_with_boxes.thumbnail((290, 290)) #big face
    img_tk = ImageTk.PhotoImage(img_with_boxes)
    label.config(image=img_tk)
    label.image = img_tk


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

        btn = tk.Button(dialog, image=face_tk,
                        command=lambda loc=(top, right, bottom, left): on_select(loc, img_np, label, crop_label,
                                                                                 dialog))
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
    """
#---------------------------------------------------------------------------

            if not face_encodings1 or not face_encodings2:
                messagebox.showinfo("Comparison Result", "No face encodings found in one or both images.")
                return
        # Calculate the face distance
            distances = face_recognition.face_distance(face_encodings1, face_encodings2[0])

        # Calculate the similarity probability (1 - distance)
            probabilities = 1 - distances

        # Determine the highest probability
            max_probability = max(probabilities)

        # Convert probability to percentage
            percentage = max_probability * 100

        # Determine the category
            if max_probability < 0.50:
                category = "low"
            elif max_probability < 0.75:
                category = "medium"
            else:
                category = "high"

        # Show the result in a messagebox
            if category == "low":
                messagebox.showinfo("Comparison Result", f"Is same person Probability: {percentage:.2f}% ({category})")
            elif category == "medium":
                messagebox.showinfo("Comparison Result", f"Is same person Probability: {percentage:.2f}% ({category})")
            else:
                messagebox.showinfo("Comparison Result", f"Is same person Probability: {percentage:.2f}% ({category})")
        except Exception as e:(
            messagebox.showerror("Error", str(e)))
        finally:
            loading_label.pack_forget()
#---------------------------------------------------------------------------
"""
# Create main application window ---------------------------------------------
root = tk.Tk()
root.title("Face Checker Tool")
root.configure(bg='black')
root.geometry("1452x600")
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

# Create and place widgets with the new design
label1 = tk.Label(frame, text="First Image", fg='white', bg='black', font=("Helvetica", 14, "bold"))
label1.grid(row=0, column=0, sticky="w", pady=10, padx=10)

entry1 = tk.Entry(frame, width=50, fg='white', bg='black', insertbackground='white', font=("Helvetica", 12))
entry1.grid(row=1, column=0, padx=10, pady=5)

button1_file = tk.Button(frame, text="Select Image", command=lambda: open_file(entry1, img_label1, crop_label1, "Select Face from First Image"), fg='white', bg='#333333', activebackground='green', font=("Helvetica", 12))
button1_file.grid(row=1, column=1, padx=10, pady=5)

button1_url = tk.Button(frame, text="From URL", command=lambda: open_url(entry1, img_label1, crop_label1, "Select Face from First Image"), fg='white', bg='#333333', activebackground='green', font=("Helvetica", 12))
button1_url.grid(row=1, column=2, padx=10, pady=5)

img_label1 = tk.Label(frame, bg='black')
img_label1.grid(row=2, column=0, columnspan=3, pady=5)

crop_label1 = tk.Label(frame, bg='black')
crop_label1.grid(row=3, column=0, columnspan=3, pady=5)

label2 = tk.Label(frame, text="Second Image", fg='white', bg='black', font=("Helvetica", 14, "bold"))
#label2.grid(row=4, column=0, sticky="w", pady=10, padx=10)
label2.grid(row=0, column=4, sticky="w", pady=10, padx=10)

entry2 = tk.Entry(frame, width=50, fg='white', bg='black', insertbackground='white', font=("Helvetica", 12))
#entry2.grid(row=5, column=0, padx=10, pady=5)
entry2.grid(row=1, column=4, padx=10, pady=5)

button2_file = tk.Button(frame, text="Select Image", command=lambda: open_file(entry2, img_label2, crop_label2, "Select Face from Second Image"), fg='white', bg='#333333', activebackground='green', font=("Helvetica", 12))
button2_file.grid(row=1, column=5, padx=10, pady=5)

button2_url = tk.Button(frame, text="From URL", command=lambda: open_url(entry2, img_label2, crop_label2, "Select Face from Second Image"), fg='white', bg='#333333', activebackground='green', font=("Helvetica", 12))
button2_url.grid(row=1, column=7, padx=10, pady=5)

img_label2 = tk.Label(frame, bg='black')
img_label2.grid(row=2, column=3, columnspan=3, pady=5)

crop_label2 = tk.Label(frame, bg='black')
crop_label2.grid(row=3, column=4, columnspan=3, pady=5)

compare_button = tk.Button(frame, text="Compare Faces", command=compare_faces, fg='white', bg='#333333', activebackground='green', font=("Helvetica", 12, "bold"))
compare_button.grid(row=15, column=2, columnspan=1, pady=20)

#-------------------------- GITHUB --------------------------------------

def open_github():
    url = "https://github.com/DevVj-1"
    webbrowser.open_new(url)

github_button = tk.Button(frame, text="GitHub", command=open_github)
github_button.grid(row=16, column=2, columnspan=1, pady=20)

#------------------

# Update the scroll region to match the size of the frame
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
# Run the application
root.mainloop()
