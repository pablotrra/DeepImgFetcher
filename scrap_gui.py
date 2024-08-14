
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
    # Adds text to the entry (This only will happen when re-adding all terms at the delete_term
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
      text="X",
      font=("Roboto", 14),
      command=lambda: self.delete_term(curr_row)
    )

    term_delete.grid(pady=padx, padx=pady, row=curr_row, column=2)

    self.term_objects.append((term, term_delete))
 
  def add_mul_terms(self, terms):
    # Add multiple terms
    # terms: list of strings. Terms to add, strings will be used in the term entry
    for i in range(0, len(terms)):
      self.add_term(terms[i], i)

  def delete_term(self, del_row):
    print(f"Deleting at {del_row}")
    # Remove specific term
    del self.term_objects[del_row]
    # Get all term widgets
    widgets = self.frame_terms.winfo_children()
    # Delete the specific widgets. One term is composed of 3 widgets (2 entry and 1 button)
    # IMPORTANT: If you delete widgets in a grid, the other widgets re-allocate accordingly
    widgets[del_row * 3].grid_remove()
    widgets[del_row * 3 + 1].grid_remove()
    widgets[del_row * 3 + 2].grid_remove()
    # Now we have to reconfigure the lambda in the command property of the widgets that come nex to ours
    del_row_sum = 0
    for i in range(del_row * 3 + 2, len(widgets), 3):
      print(widgets[i])
      print(del_row + del_row_sum)
      widgets[i].configure(command=lambda: self.delete_term(del_row + del_row_sum))
      del_row_sum += 1


  def delete_all_terms(self):
    # Something inside this is VERY SLOW. FIX
    curr_terms = self.term_objects.copy()

    # Delete x times (where x is 0 to len(self.term_objects))
    for _ in range(0, len(curr_terms)):
      # Remember that every time you delete a term, the list has n - 1. So, delete the first x
      # times
      self.delete_term(0)
    print("Deleted all terms")

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

    add_term_button.pack(pady=10, padx=10, side="left")
    load_from_dir_button.pack(pady=10, padx=10, side="left")

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