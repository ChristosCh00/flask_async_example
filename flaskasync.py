from flask import Flask,request, jsonify
from time import perf_counter
import asyncio
from helpers import *

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
    cats=await get_cat_fact_async(num)

    time=perf_counter()-time
    print(f'Endpoint response time: {time}')
    return jsonify(cats),200   

@app.route('/cat_async_limited/<int:num>',methods=['GET'])
async def cat_async_limit(num):
    time=perf_counter()
    cats=await get_cat_fact_async_with_limit(num)

    time=perf_counter()-time
    print(f'Endpoint response time: {time}')
    return jsonify(cats),200   

