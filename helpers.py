import json
import requests
import asyncio
import aiohttp
import limiter

def get_cat_fact(num):
    url='https://catfact.ninja/fact'
    print(f'Request {num} started.')
    response=requests.get(url)
    print (f'Request {num} finished. Status {response.status_code}.')
    if response.status_code==200:        
        obj=json.loads(response.text)
        return obj['fact']
    else:
        raise None

def sync_get(url,i):
    print(f'Request {i} started.')
    response=requests.get(url)
    print (f'Request {i} finished. Status {response.status_code}.')

async def async_get(session, url,i):
    print(f'Request {i} started.')
    response=await session.get(url)
    print (f'Request {i} finished. Status {response.status}.')

    return response
    
async def get_cat_fact_async(num):
    url='https://catfact.ninja/fact'
    results=[]
    async with aiohttp.ClientSession() as session:
        
        tasks=[]
        for i in range(num):
            tasks.append(async_get(session,url,i))

        responses= await asyncio.gather(*tasks)   
    count=0   
    for response in responses:
        status=response.status
        if status==200:
            json=await response.json()
            results.append(json['fact'])
            count+=1
    print(f'Successful count = {count}')
               
    return  results



async def get_cat_fact_async_with_limit(num):
    url='https://catfact.ninja/fact'
    results=[]
    for i in range(num):
        options=limiter.RequestOptions(url,'GET',i)
        limiter.q.put(options)
    
    limiter.q.put(None) ## signal that the batch is over
    limiter.event.wait()  
    responses= limiter.results.copy()
    limiter.results=[]
    limiter.event.clear()
    count=0   
    for response in responses:
        status=response.status
        if status==200:
            json=await response.json()
            results.append(json['fact'])
            count+=1
    print(f'Successful count = {count}')
            
    return  results
