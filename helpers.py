import json
import requests
import asyncio
import aiohttp

def get_cat_fact(num):
    url='https://catfact.ninja/fact'
    print(f'Request {num} started.')
    response=requests.get(url)
    print (f'Request {num} finished')
    if response.status_code==200:        
        obj=json.loads(response.text)
        return obj['fact']
    else:
        raise None

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
                count+=1
        print(f'Successful count = {count}')

        if count==num:
            for response in responses:
                json=await response.json()
                results.append(json['fact'])
        return  results



async def async_get(session, url,i):
    print(f'Request {i} started.')
    response=await session.get(url)
    print (f'Request {i} finished. Status {response.status}')

    return response