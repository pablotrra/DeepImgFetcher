import argparse
import os
import sys
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup
import requests

GOOGLE_IMG_XPATH = '//*[@id="search"]//div[@style]/g-img/img'
GOOGLE_SLCT_IMG_XPATH = '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]'
CLOSE_SLCT_IMG_XPATH = '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div//*[@jsaction="trigger.Hqc3Od"]'
TOTAL_IMAGES = 1000

def obtain_subdirs(dir):
    subdirs = [dir_name for dir_name in os.listdir(dir) if os.path.isdir(os.path.join(dir, dir_name))]
    return subdirs

def download_image(url, save_path):
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)



def main():
    parser = argparse.ArgumentParser(description="Script that scrapes google images using the names of each of the subfolders \
                                    within the specified directory. Once this is done, it will download the images and place \
                                    them inside each folder.")
    parser.add_argument('main_dir', type=str, help='Folder path')
    parser.add_argument('-a', '--add', type=str, help='Additional info for the search', nargs='*')
    args = parser.parse_args()

    # Check if the folder exists
    if not os.path.isdir(args.main_dir):
        print(f"Error: Folder '{args.main_dir}' don't exists or can't be located.")
        sys.exit(1)

    print(f"Folder '{args.main_dir}' has been provided and is valid.")

    # Additional info that will be used in the google search
    add_info = ''
    if args.add:
        add_info = " ".join(args.add)
        print(f"Additional info: {add_info}")


    sub_dirs = obtain_subdirs(args.main_dir)
    print(sub_dirs)
    
    google_image_arguments = [
        # "isz:lt,", 
        # "islt:4mp,",
        # "sur:fmc,", 
        "imgc=color,", # Full color images 
        "&imgtype=photo," # Real Photos
        "&as_eq=draw+dibujo+cartoon+people+person+man+boy+girl+woman+kid+lunch+animal+sweet+cookie,", # Terms to avoid in the search

    ]
    scrap_page(sub_dirs, add_info, google_image_arguments)

# Gets the image ref, pass it to the download method
def manage_image(curr_images, img, driver, og_dir_name, x_path):
    curr_images[img].click()
    time.sleep(0.05)
    full_img = driver.find_element(By.XPATH, GOOGLE_SLCT_IMG_XPATH)
    download_image(full_img.get_attribute("src"), (f'scraps/{og_dir_name}/scrap_{img}.jpg'))
    # Close selected image. This part is only needed when not in full screen. Can save time if browser is started in full screen
    # driver.find_element(By.XPATH, CLOSE_SLCT_IMG_XPATH).click()
    # time.sleep(0.2)

def scrap_page(dirs, add_info, img_args):

    # Options for the browser

    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("start-maximized")

    # Patch for current version of ChromeDriver. See https://stackoverflow.com/questions/78796828/i-got-this-error-oserror-winerror-193-1-is-not-a-valid-win32-application
    
    chrome_install = ChromeDriverManager().install()

    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")

    service = ChromeService(chromedriver_path)

    # Initialize Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)


    for dir_name in dirs:
        if not os.path.isdir(f'scraps/{dir_name}'):
            os.makedirs(f'scraps/{dir_name}')
        og_dir_name = dir_name
        # if dir_name != "Carrot":
        #     continue
        dir_name = dir_name.replace("_", " ")

        print(f"Now searching for {dir_name}")
        url = f"https://www.google.com/search?as_q={dir_name}+{add_info}&tbs={''.join(img_args)}&udm=2"
        print(f"URL to use: {url}")
        
        driver.get(url)

        
        try:
          # Accept cache
          cache_acpt = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]")
          cache_acpt.click()

        except NoSuchElementException:
            print("No cache in this page")

        finally:

          curr_images = driver.find_elements(By.XPATH, GOOGLE_IMG_XPATH)
          curr_images_len = len(curr_images)

          last_height = driver.execute_script('\
          return document.body.scrollHeight')
      
          while True:
              driver.execute_script('\
              window.scrollTo(0,document.body.scrollHeight)')
      
              # waiting for the results to load
              time.sleep(3)
      
              new_height = driver.execute_script('\
              return document.body.scrollHeight')

              curr_images = driver.find_elements(By.XPATH, GOOGLE_IMG_XPATH)
              curr_images_len = len(curr_images)
              # checking if we have reached the bottom of the page
              if curr_images_len >= TOTAL_IMAGES or new_height == last_height:
                  # Scroll to the top of the search to avoid "click intercepted by other element" errors
                  driver.execute_script('\
                  window.scrollTo(0,0)')
                  # Download each image.
                  curr_images_len = min(curr_images_len, TOTAL_IMAGES)
                  print(f'Images to download: {curr_images_len}')
                #   print(curr_images[-1].get_attribute('outerHTML'))
                  for img in range(0, curr_images_len):
                      # ./IMGS/{dir}/
                      try: 
                        manage_image(curr_images, img, driver, og_dir_name, GOOGLE_SLCT_IMG_XPATH)
                      # Sometimes google creates empty imgs at the end. Discard them.
                      except ElementNotInteractableException:
                          print("Empty elements found, finishing early.")
                          break
                      # Some images have a different xpath. Discard them.
                      except selenium.common.exceptions.NoSuchElementException as e:
                          continue
                  break
      
              last_height = new_height

    driver.quit()

if __name__ == '__main__':
    main()
