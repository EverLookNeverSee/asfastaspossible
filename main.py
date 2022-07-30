from fastapi import FastAPI, Response

# Defining the api object
app = FastAPI()


@app.get("/")
def root():
    return Response(status_code=200, content="The server is running.")
