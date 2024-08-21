
# libraries Import
from tkinter import *
import customtkinter
from customtkinter import filedialog
import os
from PIL import Image

def obtain_subdirs(dir):
    subdirs = [dir_name for dir_name in os.listdir(dir) if os.path.isdir(os.path.join(dir, dir_name))]
    return subdirs

class GUI:

  def add_term(self, text="", curr_row=0):
    padx = 5
    pady = 10
    # Adds the entry buttom of the term
    term = customtkinter.CTkEntry(
      master=self.frame_terms,
      placeholder_text="",
      font=("Roboto", 14),
    )
    term.grid(pady=padx, padx=pady, row=curr_row, column=0)
    # Adds text to the entry (This only will happen when re-adding all terms at the delete_term_reloc
    # method)
    term.insert(0, text)

    # Adds the entry buttom of the term
    add_info_term = customtkinter.CTkEntry(
      master=self.frame_terms,
      placeholder_text="",
      font=("Roboto", 14),
    )
    add_info_term.grid(pady=padx, padx=pady, row=curr_row, column=1)


    term_delete = customtkinter.CTkButton(
      master=self.frame_terms,
      # text="X",
      image=self.bin_img,
      text="",
      font=("Roboto", 14),
      width=10, height=10,
      command=lambda: self.delete_term_reloc(term_delete)
    )

    # This property will determine the row the button will remove
    term_delete.row = curr_row
    term_delete.grid(pady=padx, padx=pady, row=curr_row, column=2)
    self.term_objects.append((term, term_delete))
 
  def add_mul_terms(self, terms):
    # Add multiple terms. This function is a little slow, improve it.
    # terms: list of strings. Terms to add, strings will be used in the term entry
    for i in range(0, len(terms)):
      self.add_term(terms[i], i)

  def _delete_term(self, row):
    # Manage the removing of all the terms in that row
    # row: int. Number of the row that will be deleted

    # Remove specific term
    del self.term_objects[row]
    widgets = self.frame_terms.winfo_children()
    # Delete the specific widgets. One term is composed of 3 widgets (2 entry and 1 button)
    # IMPORTANT: If you delete widgets in a grid, first use grid_remove and then delete it
    for _ in range(row * 3, row * 3 + 3):
      # When one element is removed, the next one will have the index of the one that
      # was removed
      del_row = row * 3
      widgets[del_row].grid_remove() # Remove it from the grid
      # Delete it from being the master frame child. For some reason, this will not be
      # updated in the variable widgets
      widgets[del_row].destroy() 
      # Delete the widget from the variable widgets
      del widgets[del_row]

  
  def delete_term_reloc(self, button):
    # Delete the term that corresponds to the same row of the button that was clicked and
    # reconfigure the delete buttons of the next rows. 
    del_row = button.row
    # # Remove specific term
    self._delete_term(del_row)
    # Now we have to reconfigure the lambda in the command property of the widgets that come nex to ours
    for j in range(del_row, len(self.term_objects)):
      self.term_objects[j][1].row = j


  def delete_all_terms(self):
    terms_to_delete = len(self.term_objects)
    for _ in range(terms_to_delete):
      # Remember that every time you delete a term, the list has n - 1. So, delete the first x
      # times
      self._delete_term(0)

  def load_terms_from_dir(self):
    dir = filedialog.askdirectory()
    # If user select a dir (will do nothing if user select "Cancel")
    if dir:
      # Delete all terms
      self.delete_all_terms()
      if not os.path.isdir(dir):
          print(f"Error: Folder '{dir}' don't exists or can't be located.")
      else:
        sub_dirs = obtain_subdirs(dir)
        sub_dirs.sort()
        self.add_mul_terms(sub_dirs)

  def set_destination_dir(self):
    dir = filedialog.askdirectory()
    if dir:
      current_text = self.destination_dir.get()
      self.destination_dir.delete(0, len(current_text))
      self.destination_dir.insert(0, dir)

  def __init__(self):

    self.term_objects = []

    # Global appareance config

    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    # Main Window Properties

    self.root = customtkinter.CTk()
    self.root.title("Tkinter")
    self.root.geometry("900x500")

    self.root.resizable(height=True, width=True)

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

    # Right Panel

    self.frame_title = customtkinter.CTkFrame(master=self.frameRight, fg_color="transparent")
    self.frame_title.pack(pady=5, padx=10, fill="x")

    self.frame_terms = customtkinter.CTkScrollableFrame(master=self.frameRight, fg_color="transparent")
    self.frame_terms.pack(pady=0, padx=5, fill="both", expand=True)

    self.frame_buttons = customtkinter.CTkFrame(master=self.frameRight, fg_color="transparent")
    self.frame_buttons.pack(pady=0, padx=10, side="bottom", anchor="c")

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


    load_from_dir_button = customtkinter.CTkButton(
        master=self.frame_buttons,
        text="Load terms from directory",
        font=("undefined", 14),
        command=self.load_terms_from_dir
        )
    
    bin_img_loc = Image.open("./icons/trash_icon.png")

    self.bin_img = customtkinter.CTkImage(light_image=bin_img_loc, dark_image=
                                    bin_img_loc)
    delete_terms = customtkinter.CTkButton(
        master=self.frame_buttons,
        image=self.bin_img,
        text="",
        width=10, height=10,
        font=("undefined", 14),
        command=self.delete_all_terms
        )

    add_term_button.pack(pady=10, padx=10, side="left")
    load_from_dir_button.pack(pady=10, padx=10, side="left")
    delete_terms.pack(pady=10, padx=10, side="left")

    self.destination_dir = customtkinter.CTkEntry(
        master=frameDown,
        # placeholder_text="./scraps",
        font=current_text_font,
        )
    self.destination_dir.pack(padx=(5, 0), pady=(20, 20), side="left", fill="x", expand=True)
    self.destination_dir.insert(0, "./scraps")

    folder_img_loc = Image.open("./icons/folder_icon.png")

    folder_img = customtkinter.CTkImage(light_image=folder_img_loc, dark_image=
                                    folder_img_loc)

    search_folder = customtkinter.CTkButton(
        master=frameDown,
        font=("undefined", 14),
        hover=True,
        image=folder_img,
        text="",
        width=10, height=10,
        command=self.set_destination_dir,
        )
    search_folder.pack(padx=(5, 10), pady=(20, 20), side="left")

    begin_scrap = customtkinter.CTkButton(
        master=frameDown,
        text="Begin Scraping",
        font=("undefined", 14),
        hover=True,
        )
    begin_scrap.pack(padx=(5, 10), pady=(20, 20), side="right")

    #run the main loop
    self.root.mainloop()

app = GUI()