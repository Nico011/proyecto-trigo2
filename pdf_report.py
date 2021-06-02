# -*- coding: utf-8 -*-
"""
Code from:

https://towardsdatascience.com/how-to-create-pdf-reports-with-python-the-essential-guide-c08dd3ebf2ee
"""

from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    # def header(self):
    #     # Custom logo and positioning
    #     # Create an `assets` folder and put any wide and short image inside
    #     # Name the image `logo.png`
    #     self.image('assets/logo.png', 10, 8, 33)
    #     self.set_font('Arial', 'B', 11)
    #     self.cell(self.WIDTH - 80)
    #     self.cell(60, 1, 'Sales report', 0, 0, 'R')
    #     self.ln(20)
        
    # def footer(self):
    #     # Page numbers in the footer
    #     self.set_y(-15)
    #     self.set_font('Arial', 'I', 8)
    #     self.set_text_color(128)
    #     self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, images):
        # Determine how many plots there are per page and set positions
        # and margins accordingly
        if len(images) == 3:
            self.i
            self.image(images[0], 15, 25, self.WIDTH - 30, 100)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30, 100)
            self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30, 100)
        elif len(images) == 2:
            self.image(images[0], 15, 25, self.WIDTH - 30, 110)
            self.image(images[1], 15, self.WIDTH / 2 + 45, self.WIDTH - 30, 110)
        else:
            self.image(images[0], 15, 25, self.WIDTH - 30, 100)
            
    def print_page(self, images):
        # Generates the report
        self.add_page()
        self.page_body(images)