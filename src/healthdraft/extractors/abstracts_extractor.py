import pandas as pd
from pymed import PubMed
import os
import json
from src.config import get_absolute_path  # Import function to get absolute path, also runs config.py to set up environment variables

docker = False  # Flag to check if the script is running in a Docker environment

def fetch_from_keywords(keywords: list[str]):
    """
    Fetches articles from PubMed based on a list of keywords, removes duplicates.

    Args:
        keywords (list[str]): List of keywords to search for articles.

    Returns:
        pd.DataFrame: A DataFrame containing the fetched articles' details.
    """
    # Filter out empty or whitespace-only keywords
    keywords = [keyword for keyword in keywords if keyword.strip()]

    if keywords is None or len(keywords) == 0:
        print("Keywords cannot be empty")
        return None

    # Initialize PubMed API with a tool name and an email for identification
    pubmed = PubMed(tool="PubMedSearcher", email="myemail@ccc.com")

    # Retrieve PubMed API key from environment variables
    pubmed_api_key = os.getenv("PUBMED_API_KEY")

    if pubmed_api_key is None:
        raise ValueError("API_KEY environment variable is not set")

    # Use the API key in the PubMed API requests
    pubmed.parameters.update({"api_key": pubmed_api_key})
    pubmed._rateLimit = 10  # Inrease the rate limit for API calls

    # Initialize lists to store article information
    articleList = []
    articleInfo = []

    # Iterate over each search term (keyword)
    for search_term in keywords:
        # Query PubMed with the search term, retrieving up to 10 results
        results = pubmed.query(search_term, max_results=10)

        for article in results:
            # Convert the article object to a dictionary
            articleDict = article.toDict()
            articleList.append(articleDict)

        # Extract relevant information from each article
        for article in articleList:
            # Handle cases where 'pubmed_id' might contain multiple IDs
            pubmedId = article["pubmed_id"].partition("\n")[0]

            # Append the article's details to the list
            articleInfo.append(
                {
                    "pubmed_id": pubmedId,
                    "title": article["title"],
                    "keywords": article["keywords"],
                    "journal": article["journal"],
                    "abstract": article["abstract"],
                    "conclusions": article["conclusions"],
                    "methods": article["methods"],
                    "results": article["results"],
                    "copyrights": article["copyrights"],
                    "doi": article["doi"],
                    "publication_date": article["publication_date"],
                    "authors": article["authors"],
                }
            )

    # Convert the list of article details to a Pandas DataFrame
    articlesPD = pd.DataFrame.from_dict(articleInfo)

    # Remove duplicate entries based on the 'doi' column
    articlesPD.drop_duplicates(subset=["doi"], inplace=True)

    return articlesPD

def main():
    """
    Main function to fetch articles based on predefined keywords and save them as a CSV file.
    """
    keywords = ["knee", "bucket", "asthma", "diabetes"]  # Example keywords
    articlesPD = fetch_from_keywords(keywords)  # Fetch articles from PubMed

    # Retrieve the path to the configuration file
    config_path = get_absolute_path("config.json")

    # Adjust the config path if running in a Docker environment
    if docker:
        config_path = "/app/" + config_path

    # Read the JSON configuration file
    with open(config_path, "r") as f:
        config = json.load(f)

    # Get the output path for the abstracts from the config file
    abstracts_path = get_absolute_path(config.get("abstracts_output_path"))

    # Save the fetched articles to a CSV file
    articlesPD.to_csv(abstracts_path, index=None, header=True)

if __name__ == "__main__":
    main()  # Execute the main function if this script is run directly