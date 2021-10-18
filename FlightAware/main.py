# This is a sample Python script.
import html_to_json
import requests
from bs4 import BeautifulSoup

#Von der Flightaware-Seite wird der HTML Code als Variable dargestellt
result = requests.get("https://de.flightaware.com/live/airport/EDDF/departures")
src = result.content

soup = BeautifulSoup(src)



for link in soup.findAll('a'):
    #print(link.get('href'))
    a = str(link.get('href'))
    # Für jeden Link, der auf die Flugnummer zeigt, werden die geplante Ankuftszeit und die tatsächliche Ankunftszeit angegeben
    if 'live/flight/id' in a :
        #print(a)
        detail = 'https://de.flightaware.com/' + a
        detailResult = requests.get(detail)
        detailSrc = detailResult.content

        detailSoup = BeautifulSoup(detailSrc)
        #print(detailSoup)
        detailString = str(detailSoup)
        pos1 = detailString.find('flightPageDataTimesParent', 0)
        pos2 = detailString.find('flightPageDataTableContainer', 0)
        detailWithoutTop = detailString[pos1:]
        detailX = detailWithoutTop[:pos2]
        print(detailX)
        print(a)


#Von der Übersichts-Seite wird der HTML Code der Tabelle eingelesen und in ein JSON umgewandelt
text = str(soup)

posStart = text.find('<table class="prettyTable fullWidth" style="background-color: white;">', 0)


withoutTop = text[posStart:]

posEnd = withoutTop.find('<span style="font-size: x-small">', 0)
html = withoutTop[:posEnd]

html_string = """<head>
    <title>Test site</title>
    <meta charset="UTF-8"></head>"""
output_json = html_to_json.convert(html)
#print(output_json)
