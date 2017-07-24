import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.Trolley.table tr")  # selects all <tr> blocks within <table class="Trolley table">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Date'] = table_cells[0].text_content()
            record['Hospital'] = table_cells[1].text_content()
            record['Region'] = table_cells[2].text_content()
            record['Trolley total'] = table_cells[3].text_content()
            record['Sales m'] = table_cells[4].text_content()
            table_cellsurls = table_cells[1].cssselect("a")
            record['HospitalURL'] = table_cellsurls[1].attrib.get('href')

            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Hospital"], record)
                            
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #next_link = root.cssselect("a.next")
    #print next_link
    #if next_link:
        #next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        #print next_url
        #scrape_and_look_for_next_link(next_url)
    

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
#base_url = 'http://inmo.ie/6022'
starting_url = 'http://inmo.ie/6022'
scrape_and_look_for_next_link(starting_url)
