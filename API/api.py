import uvicorn 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import relations_graph_extractor

current_app_key = os.environ['app_key']
openport = int(os.environ['PORT'])

class ArticleInput(BaseModel):

    article: str


app = FastAPI()


@app.get('/')
def engine_name(response: JSONResponse):
    
    name ="API relation extraction"
    version = "February 2022"
    port = openport
    
    result = {
		"name":name,
		"version":version,
		"port":port
	}
    
    return result


@app.post('/get_relations', status_code = 200)
def get_relation(input_:ArticleInput, request: Request, response: JSONResponse):
    """
    Get relations data from article
    """
    app_key = request.headers.get('app-key')
    if app_key != current_app_key:
        response.status_code = 403
        status=0
        return {'status':status}
        
    try:
        input_ = input_.dict()
        result = relations_graph_extractor.article_get_relation(input_['article'].lower())
        status = 1 # Success
    except Exception as e:
        result = 0
        status = 0 #  Failed
        print(e)

    return {'status': status, 'relations_data':result}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=openport)