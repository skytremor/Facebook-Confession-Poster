# Facebook Confession Poster

Automatically post data from a given spreadsheet to a facebook page's newsfeed that is under the administration of the user.

* Utilizes google spreadsheet api ([gspread](https://github.com/burnash/gspread)) and facebook api.

# Basic usage
<ol>
<li> Obtain OAuth2 credentials from the <a href="https://console.developers.google.com/" title="Title">
Google Developers Console</a>. </li>
<li> Move .json file acquired from GDC in the same folder as confession_poster.py </li>
<li> Enter google spreadsheet scope following line (where the sheet resides): </li>
</ol>
```
scope = ['https://spreadsheets.google.com/feeds']
```
<ol start="4">
<li> Enter the name of the google sheet page from where the confessions will be fetched, in the following line: </li>
</ol>
```
wks = gc.open("MY_SHEET_NAME").sheet1
```
<ol start="5">
<li> Acquire <a href="http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages" title="Title"> facebook credentials</a> for the page and enter them here:
</li>
</ol>
```
cfg = {
    "page_id"      : "Enter the pages' id", 
    "access_token" : "Enter your access token here."
    }
```

<ol start="6"> <li> Modify the following variables to fit your needs: </li> </ol>

* Sleep Amount - Time between posts to the page
* First Cell - Everytime you run the script, you must mark the row from which the program begins to read.
* Column of data - Column that corresponds to the confession or data desired to post.
* Column of time - Gspreadsheet timestamps all input into the sheet automatically, select the column that corresponds to such.


