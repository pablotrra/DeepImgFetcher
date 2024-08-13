
# libraries Import
from tkinter import *
import customtkinter
from customtkinter import filedialog
import os

def obtain_subdirs(dir):
    subdirs = [dir_name for dir_name in os.listdir(dir) if os.path.isdir(os.path.join(dir, dir_name))]
    return subdirs

class GUI:

  def add_term(self, text="", curr_row=0):
    # Adds the entry buttom of the term
    term = customtkinter.CTkEntry(
      master=self.frame_terms,
      placeholder_text="",
      font=("Roboto", 14),
    )
    term.grid(pady=12, padx=10, row=curr_row, column=0)
    # Adds text to the entry (This only will happen when re-adding all terms at the delete_term
    # method)
    term.insert(0, text)
    term_delete = customtkinter.CTkButton(
      master=self.frame_terms,
      text="X",
      font=("Roboto", 14),
      command=lambda: self.delete_term(curr_row)
    )

    term_delete.grid(pady=12, padx=10, row=curr_row, column=1)

    self.term_objects.append((term, term_delete))

  def delete_term(self, del_row):
    print(f"Deleting {self.term_objects[del_row][0].get()}")
    # Remove specific term
    del self.term_objects[del_row]
    # Remove all terms from the grid
    widgets = self.frame_terms.winfo_children()
    for wid in widgets:
      wid.grid_remove()
    
    # Re-add all terms 
    # Copy all current terms
    curr_terms = self.term_objects.copy()
    # Delete list that holds all the terms, because the terms will be added again in
    # the add_term method.
    self.term_objects.clear()
    curr_row = 0
    for term in curr_terms:
      self.add_term(term[0].get(), curr_row=curr_row)
      curr_row += 1

  def delete_all_terms(self):
    for i in range(0, len(self.term_objects)):
      self.delete_term(i)

  def load_terms_from_dir(self):
    # Delete all terms
    self.delete_all_terms()
    dir = filedialog.askdirectory()



  def __init__(self):

    self.term_objects = []

    # Global appareance config

    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    # Main Window Properties

    self.root = customtkinter.CTk()
    self.root.title("Tkinter")
    self.root.geometry("700x500")

    # Allow expanding

    self.root.grid_columnconfigure(0, weight=1) # weight 0, dont expand, mantain size
    self.root.grid_columnconfigure(1, weight=3) # weight 1, it expands
    self.root.grid_rowconfigure(0, weight=1)
    # self.root.grid_rowconfigure(1, weight=1)

    current_text_font = ("Roboto", 14)

    self.frameLeft = customtkinter.CTkFrame(master=self.root)
    self.frameLeft.grid(pady=20, padx=20, row=0, column=0, sticky="nsew")

    self.frameRight = customtkinter.CTkFrame(master=self.root)
    self.frameRight.grid(pady=20, padx=20, row=0, column=1, sticky="nsew")

    frameDown = customtkinter.CTkFrame(master=self.root, fg_color="transparent")
    frameDown.grid(pady=5, padx=(10,10), row=1, column=0, columnspan=2, sticky="nsew")

    Label_id3 = customtkinter.CTkLabel(
        master=self.frameLeft,
        text="Directory with classes",
        font=current_text_font,

        )
    Label_id3.pack(pady=12, padx=10)

    classes_dir = customtkinter.CTkEntry(
        master=self.frameLeft,
        placeholder_text="",
        font=current_text_font,
        height=30,
        )
    classes_dir.pack(pady=12, padx=10, fill="x")

    # Right Panel

    self.frame_title = customtkinter.CTkFrame(master=self.frameRight, fg_color="transparent")
    self.frame_title.pack(pady=5, padx=10, fill="x")

    self.frame_terms = customtkinter.CTkScrollableFrame(master=self.frameRight, fg_color="transparent")
    self.frame_terms.pack(pady=5, padx=10, fill="x")

    self.frame_buttons = customtkinter.CTkFrame(master=self.frameRight, fg_color="transparent")
    self.frame_buttons.pack(pady=5, padx=10, fill="x", side="bottom")

    Label_id4 = customtkinter.CTkLabel(
        master=self.frame_title,
        text="Search Terms",
        font=("Roboto", 20),


        )
    Label_id4.pack(pady=10, padx=10)

    
    add_term_button = customtkinter.CTkButton(
        master=self.frame_buttons,
        text="Add term",
        font=("undefined", 14),
        command=lambda: self.add_term(curr_row=len(self.term_objects))
        )

    add_term_button.pack(pady=10, padx=10)

    load_from_dir_button = customtkinter.CTkButton(
        master=self.frame_buttons,
        text="Load terms from directory",
        font=("undefined", 14),
        command=self.load_terms_from_dir
        )

    load_from_dir_button.pack(pady=10, padx=10)

    destination_dir = customtkinter.CTkEntry(
        master=frameDown,
        placeholder_text="./scraps",
        font=current_text_font,

        )
    destination_dir.pack(padx=(5, 0), pady=(20, 20), side="left", fill="x", expand=True)

    begin_scrap = customtkinter.CTkButton(
        master=frameDown,
        text="Begin Scrap",
        font=("undefined", 14),
        hover=True,
        )
    begin_scrap.pack(padx=(5, 10), pady=(20, 20), side="right")

    #run the main loop
    self.root.mainloop()

app = GUI()