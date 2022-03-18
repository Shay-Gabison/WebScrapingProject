from pdfminer.pdfpage import PDFPage
import os.path
import re
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO



class TxtManipulation:
    dictionary = {
        "enemies": ["Algeria", "Bangladesh", "Brunei", "Iran", "Iraq", "Kuwait", "Lebanon", "Libya", "Malaysia",
                    "Pakistan",
                    "Saudi Arabia", "Syria", "Yemen", "israel", "gaza", "palestine", "Ukraine", "russia"]
        ,
        "buzzwords": ["aggression", "assault", "attempt", "blitz", "blitzkrieg", "charge", "coup de main", "descent",
                      "offense",
                      "offence)", "offensive", "onset", "onslaught", "raid", "rush", "strike", "air raid",
                      "bombardment",
                      "bombing", "access", "bout", "case", "fit", "seizure", "siege", "spell", "turn", "assail",
                      "assault",
                      "beset", "bushwhack", "charge", "descend", "raid", "rush", "strike", "trash"
                                                                                           "declining", "dismissing",
                      "refusing", "rejecting", "repudiating", "spurning", "turning down"
                                                                          "combating", "combatting", "contesting",
                      "fighting",
                      "opposing", "resisting"
                                  "avoiding", "bypassing", "circumventing", "dodging", "eluding", "escaping", "evading",
                      "missing", "troopers", "army", "weapen"
                                                     "abstaining", "forbearing", "refraining"],
        "israel": ["middle east", "israel", "IDF", "jewish", "jews", "jew", "mossad", "israeli", "shabak"]}
    def __init__(self,path,json):
        # search init

        self.path=path
        self.json=json
        rsrcmgr = PDFResourceManager()
        self.rsrcmgr=rsrcmgr

        retstr = StringIO()
        self.retstr=retstr

        self.codec = 'utf-8'
        laparams = LAParams()
        self.laparams=laparams
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        self.device=device
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        self.interpreter=interpreter
        self.password = ""
        self.maxpages = 0
        self.caching = True
        pagenos = set()
        self.pagenos = pagenos


    def classifaingArticals(self,name):
        count = 0
        fp = open(r'C:\Users\OWNER\Downloads\%s' % name, 'rb')
        text = ""
        for page in PDFPage.get_pages(fp, self.pagenos, maxpages=self.maxpages, password=self.password, caching=self.caching,
                                      check_extractable=True):
            self.interpreter.process_page(page)

            text = self.retstr.getvalue()

        for dic in range(len(self.dictionary)):
            for word in self.dictionary:
                res_search = re.search(word, text)
                if res_search is not None:
                    count += 1
                    break
                continue
        self.retstr.close()
        return count

    def searchStringInPDF(self,String):
        for fp in os.listdir(self.path):
            if fp.endswith(".pdf"):
                new_url = self.path + '\%s' % fp
                filep = open(new_url, 'rb')
                with open(self.json, "r") as file:
                    json_object = json.load(file)
                text = ""
                res_search = ""
                for page in PDFPage.get_pages(filep, self.pagenos, maxpages=self.maxpages, password=self.password, caching=self.caching,
                                              check_extractable=True):
                    self.interpreter.process_page(page)

                    text = self.retstr.getvalue()
                    res_search = re.search(String, text)
                arr=filep.name.split("Downloads\\")
                filename=arr[1]
                if res_search is not None:
                    print(filename + ": " + json_object[filename]["url"])
                    print(text)
            filep.close()

    def sumerisingArticls(self,new_url):
        new_url = self.path + '\%s' % new_url
        fp = open(new_url, 'rb')
        fp.name
        str1=""
        for page in PDFPage.get_pages(fp, self.pagenos, maxpages=self.maxpages, password=self.password, caching=self.caching,
                                      check_extractable=True):
            self.interpreter.process_page(page)
            text = self.retstr.getvalue()
        str1 = f"{text}"  # prints 'string'
        with open(fp.name.replace("pdf", "txt"), 'w',encoding='utf-8') as file:
            file.write(str(str1))
            file.close()
        str1=""
        self.__init__(self.path,self.json)
        fp.close()
    def sumerisingArticlsLOOP(self):

        for file in os.listdir(self.path):
            if file.endswith(".pdf"):
                new_url = self.path + '\%s' % file
                self.sumerisingArticls(new_url)
        self.device.close()
        self.retstr.close()
    def searchStringInJSON(self,pathstr,String):
        new_url = r'C:\Users\OWNER\Downloads' + '\%s.json' % pathstr
        str1=String.upper()
        with open(new_url, "r") as file:
            json_object = json.load(file)
        for i in json_object:
            for key in json_object.get(i):
               if json_object[i].get(key)== str1:
                   print (json_object[i])
        file.close()