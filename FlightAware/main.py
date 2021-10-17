# This is a sample Python script.
import html_to_json
import requests
from bs4 import BeautifulSoup

result = requests.get("https://de.flightaware.com/live/airport/EDDF/departures")
src = result.content

soup = BeautifulSoup(src)

body = soup.find('<table class="prettyTable fullWidth" style="background-color: white;">')



text = str(soup)

posStart = text.find('<table class="prettyTable fullWidth" style="background-color: white;">', 0)

withoutTop = text[posStart:]

posEnd = withoutTop.find('<span style="font-size: x-small">', 0)
html = withoutTop[:posEnd]

html_string = """<head>
    <title>Test site</title>
    <meta charset="UTF-8"></head>"""
output_json = html_to_json.convert(html)
print(output_json)
