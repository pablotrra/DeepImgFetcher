from DeepImgFetcher.scrap_model import scrap_page
from DeepImgFetcher.scrap_gui import GUI
import re


class Controller:

    def __init__(self):
        self.view = GUI(self)
        self.terms = []
        self.add_terms = []
        self.common_add_terms = ""
        self.google_image_args = []
        self.view.run_gui()
        pass
    
    def clear_terms(self):
        self.terms.clear()
        self.add_terms.clear()
        self.common_add_terms = ""
        self.google_image_args.clear()

    def get_terms(self):
        for term_line in self.view.term_objects:
            term_text = term_line[0].get()
            if term_text == "":
                self.view.show_error("Terms cannot be empty")
                self.clear_terms()
                return False
            self.terms.append(term_text.replace(" ", "+"))
            self.add_terms.append(term_line[1].get().replace(" ", "+"))
        return True
    
    def get_common_info(self):
        common_text = self.view.add_info_entry.get("0.0", "end")
        if common_text == '\n':
            self.common_add_terms = ""
        else:
            common_text = re.sub('\s+',' ', common_text)
            print(f"After re.sub {common_text}")
            self.common_add_terms = common_text.replace('\n', '').replace(' ', '+')

        # Poner lo mismo en el avoid
        common_avoid_terms = self.view.avoid_info_entry.get("0.0", "end")
        if common_avoid_terms != '\n':
            self.google_image_args.append(f"&as_eq={common_avoid_terms.replace(' ', '+')}")

    def get_color_type(self):
        color = self.view.color_value.get()
        img_type = self.view.imgtype_value.get().lower()
        self.google_image_args.append(f"&tbs=ic:{color},itp:{img_type}")

    def init_scrap(self):
        result = self.get_terms()
        self.get_common_info()
        self.get_color_type()
        if result:
            print("terms", self.terms)
            print("add_terms", self.add_terms)
            print("common_add_terms", self.common_add_terms)
            print("google_image_args", self.google_image_args)
        # scrap_page(dirs=self.terms, add_info_by_search=self.add_terms)
        self.clear_terms()
        pass