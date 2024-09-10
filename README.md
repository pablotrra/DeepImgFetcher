# DeepImgFetcher

Software that allows the massive download of images from Google, with the objective of starting or extending an image dataset for Deep Learning projects.

## Table of Contents

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Known Issues](#known-issues)

## Description

This software allows massive downloading of images from Google. The search terms to be downloaded can be entered manually or scanned from a folder. 

It also allows the configuration of each Google search, adding terms that will specify the search, types and colors of images, terms to avoid, etc.


## Installation

Instructions for setting up the project locally. Include steps to install dependencies and any specific requirements.

```bash
# Clone the repository
git clone https://github.com/pablotrra/DeepImgFetcher.git

# Navigate to the project directory
cd DeepImgFetcher
```

This software can be used without installing the dependencies (by executing the .exe) or by installing them and following the next instructions:

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the dependencies
pip install -r requirements.txt

# Execute the main.py file with python

python main.py
```

## Usage

In this project, each class or search term is called a *term*.

### Left panel

The options of the left panel are as follows:

- Number of images: The number of images that will be downloaded per term. This field is required.
- Common additional info: Additional info that will be added in EVERY Google search.
- Terms to avoid: Terms that will be avoided in EVERY Google Search.
- Image color: The color of the images in the Google search.
- Image type: The type of the images in the Google search.

### Right panel

In this panel, the search terms for downloading the images will be added.

To add a term manually click *Add term*. Two text entry boxes and a delete button will appear:

- Left text entry: The term.
- Rigth text entry: Additional info that will be added in the Google search of this term.
- Delete button: Delete this term.

To scan the terms from a directory click *Load terms from directory*, then navigate to the folder containing the folders with the term names and click *Select Folder*.

All terms can be deleted by clicking on the button with the trash bin to the right of the above mentioned buttons.

### Bottom panel

This panel manage the destination folder and the start of the scraping process.

You can type the destination folder manually using the text entry or select it using the button with the folder icon. 

Para empezar el proceso de scrapping, haz click en el botón *Begin Scraping*

## Known issues

- Some times adding too many terms with the scan button can be slow
- Some times removing too many terms with the button can be slow
- Linux compatibility has not been tested yet.


