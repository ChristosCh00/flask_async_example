from flask import Flask,request, jsonify
import requests
import json
from time import perf_counter
import asyncio

app=Flask(__name__)

@app.route('/hello/')
def hello():
    return 'Hello'

@app.route('/cat/<int:num>',methods=['GET'])
def cat(num):
    time=perf_counter()
    cats=[]
    for n in range(num):
        fact=get_cat_fact(n)
        cats.append(fact)

    time=perf_counter()-time
    print(f'Endpoint response time: {time}')
    return jsonify(cats),200

@app.route('/cat_async/<int:num>',methods=['GET'])
async def cat_async(num):
    time=perf_counter()
    cats=[]
    for n in range(num):
        fact=await get_cat_fact_async(n)
        cats.append(fact)

    time=perf_counter()-time
    print(f'Endpoint response time: {time}')
    return jsonify(cats),200   

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