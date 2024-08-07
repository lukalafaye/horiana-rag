from PyPDF2 import PdfReader
import os
from pprint import pprint
import re


def PDF_PROCESS (pdf_path) :
    
    pages_text,Metadata,tab=extract_information2(pdf_path)
    Textab=tab
    label,text,start=Summary(pages_text)
    Title,Text=CORE(pages_text,start+1)
    SubTitle=[]
    SubText=[]
    for i in range (len(Title)):
        a,b=SUBCORE(Text[i])
        if len(a)!=0 :
            SubTitle.append(a)
            SubText.append(b)
        else :
            SubTitle.append([Title[i]])
            SubText.append([Text[i]])
    Content=[]
    Titab=[]
    for i in range (len(tab)) :
        Content.append(INFO_TABLE(tab[i])[0:3])
        Titab.append(INFO_TABLE(tab[i])[3])
        
    Parts={
        "SubTitle" : SubTitle,
        "Text" : SubText
    }


    Sum={
        "label" : label,
        "text" : text
    }

    Core={
        "Title" : Title,
        "Parts" : Parts
    }

    Table= {
        "Titab" :Titab,
        "Content" :Content,
        "Textab" :Textab
    }

    Document = {
        "Metadata": Metadata,
        "Sum": Sum,
        "Core": Core,
        "Table": Table
    }
    return(Document)
def extract_information2(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        meta = reader.metadata
        number_of_pages = len(reader.pages)    
        pages_text = []
        for n in range(number_of_pages):
            page = reader.pages[n]
            pages_text.append('\n'+page.extract_text())
    metadata = f"""
    Information about {pdf_path}: 

    Author: {meta.author}
    Creator: {meta.creator}
    Producer: {meta.producer}
    Subject: {meta.subject}
    Title: {meta.title}
    Number of pages: {number_of_pages}
    """
    g=re.compile('TABLE ')
    print(metadata)
    bel,tab,pages_text=EXTRACT_TABLE2 (pages_text)
    return(pages_text,metadata,tab)
def EXTRACT_TABLE2 (pages_text) :
    i=0
    n=len(pages_text)
    res=[]
    label=[]
    p=re.compile(r'TABLE [0-9]\n')
    d=re.compile(r'([0-9]\n[^012345789]{40,100})|(TABLE [0-9]\n)')
    while i<n :
        pos=p.search(pages_text[i])
        if pos!=None :
            label.append(pages_text[i][pos.start():pos.end()])
            dos=d.search(pages_text[i][pos.end():])
            res.append(pages_text[i][pos.end():pos.end()+dos.start()])
            pages_text[i]=pages_text[i][:pos.start()]+pages_text[i][pos.end()+dos.start():]
        else :
            i+=1
    return(label,res,pages_text)
def CORE(pages_text,start) :
    res=[]
    label=["INTRODUCTION"]
    n=len(pages_text)
    i=0
    rep=0
    p=re.compile(r'([A-Z]{6,}\n)|(ORCID iDs)')
    Prems=0
    while i<n :
        pos=p.search(pages_text[i][rep:])
        if Prems==0 and pos!=None :
            doc=pages_text[0][start:]
            for l in range (i-1):
                doc+=pages_text[l]
            doc+=pages_text[i][:pos.start()+rep]
            Prems=1
            res.append(doc)
        if pos!=None :
            label.append(pages_text[i][pos.start()+rep:pos.end()+rep])
            start=pos.end()+rep
            rep=start
            j=i
            while(j<n) :
                pos=p.search(pages_text[j][rep*(i==j):])
                if pos!=None :
                    end=pos.start()+rep*(i==j)
                    doc=''
                    k=j-i
                    doc+=pages_text[i][start-1:(i==j)*(end-1)+(i!=j)*(len(pages_text[i]))]
                    for l in range(k-1) :
                        doc+=pages_text[i+l+1]
                    doc+=pages_text[j][:(end-1)*(i!=j)]
                    res.append(doc)
                    j=n+1
                j+=1
            if j==n :
                doc=pages_text[i][start:]
                for l in range(n-1-i) :
                    doc+=pages_text[i+l+1]
                res.append(doc)
                i=n
        else :
            i+=1
            rep=0
    return (label,res)
def Summary(pages_text) :
    Marks = ['Background:', 'Purpose/Hypothesis:','Purpose:','Hypothesis:','Study Design:','Methods', 'Results:',  'Conclusion:', 'Registration:','Keywords:','\n']
    res=[]
    label=[]
    for i in range (len(Marks)-1) :
        p=re.compile(Marks[i])
        pos=p.search(pages_text[0])
        if pos!=None :
            start=pos.end()
            label.append(Marks[i])
            j=int(1)
            while(j<len(Marks)) :
                p=re.compile(Marks[i+j])
                pos=p.search(pages_text[0][start:])
                if pos!=None :
                    end=pos.start()
                    res.append(pages_text[0][start:start + end-1])
                    j=len(Marks)
                j+=1
    return (label,res,start + end)

def SUBCORE(par) :
    res=[]
    label=['Introduction']
    p=re.compile(r'\n((?!Journal)[A-Z][\-a-z\, ]{1,20}\s*){1,}\n')
    pos=p.search(par)
    prems=0
    while pos!=None :
        prems+=1
        res.append(par[:pos.start()])
        label.append(par[pos.start():pos.end()])
        par=par[pos.end():]
        pos=p.search(par)   
    res.append(par)
    if prems==0 :
        label=['Text Body']
    return (label,res)

def INFO_TABLE (tab) :
        p=re.compile(r'[A-Z][a-z]{1,20}\s(\(*[A-Z][a-z\) ]{1,40}){1,}\n')
        pos=p.search(tab)
        titre = tab[pos.start():pos.end()]
        tab=tab[pos.end():]
        p=re.compile(r'([A-Z][a-z ]{1,40}){1,}[Nn=0-9\( ]*[\)\n]+')
        r=re.compile(r'\n')
        dos=r.search(tab)
        tabtit=tab[:dos.end()]
        tab=tab[dos.end():]
        pos = p.search(tabtit)
        Head=[]
        Line=[]
        nb=[]
        while pos!=None :
            Head.append(tabtit[pos.start():pos.end()])
            tabtit=tabtit[pos.end():]
            pos=p.search(tabtit)   
        p=re.compile(r'[0-9]')
        pos=p.search(tab)        
        while pos!=None :
            Line.append(tab[:pos.start()])
            tab=tab[pos.start():]
            p=re.compile(r'[A-Z\n]')
            pos=p.search(tab)
            if pos!=None :
                nb.append(EXTRACT_LINE(tab[:pos.start()],Head))
                tab=tab[pos.start():]
            else :
                nb.append(EXTRACT_LINE(tab,Head))
                tab=''
            p=re.compile(r'[0-9\.\(\) ]{5,}')
            pos=p.search(tab)
        return(Head,Line,nb,titre)

def EXTRACT_LINE(line,Head) :
    d=re.compile(r'[0-9]')
    pos=d.search(line)
    line=line[pos.start():]
    p=re.compile(r'\s')    
    pos=p.search(line)
    nb=[]
    while pos!=None :
        nb.append(line[:pos.start()])
        line=line[pos.end():]
        pos=p.search(line)
    if d.search(line)!=None :    
        nb.append(line)
    n=len(nb)
    res=[]
    if n == len(Head)*2 :
        for i in range (n//2) :
            if nb[2*i+1][0]=='(' :
                res.append(nb[2*i]+nb[2*i+1])
            else :
                res.append(nb[2*i]+'+-'+nb[2*i+1][1:])
    elif n==len(Head)*2-1 :
        for i in range (n//2) :
            if nb[2*i+1][0]=='(' :
                res.append(nb[2*i]+nb[2*i+1])
            else :
                res.append(nb[2*i]+'+-'+nb[2*i+1][1:])
        res.append(nb[n-1])
    else :
        res=nb
    return(res)


Document = PDF_PROCESS("C:/Users/felix/OneDrive/Documents/Course SF/AP_20211103_SONNERY_COTTET_Article publié.pdf")

print(Document)
