from __future__ import annotations
from typing import Coroutine
import asyncio
import threading
from queue import Queue
import aiohttp
from time import perf_counter, sleep
import helpers


class RequestOptions:
    '''
    A class to be used for sending all the necssary info 
    to construct an request from the helpers module.
    '''
    #### TODO #### Should include more functionality to this class, 
    # but there's no need for now
    def __init__(self,url,method,request_index):
        self.method=method
        self.url=url
        self.request_index=request_index ## just for logging purposes

    def produce_request_from_options(session:aiohttp.ClientSession,options:RequestOptions) -> Coroutine:
        if options.method=='GET':
            return helpers.async_get(session,options.url,options.request_index)
        else:
            raise ValueError ("Only 'GET' is currently supported.")


q=Queue(maxsize=0) ## infinite size queue
event=threading.Event()
stop_event=threading.Event()


def submit_item_to_queue(item):
    global q
    q.put_nowait(item)
    


def limit_wrapper():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(callback())
    loop.close()


#timeout = aiohttp.ClientTimeout(total=120)
limit=100
rate=60
results=[]
batch_size=0
url_of_batch=0

def send_results():
    global batch_size,url_of_batch,event
    batch_size=0
    url_of_batch=0
    event.set()

async def callback():

    global q, event, limit,rate,counter, results,batch_size,url_of_batch, stop_event
    tasks=[]
    responses=[]  
    time1=0    
    counter=0
    options=[]
    print("Task Queue started...")    
    try:    
        while True:
            if not event.is_set():
                if q.qsize()>0:  
                    item=q.get()
                    if item:
                        options.append(item)
                        counter+=1
                        batch_size+=1
                        
                    no=batch_size-len(results)    
                    if item is None and counter>0:
                        async with aiohttp.ClientSession() as session:
                            for i in range(no):
                                tasks.append(RequestOptions.produce_request_from_options(session,options[i]))
                                time1=perf_counter()                         
                            responses=  await asyncio.gather(*tasks)
                        tasks.clear()
                        options.clear()
                        results.extend(responses)
                        responses.clear()
                        send_results()
                    elif counter==limit :
                        async with aiohttp.ClientSession() as session:
                            for i in range(no):
                                tasks.append(RequestOptions.produce_request_from_options(session,options[i]))
                            if time1==0:    
                                time1=perf_counter()  
                            responses= await asyncio.gather(*tasks)
                        tasks.clear()
                        options.clear()
                        results.extend(responses)
                        responses.clear()
                        if q.qsize()>0 and q.queue[0] is None:
                            send_results()
                        elapsed_time=perf_counter()-time1
                        sleep_time=rate-elapsed_time
                        print(f"Sleeping for {sleep_time} seconds to reset API limit...")
                        sleep(rate-elapsed_time)
                        counter=0   
                        time1=0

                
                if perf_counter()-time1>=60 and time1>0:
                    counter=0   
                    time1=0

            if stop_event.is_set():   
                break 
    except KeyboardInterrupt:
        pass        

    print("Task Queue finished")