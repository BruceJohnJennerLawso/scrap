from lxml import html
import requests

page = requests.get('http://strobe.uwaterloo.ca/athletics/intramurals/teams.php?team=12348&sport=1')
tree = html.fromstring(page.content)
