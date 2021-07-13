from bs4 import BeautifulSoup as bs
import urllib.request
import csv
import re
from collections import Counter

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

url = 'https://genius.com/Mac-miller-self-care-lyrics'
headers = {'User-Agent': user_agent,}
request = urllib.request.Request(url, None, headers)
response = urllib.request.urlopen(request)
soup = bs(response, 'html.parser')
p_tag = soup.p
text = p_tag.get_text()
text = re.sub(r'\[.*\]', '', text)
text = re.sub('[\n]', ' ', text)
text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
text = text.lower()
text = text.split()
counter = Counter(text).most_common()

with open('genius.csv', 'w', encoding='utf-8') as file:
    file.write(str(counter))
