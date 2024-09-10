from DeepImgFetcher.scrap_model import scrap_page
from DeepImgFetcher.scrap_gui import GUI
import re
import threading
import os


class Controller:

    def __init__(self):
        # Initialize the GUI and pass controller reference
        self.view = GUI(self)

        self.terms = []
        self.add_terms = []
        self.common_add_terms = ""
        self.google_image_args = []
        self.image_number = 0
        # Run GUI loop
        self.view.run_gui()
        pass
    
    # Empty the scrap terms 
    def clear_terms(self):
        self.terms.clear()
        self.add_terms.clear()
        self.common_add_terms = ""
        self.google_image_args.clear()
        self.image_number = 0

    def get_terms(self):
        # Throw error if no terms are added
        if len(self.view.term_objects) == 0:
            self.view.show_error("No terms added")
            self.clear_terms()
            return False
        
        for term_line in self.view.term_objects:
            # term_line objects are like this (term, info of term, delete button)
            term_text = term_line[0].get()
            # Throw error if a term is empty
            if term_text == "":
                self.view.show_error("Terms cannot be empty")
                self.clear_terms()
                return False
            self.terms.append(term_text.replace(" ", "+"))
            self.add_terms.append(term_line[1].get().replace(" ", "+"))
        return True
    
    # Delete line breaks after the end of every line, emtpy lines and two or more spaces in a row
    def delete_line_break(self, text):
        return re.sub('\s+',' ', text).replace('\n', '')

    def get_common_info(self):
        # .get("0.0", "end") is for getting all the text
        common_text = self.view.add_info_entry.get("0.0", "end")
        # If textbox is empty, it has \n in its value. Ignore if textbox is empty
        if common_text == '\n':
            self.common_add_terms = ""
        else:
            self.common_add_terms = self.delete_line_break(common_text).replace(' ', '+')

        
        common_avoid_terms = self.view.avoid_info_entry.get("0.0", "end")
        if common_avoid_terms != '\n':
            common_avoid_terms = self.delete_line_break(common_avoid_terms).replace(' ', '+')
            self.google_image_args.append(f"&as_eq={common_avoid_terms}")

    def get_color_type(self):
        color = self.view.color_value.get()
        # Lower img_type value
        img_type = self.view.imgtype_value.get().lower()
        self.google_image_args.append(f"&tbs=ic:{color},itp:{img_type}")

    def get_image_number(self):
        image_num = self.view.image_number.get()
        if image_num == '':
            self.view.show_error("You have to specify a number of images to be scrapped")
            return False
        else:
            try:
                self.image_number = int(image_num)
            except:
                self.view.show_error("Error at converting number")
            return True

    def get_destination_dir(self):
        self.destination_dir = self.view.destination_dir.get()
        if not os.path.isdir(self.destination_dir):
            self.view.show_error("Destination folder does not exist")
            return False
        return True

    
    def init_scrap(self):
        terms_result = self.get_terms()
        if terms_result:
            image_result = self.get_image_number()
        self.get_common_info()
        self.get_color_type()
        valid_destination = self.get_destination_dir()
        if terms_result and image_result and valid_destination:
            print("terms", self.terms)
            print("add_terms", self.add_terms)
            print("common_add_terms", self.common_add_terms)
            print("google_image_args", self.google_image_args)
            print("destination_dir", self.destination_dir)
        
            self.view.show_scrapping_gui(self.terms)

            # Copying the terms because when deleting them later, the scrap_page method will not have access to them
            terms = self.terms.copy()
            common_add_terms = self.common_add_terms
            google_image_args = self.google_image_args.copy()

            # This terms are not a list so it isnt necessary to copy them. 
            add_terms = self.add_terms.copy()
            image_number = self.image_number
            destination_dir = self.destination_dir
            
            scrapController = ScrappingGUIController(self.view.scrapping_gui, True)
            thread = threading.Thread(target=scrap_page, args=(destination_dir, terms, common_add_terms, google_image_args, add_terms, image_number, scrapController))
            thread.start()

        self.clear_terms()
        pass
     
# This controller will manage interactions with the scrapping gui
class ScrappingGUIController:
    def __init__(self, scrapping_gui, draw_methods) -> None:
        self.scrapping_gui = scrapping_gui
        self.scrapping_gui.set_controller(self)
        self.scrapping_gui.set_cancel_button()
        self.draw_methods = draw_methods
        self.end_thread = False # If this flag is set, the thread will be stopped
    
    def advance_progress_bar(self):
        if self.draw_methods:
            self.scrapping_gui.next_dir()

    def add_text(self, msg):
        if self.draw_methods:
            self.scrapping_gui.add_text(msg)

    # This method will set the end flag to true. 
    def set_end_flag(self):
        self.add_text("Stopping scraping")
        self.end_thread = True

    def get_end_flag(self):
        return self.end_thread
    
    def finish_state(self):
        if self.end_thread:
            self.add_text("Scraping cancelled")
        self.scrapping_gui.change_button()