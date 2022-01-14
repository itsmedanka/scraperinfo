import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.common.by import By 
import re
import time
import re
import spacy
from string import punctuation

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("start-maximized")
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome('chromedriver',options=chrome_options)
question = input("Search for:")
question = question.replace(' ','+')
browser.get("https://www.google.com/search?q="+question)

time.sleep(3)

linky = []
headings = browser.find_elements(By.XPATH, '//div[@class = "g"]')
numbery = 0
for heading in headings:

    title = heading.find_elements(By.TAG_NAME, 'h3')
    links = heading.find_element(By.CSS_SELECTOR, '.yuRUbf>a').get_attribute("href")  # This ain't working either, any help?
    linky.append(links)
    print(links)
    # link = heading.find_element_by_name('a href')
    for t in title:
        print('title:', t.text, "---------------", numbery)
        numbery = numbery + 1

print('scraping through all links and giving you points')

time.sleep(5)

main_link = linky[0]
browser.get(main_link)
time.sleep(10)
MainHead = ""
paragraph = ""
paras = browser.find_elements(By.TAG_NAME,'p')
headings = browser.find_elements(By.TAG_NAME,'h1')
for heading in headings:
  print(heading.text)
  MainHead = MainHead + heading.text
print('------------------------------------------------------')
for para in paras:
  paragraph = paragraph + '\n' + para.text

with open('DataExtracter.txt','w') as f:
  f.write(MainHead)
  f.write('\n')
  f.write(paragraph)


nlp = spacy.load('en_core_web_trf')
with open('DataExtracter.txt','r') as f:
  text = f.read()


doc= nlp(text)
result = []
ent_tag = ['ORG', 'GPE', 'PERSON','LANGUAGE','NORP'] 
pos_tag = ['ADJ','NOUN','PROPN']

for token in doc.ents:
  if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
    continue
  if(token.label_ in ent_tag):
    result.append(token.orth_)


for token in doc:
  if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
    continue
  if(token.pos_ in pos_tag):
    result.append(token.orth_)

sentence = []
for sent in doc.sents:
  sentence.append(sent.orth_)

res = []
for i in set(result):
  res.append(i)

print(res)

def filter_lines_by_keywords(lines_to_filter, key_words):
   key_words_s = set(key_words)
   return filter(lambda l: set(l.split()) & key_words_s, lines_to_filter)

resu = filter_lines_by_keywords(lines_to_filter = sentence, key_words = res)
for i in list(resu):
  print(i)

