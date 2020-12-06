from fastapi import FastAPI


app = FastAPI()


@app.post("/")
def process_incoming_stream():
    """
    docstring
    """
    pass
