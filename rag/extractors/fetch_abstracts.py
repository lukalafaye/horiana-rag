import pandas as pd
from pymed import PubMed
import json 

docker = False 

def fetch_from_keywords(keywords: list[str]):
    pubmed = PubMed(tool="PubMedSearcher", email="myemail@ccc.com")
    #Monkey patch to use api key
    #my_api_key = 'thisismyapikey'
    #pubmed.parameters.update({'api_key': my_api_key})
    # pubmed._rateLimit = 10

    ## PUT YOUR SEARCH TERM HERE ##
    search_terms = [keyword for keyword in keywords]

    # Create a GraphQL query in plain text
    # query = '(("2018/05/01"[Date - Create] : "3000"[Date - Create])) AND (Xiaoying Xian[Author] OR diabetes)'

    articleList = []
    articleInfo = []

    for search_term in search_terms:
        results = pubmed.query(search_term, max_results=10)   

        for article in results:
        # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
        # We need to convert it to dictionary with available function
            articleDict = article.toDict()
            articleList.append(articleDict)

        # Generate list of dict records which will hold all article details that could be fetch from PUBMED API
        for article in articleList:
        #Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
            pubmedId = article['pubmed_id'].partition('\n')[0]
            # Append article info to dictionary 
            articleInfo.append({u'pubmed_id':pubmedId,
                            u'title':article['title'],
                            u'keywords':article['keywords'],
                            u'journal':article['journal'],
                            u'abstract':article['abstract'],
                            u'conclusions':article['conclusions'],
                            u'methods':article['methods'],
                            u'results': article['results'],
                            u'copyrights':article['copyrights'],
                            u'doi':article['doi'],
                            u'publication_date':article['publication_date'], 
                            u'authors':article['authors']})

        # Generate Pandas DataFrame from list of dictionaries
    articlesPD = pd.DataFrame.from_dict(articleInfo)
    articlesPD.drop_duplicates(subset=['doi'], inplace=True)

    # Saving instructions
    config_path = 'config.json'
    if docker:
        config_path = '/app/' + config_path

    # Lire le fichier de configuration JSON
    with open(config_path, 'r') as f:
        config = json.load(f)

    abstracts_path = config.get('abstracts_path')
    articlesPD.to_csv(abstracts_path, index = None, header=True)

    return articlesPD

def main():
    keywords = ["knee", "bucket"]
    articlesPD = fetch_from_keywords(keywords)

if __name__ == "__main__":
    main()
