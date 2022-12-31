import asyncio
import threading
from queue import Queue
import aiohttp
from time import perf_counter, sleep
import helpers


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
    url = 0
    print("Task Queue started...")    
    try:    
        while True:
            if not event.is_set():
                if q.qsize()>0:  
                    url=q.get()
                    if batch_size==0:
                        url_of_batch=url
                    if url:
                        counter+=1
                        batch_size+=1
                        
                    no=batch_size-len(results)    
                    if url is None and counter>0:
                        async with aiohttp.ClientSession() as session:
                            for i in range(no):
                                tasks.append(helpers.async_get(session,url_of_batch,i))
                            if time1==0:    
                                time1=perf_counter()                         
                            responses=  await asyncio.gather(*tasks)
                        tasks.clear()
                        results.extend(responses)
                        responses.clear()
                        send_results()
                    elif counter==limit :
                        async with aiohttp.ClientSession() as session:
                            for i in range(no):
                                tasks.append(helpers.async_get(session,url,i))
                            if time1==0:    
                                time1=perf_counter()  
                            responses= await asyncio.gather(*tasks)
                        tasks.clear()
                        results.extend(responses)
                        responses.clear()
                        if q.qsize()>0 and q.queue[0] is None:
                            send_results()
                        elapsed_time=perf_counter()-time1
                        sleep(rate-elapsed_time)
                        counter=0   
                        time1=0

                
                if perf_counter()-time1>=60 and time1>0 and counter==0:
                    counter=0   
                    time1=0

            if stop_event.is_set():   
                break 
    except KeyboardInterrupt:
        pass        

    print("Task Queue finished")