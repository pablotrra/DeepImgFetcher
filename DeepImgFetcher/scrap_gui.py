
# libraries Import
import tkinter as tk
from tkinter import *
import customtkinter
from customtkinter import filedialog
# from tktooltip import ToolTip
from tkinter import messagebox

import os
from PIL import Image

from tools.common_methods import obtain_subdirs

CURRENT_TEXT_FONT = ("Roboto", 14)

def centerWindowToDisplay(Screen: customtkinter, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

class ToolTip:
    def __init__(self, widget, msg=""):
        self.widget = widget
        self.text = msg
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)
        widget.bind("<Motion>", self.move_tooltip)

    def show_tooltip(self, event):
        # Create tootlip window
        self.tooltip_window = tk.Toplevel(self.widget, background="grey")
        
        # self.tooltip_window = customtkinter.CTkToplevel(self.widget, fg_color="grey")
        self.tooltip_window.wm_overrideredirect(True)  # Delete window border
        
        # Tooltip label
        label = customtkinter.CTkLabel(self.tooltip_window, text=self.text, font=CURRENT_TEXT_FONT, bg_color="grey")
        label.pack(padx=5, pady=5)

        # Pos tooltip
        self.move_tooltip(event)

    def move_tooltip(self, event):
        if self.tooltip_window:
            # Move tooltip with mouse
            x = event.x_root + 20
            y = event.y_root + 10
            self.tooltip_window.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event):
        # Destroy tooltip if it exists
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

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
    self.term_objects.append((term, add_info_term, term_delete))
 
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
      self.term_objects[j][2].row = j


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

  def set_image_number(self):
    
    image_number_frame = customtkinter.CTkFrame(master=self.frameLeft, fg_color="transparent", width=250)
    image_number_frame.pack(pady=0, padx=20, fill="x", anchor="c")

    image_number_label = customtkinter.CTkLabel(
    master=image_number_frame,
    text="Number of images:",
    font=CURRENT_TEXT_FONT,
    )

    image_number_label.pack(pady=0, padx=10, side="left")
    # Only let the user write numbers
    def validate_numbers(text):
      if str.isdigit(text) or text == "":
        return True
      else:
        return False
    
    validation = image_number_frame.register(validate_numbers)

    self.image_number = customtkinter.CTkEntry(
        master=image_number_frame,
        placeholder_text="",
        font=CURRENT_TEXT_FONT,
        validate="key", # Validate every key pressed when this is focus
        validatecommand=(validation, '%P')
        )
    self.image_number.pack(padx=(5, 10), pady=(20, 20), side="left")

  def set_common_add_info(self):
    # Common additional info
    frame_add_info = customtkinter.CTkFrame(master=self.frameLeft, fg_color="transparent", width=250)
    frame_add_info.pack(pady=5, padx=20, fill="x")

    add_info_label = customtkinter.CTkLabel(
        master=frame_add_info,
        text="Common additional info",
        font=CURRENT_TEXT_FONT,
        )
    add_info_label.pack(pady=0, padx=10)

    self.add_info_entry = customtkinter.CTkTextbox(
        master=frame_add_info,
        font=CURRENT_TEXT_FONT,
        width=20, height=100
        )

    self.add_info_entry.pack(pady=5, padx=10, fill="x", expand=True)

    # Tooltip for info entry
    tooltip = ToolTip(self.add_info_entry, "Additional info that will be added in EVERY Google Search")

  def set_common_avoid_terms(self):
    # Common avoid info
    frame_avoid_info = customtkinter.CTkFrame(master=self.frameLeft, fg_color="transparent")
    frame_avoid_info.pack(pady=5, padx=20, fill="x")

    avoid_info_label = customtkinter.CTkLabel(
        master=frame_avoid_info,
        text="Terms to avoid",
        font=CURRENT_TEXT_FONT,
        )
    avoid_info_label.pack(pady=0, padx=10)

    self.avoid_info_entry = customtkinter.CTkTextbox(
        master=frame_avoid_info,
        font=CURRENT_TEXT_FONT,
        width=20, height=100
        )

    self.avoid_info_entry.pack(pady=5, padx=10, fill="x")

    # Tooltip for info entry
    ToolTip(self.avoid_info_entry, msg="Terms that will be avoided in EVERY Google Search")
  
  def set_color_info(self):
    # Color parameter
    frame_color_info = customtkinter.CTkFrame(master=self.frameLeft, fg_color="transparent")
    frame_color_info.pack(pady=5, padx=20)

    color_info_label = customtkinter.CTkLabel(
        master=frame_color_info,
        text="Image color",
        font=CURRENT_TEXT_FONT,
        )
    color_info_label.pack(pady=0, padx=10)

    self.color_value = customtkinter.StringVar(value="color")
    
    frame_radial_buttons = customtkinter.CTkFrame(master=frame_color_info)
    frame_radial_buttons.pack(expand=True, fill="both")

    color_radio = customtkinter.CTkRadioButton(frame_radial_buttons, text="Full Color", value="color", variable=self.color_value)
    gray_radio = customtkinter.CTkRadioButton(frame_radial_buttons, text="Black and white", value="gray", variable=self.color_value)
    trans_radio = customtkinter.CTkRadioButton(frame_radial_buttons, text="Transparent", value="trans", variable=self.color_value)

    color_radio.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    gray_radio.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    trans_radio.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    frame_radial_buttons.grid_columnconfigure((0, 1, 2), weight=1)

  def set_imgtype(self):

    frame_imgtype_info = customtkinter.CTkFrame(master=self.frameLeft, fg_color="transparent")
    frame_imgtype_info.pack(pady=5, padx=20, fill="x", anchor="c")
    # This needs to be converted to lowercase

    color_info_label = customtkinter.CTkLabel(
        master=frame_imgtype_info,
        text="Image type",
        font=CURRENT_TEXT_FONT,
        )
    color_info_label.pack(pady=0, padx=10, side="left")


    self.imgtype_value = customtkinter.StringVar(value="No type")
    imgtype_sel = customtkinter.CTkOptionMenu(frame_imgtype_info, values=[
                                                  "No type",
                                                  "Clipart", 
                                                  "Face",
                                                  "Lineart",
                                                  "Stock",
                                                  "Photo",
                                                  "Animated"],
                                         variable=self.imgtype_value)
    imgtype_sel.pack(pady=5, padx=2.5, side="left")
    
    # Tooltip for img type
    ToolTip(imgtype_sel, msg="No type No image type specified\nClipart Clipart-style images only\nFace Images of faces only\nLineart Line art images only\nStock Stock images only\nPhoto Photo images only\nAnimated Animated images only")

  def set_terms(self):
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
    
    bin_img_loc = Image.open("./DeepImgFetcher/assets/icons/trash_icon.png")

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

    # Tooltip for info entry
    ToolTip(delete_terms, msg="Delete all terms")
  
  def set_scrap_controls(self):
    self.destination_dir = customtkinter.CTkEntry(
        master=self.frameDown,
        # placeholder_text="./scraps",
        font=CURRENT_TEXT_FONT,
        )
    self.destination_dir.pack(padx=(5, 0), pady=(20, 20), side="left", fill="x", expand=True)
    self.destination_dir.insert(0, "./scraps")

    folder_img_loc = Image.open("./DeepImgFetcher/assets/icons/folder_icon.png")

    folder_img = customtkinter.CTkImage(light_image=folder_img_loc, dark_image=
                                    folder_img_loc)

    search_folder = customtkinter.CTkButton(
        master=self.frameDown,
        font=("undefined", 14),
        hover=True,
        image=folder_img,
        text="",
        width=10, height=10,
        command=self.set_destination_dir,
        )
    search_folder.pack(padx=(5, 0), pady=(20, 20), side="left")

    begin_scrap = customtkinter.CTkButton(
        master=self.frameDown,
        text="Begin Scraping",
        font=("undefined", 14),
        hover=True,
        command=self.controller.init_scrap
        )
    begin_scrap.pack(padx=(5, 10), pady=(20, 20), side="right")

  def show_error(self, msg):
    messagebox.showerror('Error', msg)

  def show_scrapping_gui(self, dirs):
    self.scrapping_gui = ScrapGUI(self.root, dirs)
    self.scrapping_gui.grab_set()  # Block the main window until the error window is closed

  

  def __init__(self, controller):
    
    # Set controller reference for calling methods
    self.controller = controller

    self.term_objects = []

    # Global appareance config

    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    # Main Window Properties

    self.root = customtkinter.CTk()
    self.root.title("Deep Image Fetcher")
    self.root.geometry("900x500")

    self.root.resizable(height=True, width=True)

    self.root.grid_columnconfigure(0, weight=1) # weight 0, dont expand, mantain size
    self.root.grid_columnconfigure(1, weight=3) # weight 1, it expands
    self.root.grid_rowconfigure(0, weight=1)
    # self.root.grid_rowconfigure(1, weight=1)


    # sticky = ns means fill the axis in the north and south direction. Width will be controlled with
    # the width parameter
    self.frameLeft = customtkinter.CTkScrollableFrame(master=self.root, width=300)
    self.frameLeft.grid(pady=20, padx=(10, 5), row=0, column=0, sticky="ns")

    self.set_image_number()
    self.set_common_add_info()
    self.set_common_avoid_terms()
    self.set_color_info()
    self.set_imgtype()

    self.frameRight = customtkinter.CTkFrame(master=self.root)
    self.frameRight.grid(pady=20, padx=(5, 10), row=0, column=1, sticky="nsew")

    self.frameDown = customtkinter.CTkFrame(master=self.root, fg_color="transparent")
    self.frameDown.grid(pady=5, padx=(10,10), row=1, column=0, columnspan=2, sticky="nsew")

    # Right Panel

    self.set_terms()
    self.set_scrap_controls()
    #run the main loop
    self.root.minsize(780, 450)

  # Start the GUI
  def run_gui(self):
    self.root.mainloop()
     
class ScrapGUI(customtkinter.CTkToplevel):
  def __init__(self, parent, dirs):
      super().__init__(parent)

      self.title("Scraping...")
      self.wm_overrideredirect(True)  # Delete window border

      self.geometry(centerWindowToDisplay(parent, 500, 400, parent._get_window_scaling()))
      self.resizable(False, False)

      # Create a frame to contain the widgets
      

      self.dirs = dirs

      self.num_dirs = len(dirs)
      self.current_dir = 0

      # self.tittle = customtkinter.CTkLabel(frame, text=f"Scrapping {dirs[self.current_dir - 1]}", font=("Roboto", 15))
      # self.tittle = customtkinter.CTkLabel(self.frame, text=f"Scrapping...", font=("Roboto", 20))
      # self.tittle.pack(pady=0)

      # Text

      text_frame = customtkinter.CTkFrame(self, bg_color="transparent")
      text_frame.pack(pady=(10, 10), padx=20, fill="x")

      self.TextBox = customtkinter.CTkTextbox(text_frame, font=CURRENT_TEXT_FONT)
      self.TextBox.insert(tk.END, "Initializing scraping")
      self.TextBox.pack(pady=10, padx=15, fill="both", expand="True")

      # Progress bar

      progress_frame = customtkinter.CTkFrame(self, fg_color="transparent")
      progress_frame.pack(pady=(10, 10), padx=20, fill="x")

      self.progress_bar = customtkinter.CTkProgressBar(progress_frame, orientation="horizontal",
        width=350,
        height=10,
        progress_color="blue",
        mode="determinate",
        indeterminate_speed=14
        )
      
      self.progress_bar.pack(pady=10, padx=15, fill="x", expand="True", side="left")
      self.progress_bar.set(0 / self.num_dirs)

      self.progress_label = customtkinter.CTkLabel(progress_frame,
                                                  text=f"0 / {self.num_dirs}")
      self.progress_label.pack(pady=10, padx=(0, 15), fill="x", side="left")

      # Cancel button

      cancel_frame = customtkinter.CTkFrame(self, fg_color="transparent")
      cancel_frame.pack(pady=(10, 20), padx=20, fill="x")
      
      self.button = customtkinter.CTkButton(cancel_frame,
                                        text="Cancel")
      self.button.pack(side="bottom")
    
  
  def next_dir(self):
    self.current_dir += 1
    # Manage progressing of the progress bar
    self.progress_bar.set(self.current_dir / self.num_dirs)
    self.progress_label.configure(text=f"{self.current_dir} / {self.num_dirs}")

  def add_text(self, msg):
    # Add message at the end
    self.TextBox.insert(tk.END, "\n" + msg)
    # Move scrollbar to the end
    self.TextBox.yview_moveto(1.0)

  def set_controller(self, controller):
    self.controller = controller
  
  # Set cancel button command to set the end flag to true
  def set_cancel_button(self):
    self.button.configure(command=self.controller.set_end_flag)
  
  def close_window(self):
    self.destroy()
  
  def change_button(self):
    self.button.configure(text="Done", command=self.close_window)