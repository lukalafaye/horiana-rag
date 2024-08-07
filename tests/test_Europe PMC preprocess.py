import xml.etree.ElementTree as ET
import requests
import pandas as pd



def getCore(root) :
    label=[]
    Sublabel=[]
    Subtxt=[]
    body=root.find('body')
    Core=body.findall('sec')
    for part in Core :
        Sublabel.append([])
        Subtxt.append([])
        lab=part.find('title')
        if (lab!=None) :
            label.append(lab.text)
            #res.append(get_full_text(part))
            SubCore=(part.findall('p') + part.findall('sec'))
            for SubPart in SubCore :
                Subtxt[-1].append(ET.tostring(SubPart, encoding='unicode', method='xml'))
                Sublab=SubPart.findall('title') or SubPart.findall('bold')
                if len(Sublab) !=0 :
                    Sublabel[-1].append(Sublab[0].text)
                else :
                    Sublabel[-1].append([])
    return(label,Sublabel,Subtxt)

def POSTLABEL (Sublabel) :
    n= len(Sublabel) 
    for i in range (n) :
        p=len(Sublabel[i])
        m=p
        for j in range(p) :
            if len(Sublabel[i][j])>0 :
                m=j
                break
        for j in range(m) :
            if m==p :
                Sublabel[i][j]='Text Body part '+str(j)
            else :
                Sublabel[i][j]='Introduction part '+str(j)
    return(Sublabel)

def FULLTXT(id) :
    root=get_fulltext(id)
    Title,Subtitle,SubText=getCore(root)
    SubTitle=POSTLABEL(Subtitle)
    Abstract=getAb(root)
    Parts={
        "SubTitle" : SubTitle,
        "Text" : SubText
    }

    Core={
        "Title" : Title,
        "Parts" : Parts
    }
    Document = {
        "Abstract": Abstract,
        "Core": Core,
    }
    return(Document)

def RECHERCHE_ARTICLE(Keywords) :
    # Exemple de requête
    query = Keywords + " AND (HAS_FT:Y)"
    articles = get_articles(query)
    
    # Convertir les articles en DataFrame
    if articles:
        df = articles_to_dataframe(articles)
        for i in range(len(df['fulltext'])) :
            compt=FULLTXT(df['id'][i])
            df['fulltext'][i]=compt
        return(df)
    else:
        print("Erreur lors de la récupération des articles.")


def get_full_text(element):
    text = element.text or ''
    for child in element:
        if child.tag == 'sec':
            text += '\n' + ET.tostring(child, encoding='unicode', method='text')
        else:
            text += ET.tostring(child, encoding='unicode', method='text')
    return text

def getAb(root) :
    for ab in root.iter('abstract') :
        res=''
        for par in ab :
            if isinstance(par.text,str):
                res+='\n' + par.text
    return(get_full_text(ab))


def get_fulltext(article_id):
    fulltext_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/"
    url = f"{fulltext_url}{article_id}/fullTextXML"
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        return root
    else:
        print(f"Erreur lors de la récupération du texte intégral pour l'article {article_id}: {response.status_code}")
        print(f"Réponse: {response.text}")
        return None


def articles_to_dataframe(articles):
    data = []
    for article in articles.get('resultList', {}).get('result', []):
        article_id = article.get('pmcid')
        fulltext = get_fulltext(article_id)
        data.append({
            'id': article_id,
            'title': article.get('title'),
            'abstract': article.get('abstractText'),
            'journal': article.get('journalInfo', {}).get('journal', {}).get('title'),
            'publicationDate': article.get('journalInfo', {}).get('printPublicationDate'),
            'authors': [author.get('fullName') for author in article.get('authorList', {}).get('author', [])],
            'fulltext': fulltext
        })
    return pd.DataFrame(data)


def get_articles(query, result_type='search', format='json'):
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
    url = f"{base_url}query={query}&resultType=core&format={format}&source=MED&sort_cited:y"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la requête à l'API: {response.status_code}")
        print(f"Réponse: {response.text}")
        return None

df=RECHERCHE_ARTICLE("ACLR")

for i in range (len(df['fulltext'][0]['Core']['Title'])) :
    print('===========')
    print(df['fulltext'][0]['Core']['Title'][i])
    print('===========')
    for j in range(len(df['fulltext'][0]['Core']['Parts']['SubTitle'][i])) :
        print(df['fulltext'][0]['Core']['Parts']['SubTitle'][i][j])
        print('---------')
        print(df['fulltext'][0]['Core']['Parts']['Text'][i][j])
        print('--------')
