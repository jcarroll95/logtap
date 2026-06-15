import io
from fastapi import FastAPI, Query, UploadFile, HTTPException
from logtap.analyze import analyze
from logtap.reporter import build_dict
import logging
app = FastAPI()


logger = logging.getLogger(__name__)
@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/jobs")
def create_job(upload: UploadFile, top_n: int = Query(default=5, ge=1, le=100)):
    try:
        input_stream = io.TextIOWrapper(upload.file, encoding="utf-8")
        output = analyze(input_stream, top_n)
    except UnicodeDecodeError as e:
        logger.info(upload.filename)
        logger.info(e)
        raise HTTPException(
            status_code=400, 
            detail="Uploaded file must be UTF-8 encoded text"
        )
    
    return build_dict(output)
