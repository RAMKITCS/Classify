import time,sys,os
from tkinter.messagebox import NO
from clean import clean

st=time.time()
#print(Predict("Classification/sport_3.txt"))
print(time.time()-st)
from fastapi import FastAPI,Request,UploadFile,Depends,status,Form,File,Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/model")
def hello(request:Request,path:str=Form(None),pythonfile:str=Form(),data:str=Form(None)):
    try:
        if path:
            sys.path.insert(1,path)
        pyfile=__import__(pythonfile)
        return pyfile.Predict(data)
    except Exception as e:
        print(str(e))
        return str(e)

    return "Hello yt"
print("hello",__name__)
if __name__ == "__main__":
    print("in same main")
    uvicorn.run("main:app",debug = True, port = 5000,host='0.0.0.0',access_log=True,reload=True,log_level=True)