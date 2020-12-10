import docx2txt
import re
from bs4 import BeautifulSoup
import requests 
#for plagiarism
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import string
from difflib import SequenceMatcher
#for grammar
#import language_tool_python
#tool = language_tool_python.LanguageTool('en-US')
'''
def gram_check(text):
    matches = tool.check(text)
    res={}
    final=''
    for prob in matches:
        final+=str(prob)
        final+='\n'
    return final
'''
    
def plag_check(main_text,cand_text):
    X=word_tokenize(main_text)
    Y=word_tokenize(cand_text)
    sw = stopwords.words('english')

    #remove stopwords
    X_set = {w for w in X if not w in sw} 
    Y_set = {w for w in Y if not w in sw}

    #remove punctuations
    X_set = list(filter(lambda X_set: X_set not in string.punctuation, X_set))
    Y_set = list(filter(lambda Y_set: Y_set not in string.punctuation, Y_set))

    st1=" "
    st1=st1.join(X_set)

    st2=" "
    st2=st2.join(Y_set)

    #Jaccard Similiarity
    a = set(st1.split()) 
    #print(len(a))
    b = set(st2.split())
    c = a.intersection(b)
    #print(len(c))
    try:
        return (float(len(c)) / len(a))*100
    except:
        return 0

def calculate_ratio(matches, length):
    if length:
        return 1.0 * matches / length
    return 0

def sequence_check(main_text,cand_text):
    m1 = SequenceMatcher(None, main_text, cand_text)
    matches1 = sum(triple[-1] for triple in m1.get_matching_blocks())
    return calculate_ratio(matches1,len(main_text))*100
  



def extract_link(my_text):
    links=re.findall(r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b', my_text)
    return links


def scrape(url):
    #to avoid 503 error and to replicate human access to the page
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    print("Downloading using the URL %s"%url)
    r = requests.get(url, headers=headers)
    #Status Check
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon \n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None

    return r

def get_document(page):
    soup = BeautifulSoup(page.text, "lxml")
    all_para=soup.find_all("p")
    doc=[]
    for para in all_para:
        doc.append(para.get_text())
    document=' '.join(doc)
    return document
