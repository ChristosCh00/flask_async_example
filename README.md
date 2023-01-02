# flask_async_example
A simple Flask app to demonstrate async endpoints.

This repo includes 3 endpoints with 3 different implementations of consuming the same API, each by adding some degree of complexity.

Thanks to the free API https://catfact.ninja/ that was used in this demo.

# Scenario - Applied constraints:
a) Flask must be used. Flask[async] can be used to have async endpoint functions, however there are limitiations. There are other modules that are async-first, such as Quart.
b) The API that our endpoints are consuming can only be hit once to provide a single cat fact. Even though the Cat Facts API has the ability to return a list of facts for 1 request, we will pretend that this is not an option and that our only option is to use the /fact endpoint. That is to simulate similar 1-to-1 with high volume of requests.



# Usage

NOTES: 
1) The Cat Facts API (at least the /fact endpoint) seems to have a limit of 100 requests per minute.
2) See the console outputs to better understand the sequence that the requests are made, to see the status codes and the elapsed time of each endpoint.

a) http://127.0.0.1:5000/cat/{int:N} -GET

 This will return N cat facts. This endpoint will perform N requests to the external API in a synchronous manner, collect the their results and return them in a list. If the external API limit is exceeded it will retrun an error.
 
b) http://127.0.0.1:5000/cat_async/{int:N} -GET

 This will return N cat facts. This endpoint will perform N requests to the external API in an asynchronous manner, collect the their results and return them in a list. In this case it is quite possible that the external API limitis will be exceeded. If that happens and we will start getting 429 responses. These will discarded and only the 200 will be returned. So there is a chance that we get fewer cat facts than what we asked for.
 
c) http://127.0.0.1:5000/cat_async_limited/{int:N} -GET

 This will return N cat facts. This endpoint will perform N requests to the external API in an asynchronous manner, collect the their results and return them in a list. In this case, the set up gets more complex in order to solve the limit issue from the /cat_async endpoint. The endpoint sumbits the request info to task queue running on a background thread that has it's own event loop. There the requests are constructed and performed in a way that guarantees that the external API limits are respected. The background thread keeps track of time and of the items going through the queue and when limit is met it sleeps for the time need to reset.
 
# Installation
Please intall the dependencies from the requirements.txt and run WSGI.py. The API will be listening on http://127.0.0.1:5000.

