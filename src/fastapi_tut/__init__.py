import uvicorn 

# Also, no need to run the file
# to start the server run this in the root folder i.e fastapi_tut - uv run uvicorn app.app:app --reload

if __name__=="__main__": 
    #it means if this file is run directly then the conditions becomes true and if the file is being imported by another file then the if body wont get executed
    uvicorn.run("app.app:app", host = "0.0.0.0", port = 8000, reload= True) # folder.file.fastapi_variable, run it on any available domain i.e the local host
    