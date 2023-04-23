import requests
import json
from .models import CarDealer,Review
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):    
    try:
        response = requests.post(url,json=json_payload,params=kwargs)
        response.raise_for_status()
        print("post command used")
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong", err)
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):

    if "apikey" in kwargs :
        try:
            authenticator = IAMAuthenticator(kwargs.get("apikey"))
            natural_language_understanding = NaturalLanguageUnderstandingV1(
                version='2022-04-07',
                authenticator=authenticator
            )
            natural_language_understanding.set_service_url(url)
            response = natural_language_understanding.analyze(
                text=kwargs.get("text"),
                features=Features(sentiment=SentimentOptions())).get_result()
            #print(json.dumps(response, indent=2))
            return response
        except Exception as e:
            print("Exception occurred: {}".format(str(e)))
            return None
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
            return 404






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
    json_result = post_request(url, json_payload = data) # here is diction
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
    data = {"dealership": dealerId}
    json_result = post_request(url, json_payload = data)
    reviewlist = []

    if json_result:
        # Get the rows field from JSON response
        docs = json_result.get("docs")
        #print(docs)
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
                car_year=doc.get('car_year'),
                sentiment = analyze_review_sentiments(doc.get("review"))
            )
            
            reviewlist.append(review)
    print(reviewlist)
    return reviewlist

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/fbec6622-ada0-42c5-916c-2b0dc1f32005"
    api_key = "tIAe9_JDEmkvEXsIsubk-Od2FTu6LkmsijgsA-7BWU_9"
    # Send the request to the NLU service
    response = get_request(url=url,apikey=api_key,text = text)
    # Return the sentiment label
    return response['sentiment']['document']['label']