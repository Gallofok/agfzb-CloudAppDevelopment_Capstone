import requests
import json
from .models import CarDealer,Review
from requests.auth import HTTPBasicAuth

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, params=None, data=None):
    try:
        response = requests.post(url, params=params, json=data)
        
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
    except Exception as error:
        print(f"Other error occurred: {error}")
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url,**kwargs):
    print(kwargs['api_key'])
    print("GET from {} ".format(url))
    json_data = 0

    if "api_key" in kwargs:
    # Call get method of requests library with URL and parameters
        try:
            print("API—KEY USED")
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=params["text"],auth=HTTPBasicAuth('apikey', kwargs['api_key']))
            
            # status_code = response.status_code
            # print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
            return json_data
        except:
        # If any error occurs
            print("Network exception occurred")
            pass
    else:            
        try: 
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                            params=kwargs)

            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
            return json_data                          
        except:
            print("Network exception occurred")
            pass






# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"],state = dealer_doc["state"])
            results.append(dealer_obj)
    return results


def get_dealer_by_id(url, dealerId):
    result = None
    data = {"id": dealerId}
    json_result = post_request(url, data = data) # here is diction
    if json_result:
        dealer = json_result.get("docs") # here is list
        dealer = dealer[0]
        result = CarDealer(
            address=dealer["address"], 
            city=dealer["city"], 
            full_name=dealer["full_name"],
            id=dealer["id"], 
            lat=dealer["lat"], 
            long=dealer["long"],
            short_name=dealer["short_name"],
            st=dealer["st"], 
            zip=dealer["zip"], 
            state=dealer["state"]
        )
    return result
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    result = None
    data = {"dealership": dealerId}
    json_result = post_request(url, data = data)
    reviews = []
    if json_result:
        # Get the rows field from JSON response
        docs = json_result.get("docs")
        print(docs)
        # Iterate through the rows
        for doc in docs:
            # Get the doc field from row
            # Create a  Review object with values in the doc object
            review = Review(
                name=doc.get('name'),
                dealership=doc.get('dealership'),
                review=doc.get('review'),
                purchase=doc.get('purchase'),
                purchase_date=doc.get('purchase_date'),
                car_make=doc.get('car_make'),
                car_model=doc.get('car_model'),
                car_year=doc.get('car_year')
            )
            reviews.append(review)
    return reviews

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/fbec6622-ada0-42c5-916c-2b0dc1f32005"
    api_key = "tIAe9_JDEmkvEXsIsubk-Od2FTu6LkmsijgsA-7BWU_9"

    # Define the parameters for the NLU request
    params = {
        "text": text,
        "features": {
            "sentiment": {}
        }
    }

    # Send the request to the NLU service
    response = get_request(url=url,api_key=api_key,params=params)

    # # Check the response status code
    if response.status_code != 200:
        raise ValueError("Failed to analyze sentiment: {}".format(response.text))

    # Parse the response JSON and extract the sentiment label
    data = json.loads(response.text)
    sentiment_label = data["sentiment"]["document"]["label"]

    # Return the sentiment label
    return response   