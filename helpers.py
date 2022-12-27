def get_cat_fact(num):
    url='https://catfact.ninja/fact'
    print(f'Cat fact {num} request started.')
    response=requests.get(url)
    print (f'Cat fact {num} request finished')
    if response.status_code==200:        
        obj=json.loads(response.text)
        return obj['fact']
    else:
        raise None

async def get_cat_fact_async(num):
    url='https://catfact.ninja/fact'
    print(f'Cat fact {num} request started.')
    response= await requests.get(url)
    print (f'Cat fact {num} request finished')
    if response.status_code==200:        
        obj=json.loads(response.text)
        return obj['fact']
    else:
        raise None