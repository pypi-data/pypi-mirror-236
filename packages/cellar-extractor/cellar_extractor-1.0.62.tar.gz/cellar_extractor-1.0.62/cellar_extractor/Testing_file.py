"""

This file is purely a testing file for trying out separate parts of code, testing if everything works and such.
Can be also used to develop future code.



"""

from nodes_and_edges import get_nodes_and_edges
from os.path import join
from json_to_csv import read_csv
import time
from eurlex_scraping import *
from cellar import *
from sparql import *




if __name__ == '__main__':
   celex = "61969CJ0006"
   site = get_html_text_by_celex_id(celex)
   text = get_full_text_from_html(site)
   operative = get_operative_part(text)
   print(operative)
   data, json = get_cellar_extra(sd='2022-01-01',ed="2022-03-03",max_ecli=2000,save_file='n')

   b=2
