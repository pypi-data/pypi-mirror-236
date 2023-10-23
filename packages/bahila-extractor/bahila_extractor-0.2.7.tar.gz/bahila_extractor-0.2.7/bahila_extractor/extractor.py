from datetime import datetime
import sys
# Add the path of the directory containing the theguardian module to sys.path
# Replace 'path_to_theguardian_module' with the actual path to the module's directory
import requests
import openai
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
# import sys
# sys.path.append('../')
# from .theguardian_content import theguardian_content



PAGESIZE = 10


"""
The content endpoint (/search) returns
all pieces of content in the API.
"""
import requests
import copy


class Content:

    def __init__(self, api, url=None, **kwargs):
        """
        :param api: api_key
        :param url: optional url to get the content.
        :param kwargs: optional header data
        :return: None
        """

        self.__headers = {
            "api-key": api,
            "format": "json"
        }
        self.__request_response = None

        if url is None:
            self.base_url = "https://content.guardianapis.com/search"
        else:
            self.base_url = url

        if kwargs:
            for key, value in kwargs.items():
                self.__headers[key] = value

    def __response(self, headers=None):

        """
        :param headers: optional header
        :return: returns raw response.
        """

        if headers is None:
            headers = self.__headers
        else:
            headers.update(self.__headers)

        res = requests.get(self.base_url, headers)

        return res

    def get_request_response(self, headers=None):

        """
        :param headers: optional headers
        :return: raw request response
        """

        self.__request_response = self.__response(headers)
        return self.__request_response

    def get_content_response(self, headers=None):

        """
        :param headers: optional header
        :return: json content of the response for the request
        """

        self.get_request_response(headers)
        return self.__request_response.json()

    def response_headers(self, headers=None):

        """
        :param headers: optional header
        :return: dict of header contents in the response
        """

        if self.__request_response:
            response_content = copy.deepcopy(self.__request_response.json())
        else:
            self.get_request_response(headers)
            response_content = copy.deepcopy(self.__request_response.json())

        headers_content = response_content['response']
        headers_content.pop("results")

        return headers_content

    def find_by_id(self, ids, **kwargs):

        """
        :param ids: Get the Content using its id. IDs are usually in the form
        of url/section/YYYY/month/DD/name-of-article/
        technology/2014/feb/17/flappy-bird-clones-apple-google

        :param kwargs: optional headers
        :return: dict
        """

        ids_and_options = self.__response_for_id(ids, **kwargs)
        ids_and_options.update(self.__headers)

        return self.__response(ids_and_options).json()

    @staticmethod
    def __response_for_id(ids, **kwargs):

        """
        :param ids: IDs are usually in the form
        of url/section/YYYY/month/DD/name-of-article/

        :param kwargs: optional headers
        :return: dict
        """

        headers = {}

        if ids and isinstance(ids, str):
            headers["ids"] = ids
        if kwargs:
            headers.update(kwargs)

        return headers

    @staticmethod
    def get_results(content):

        """
        :param content: response from url
        :return: list of results
        """

        if isinstance(content, dict):
            results = content["response"]["results"]
        else:
            raise TypeError("Content of type dictionary required as input.")

        return results if results else []

    def get_references_in_page(self, page_number=None):

        """
        :param page_number: optional
        :return:
        """

        head = self.response_headers()

        if page_number is None:
            content = self.get_content_response({
                "show-references": "all"
            })
            results = self.get_results(content)
            references = self.__get_references(results)
            return references
        elif page_number and page_number <= head["pages"]:
            content = self.get_content_response({
                "page": page_number,
                "show-references": "all"
            })
            results = self.get_results(content)
            references = self.__get_references(results)
            return references
        else:
            raise ValueError("Page number greater than available pages. Available pages {}."
                             .format(head["pages"]))

    @staticmethod
    def __get_references(results):

        """
        :param results: list of results
        :return: list of results
        """

        refs = [(result["id"], result["references"]) for result in results if result["references"]]

        return refs



# Filter function to remove unwanted content
unwanted_keywords = ["football", "society","fashion","music","lifeandstyle","environment","media","tv-and-radio","film"]
def filter_function(content):
    title = content.get('webTitle', '').lower()
    section = content.get('sectionName', '').lower()
    for keyword in unwanted_keywords:
        if keyword in title or keyword in section:
            return False
    return True

def get_content(fromdate, todate, keyword, api_key, page_size=10):
    """
    Fetches and filters articles from The Guardian based on given criteria.
    
    Parameters:
    - fromdate (str): The start date in the format "YYYY-MM-DD" to fetch articles from. 
    - todate (str): The end date in the format "YYYY-MM-DD" to fetch articles until.
    - keyword (str): A keyword or phrase to search within the articles.
                     If left empty, it will fetch articles without a specific keyword filter.
    - api_key (str): Your API key provided by The Guardian.

    Returns:
    - List[Dict]: A filtered list of articles from The Guardian. Each article 
                  is represented as a dictionary with details like title, URL, etc.

    Description:
    The function fetches articles from The Guardian's "world" section within 
    the specified date range and containing the given keyword. The fetched articles 
    are then filtered to exclude those with certain unwanted keywords or from unwanted sections.
    """
    
    # Set up query parameters
    params = {
        "section" : "world",
        "from-date": fromdate,
        "to-date": todate,
        "q": keyword,
        "api-key": api_key,
        "page-size": page_size
    }


    
    # Create the Content instance with the specified parameters
    content = Content(api=api_key, **params)

    # Get content response
    json_content = content.get_content_response()

    # Extract results from the response
    results = content.get_results(json_content)

    # Apply the filter to the results
    filtered_results = list(filter(filter_function, results))
    
    return filtered_results


def fetch_article_content(api_key, endpoint):
    # Construct the full URL with the API key
    url = f"{endpoint}?api-key={api_key}&show-fields=body"
    
    # Make the GET request to the API
    response = requests.get(url)
    
    # If the request was successful, extract and return the article content
    if response.status_code == 200:
        data = response.json()
        article_content = data["response"]["content"]["fields"]["body"]
        article_content = BeautifulSoup(article_content, 'html.parser').get_text()
        return article_content
    else:
        return f"Error {response.status_code}: Unable to fetch the article."
    
def event_type_classification(headline):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": f"Here is the title of a news piece: {headline}\nQuestion: Did anyone die in this event? Only answer yes or no."
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    
    return response["choices"][0]['message']['content']


def get_title_and_content(start_time, end_time, keyword, api_key, page_size=10):
    contents = get_content(start_time, end_time, keyword, api_key, page_size=page_size)
    news_dic = dict()
    for item in contents:
        date = item.get('webPublicationDate','').split('T')[0]
        endpoint = item.get('apiUrl','')
        item = {"title": item.get('webTitle', ''), "endpoint": item.get('apiUrl',''),
        "main_content": fetch_article_content(api_key, endpoint), "url": item.get('webUrl','')}
        if date not in news_dic:
            news_dic[date] = [item]
        else:
            news_dic[date].append(item)
    return news_dic



def filter_news(start_time, end_time, keyword, api_key):
    print('start filtering news')
    news_dic = get_title_and_content(start_time, end_time, keyword, api_key)
    print('finish fetching news')
    # print(news_dic)
    filtered_dic = dict()
    for date, data in news_dic.items():
        filtered_dic[date] = list()
        for news in data:
            # if 'yes' in event_type_classification(news['title']).lower():
            #     filtered_dic[date].append(news)
            filtered_dic[date].append(news)
    
    return filtered_dic


def get_casualty_dict(main_content):
    # Schema
    schema = {
        "properties": {
            "event_subject": {"type": "string"},
            "event_number_of_victims": {"type": "integer"},
            "event_location": {"type": "string"},
        },
        # "required": ["number_of_victims"],
    }

    # Input (trimmed)
    inp = main_content[:4000]

    # Run chain
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    chain = create_extraction_chain(schema, llm)
    result = chain.run(inp)

    # final_result = None
    # for event in result:
    #     # make sure the event_number_of_victims is not None
    #     if event['event_number_of_victims'] is None:
    #         continue
    #     if event['event_number_of_victims'] == max([e['event_number_of_victims'] for e in result if e['event_number_of_victims'] is not None]):
    #         final_result  = event
    
    return result