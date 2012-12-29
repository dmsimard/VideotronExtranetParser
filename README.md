#VideotronExtranetParser.py#

##ABOUT
A parser for a public videotron extranet page showing a customer's current and monthly usage.

The parser for the time being is a proof of concept that parses the page and returns dictionaries with parsed data.

##LICENSE
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

##REQUIREMENTS
- Python3 (tested under Python 3.2.3)
- BeautifulSoup (bs4)

##USAGE
- Provide a valid URL that leads to a Videotron Extranet Internet Usage page, like so:

    ```python
    url = "https://extranet.videotron.com/services/secur/extranet/tpia/Usage.do?lang=ENGLISH&compteInternet=vlusername"
    parser = VideotronExtranetParser(url)
    ```

- Call parse_summary_rows to obtain parsed summary billing period information rows

    ```python
    summary_rows = parser.parse_summary_rows()
    for row in summary_rows:
      print(row)
    >>> {'gb_combined': '75.23',
      'mb_combined': '77038.27',
      'mb_download': '65504.84',
      'gb_upload': '11.26',
      'mb_upload': '11533.43',
      'date': '2012-11-21 to 2012-12-20',
      'gb_download': '63.97'}
      ```

- Call parse_detailed_rows to obtain parsed detailed daily information rows

    ```python
    detailed_rows = parser.parse_detailed_rows()
    for row in detailed_rows:
      print(row)
    >>> {'date': '2012-12-21',
    'mb_upload': '65.51',
    'mb_download': '234.93',
    'kb_upload': '67082',
    'kb_download': '240572'}
    ```
