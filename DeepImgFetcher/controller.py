from DeepImgFetcher.scrap_model import scrap_page
from DeepImgFetcher.scrap_gui import GUI
import re


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

    def advance_progress_bar(self):
        self.view.next_dir()

    def init_scrap(self):
        terms_result = self.get_terms()
        if terms_result:
            image_result = self.get_image_number()
        self.get_common_info()
        self.get_color_type()
        if terms_result and image_result:
            print("terms", self.terms)
            print("add_terms", self.add_terms)
            print("common_add_terms", self.common_add_terms)
            print("google_image_args", self.google_image_args)
        
            self.view.show_scrapping_gui(self.terms)
            scrap_page(self.terms, self.common_add_terms, self.google_image_args, self.add_terms, self.image_number, self.advance_progress_bar)

        self.clear_terms()
        pass
     