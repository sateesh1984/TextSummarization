import re, string, unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer

import json
from gensim.summarization import summarize
import PyPDF2

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text

def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)
def extractPdfText(filePath=''):


    fileObject = open(filePath, 'rb')
   
    pdfFileReader = PyPDF2.PdfFileReader(fileObject)
    totalPageNumber = pdfFileReader.numPages
    info=pdfFileReader.getDocumentInfo()
    currentPageNumber = 1
    text = ''
    #print(info)

    while(currentPageNumber < totalPageNumber ):

       
        pdfPage = pdfFileReader.getPage(currentPageNumber)
        text = text + pdfPage.extractText()
        #print("page number : "+str(currentPageNumber))
        #print(pdfPage.extractText())
        #print()
        currentPageNumber = currentPageNumber + 1
    return text
def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words
def format_sent(sentence):
    sentence = sentence.replace(".","")
    sentence = sentence.replace("  ","")
    
    return sentence

pdfText = extractPdfText("C:\\Users\\sontikommu2\\Downloads\\Gartner_Reports2\\Gartner_Reports2\\Modern Platform - VMware Design v1.2 - Release Note.pdf")

sampleText = denoise_text(pdfText)

sampleText = replace_contractions(sampleText)

words = nltk.word_tokenize(sampleText)

prepare = ' '.join(words).replace('Ł','')

splsent = sent_tokenize(prepare)

filt = ["NNP","NN","JJ"]
filt_sent =[]
for sent in splsent:
    sent=format_sent(sent)
    tkns=word_tokenize(sent)
    if(len(tkns)>0):
        kk=nltk.pos_tag([tkns[0]])
        if(len(kk)>0):
            if(kk[0][1] in filt):
                filt_sent.append(sent)
                #print(""+str(kk[0][1])+"      "+sent)
formatted = ". ".join(filt_sent)
#print(filt_sent)
#print(formatted)

count=len(filt_sent)
if(count<=2):
    sum_count=count
elif(count<=20):
    sum_count=2
elif(count<=50):
    sum_count=3
elif(count<=100):
    sum_count=4
else:
    sum_count=5

print("{} {}",count,sum_count)
print(summarize(formatted,0.2))
#print(formatted)


parser = PlaintextParser.from_string(formatted, Tokenizer("english"))
#print(parser.document)
summarizer = LexRankSummarizer()

summary = summarizer(parser.document, sum_count) #Summarize the document with 5 sentences
#print(pdfText)
print("LexRank")
for sentence in summary:
    print(sentence)

summarizer_lsa = LsaSummarizer()
summary_2 =summarizer_lsa(parser.document,sum_count)
print("Lsa")
for sentence in summary_2:
    print(sentence)
    
    
summarizer_luhn = LuhnSummarizer()
summary_1 =summarizer_luhn(parser.document,sum_count)
print("Luhn")
for sentence in summary_1:
    print(sentence)