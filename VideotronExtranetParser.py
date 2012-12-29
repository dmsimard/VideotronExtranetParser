#!/usr/bin/python3 -tt
"""
VideotronExtranetParser.py, a (proof of concept) parser for extranet.videotron.com/services/secur/extranet/tpia/Usage.do
David Moreau Simard, moi@dmsimard.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import urllib.request
import re
import sys
from bs4 import BeautifulSoup

class VideotronExtranetParser():
  def __init__(self, url):
    self.url = url

    # Try to fetch our page and initialize our BeautifulSoup object.
    try:
      self.html = urllib.request.urlopen(self.url)
      self.soup = BeautifulSoup(self.html)
    except urllib.request.URLError as ex:
      print("Unable to retrieve information page: {0}".format(ex))
      sys.exit(1)

  def parse_summary_rows(self):
    # Summary format:
    # Date # mb_download # gb_download # mb_upload # gb_upload # mb_combined # gb_combined #

    # Identify a summary data row with the date cell
    pattern = re.compile("\d{4}-\d{2}-\d{2} to")
    date_cells = self.soup.findAll(text=pattern)

    # There are 7 cells in a summary information row.
    # Knowing this, assign each cell to a variable and fill a dictionary.
    # We'll return a list of dictionaries which correspond to each row of the table.
    data_rows = list()
    for td in date_cells:
      tr = td.parent.parent
      date, mb_download, gb_download, mb_upload, gb_upload, mb_combined, gb_combined = tr.findAllNext('td', limit=7)

      # We don't need the <br/> tag found in the date cell, remove it.
      date = [" " if str(element) == "<br/>" else element for element in date.contents]

      data_row_dict = {
        "date": ''.join(date),
        "mb_download": mb_download.text,
        "gb_download": gb_download.text,
        "mb_upload": mb_upload.text,
        "gb_upload": gb_upload.text,
        "mb_combined": mb_combined.text,
        "gb_combined": gb_combined.text
      }
      data_rows.append(data_row_dict)

    return data_rows

  def parse_detailed_rows(self):
    # Detailed format:
    # Date # kb_download # mb_download # kb_upload # mb_upload #

    # Identify a detailed data table row and return variables.
    # I'm happy with also catching summary rows and excluding them later
    pattern = re.compile("\d{4}-\d{2}-\d{2}")
    date_cells = self.soup.findAll(text=pattern)

    # There are 5 cells in a detailed information row.
    # Knowing this, assign each cell to a variable and fill a dictionary.
    # We'll return a list of dictionaries which correspond to each row of the table.
    data_rows = list()
    for td in date_cells:
      tr = td.parent.parent
      date, kb_download, mb_download, kb_upload, mb_upload = tr.findAllNext('td', limit=5)

      # Exclude summary rows
      if not re.search("to", str(date)):
        data_row_dict = {
            "date": date.text,
            "kb_download": kb_download.text,
            "mb_download": mb_download.text,
            "kb_upload": kb_upload.text,
            "mb_upload": mb_upload.text
        }
        data_rows.append(data_row_dict)

    return data_rows

url = "https://raw.github.com/dmsimard/VideotronExtranetParser/master/VideotronInternetUsage.html"
parser = VideotronExtranetParser(url)

summary_rows = parser.parse_summary_rows()
detailed_rows = parser.parse_detailed_rows()

for row in summary_rows + detailed_rows:
  print(row)