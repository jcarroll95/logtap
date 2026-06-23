import io
from fastapi import FastAPI, Query, UploadFile, HTTPException, Depends
from logtap.analyze import analyze
from logtap.schemas import JobResponse, ItemCount
from sqlalchemy.ext.asyncio import AsyncSession
from logtap.database import get_db
import logging
app = FastAPI()


logger = logging.getLogger(__name__)
@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/jobs", response_model=JobResponse)
async def create_job(
        upload: UploadFile,
        db: AsyncSession = Depends(get_db),
        top_n: int = Query(default=5, ge=1, le=100)):
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

    # we need to store output somewhere, a list with the uuid
    # output is a Record dataclass
    # db.add() is a sqlalchemy function expecting an object from my schema: a jobrecord
    # I need to map output into a new jobresponse instance then add THAT to the db
    db.add(output)
    await db.commit()
    # we need to return job id and status

@app.get("/jobs/{job_id}")
def read_job(job_id: str):
    # we need to pull that job id's data out of the list

    # Convert tuples to ItemCount models
    top_ips = [ItemCount(name=ip, count=count) for ip, count in output.top_ips]
    top_paths = [ItemCount(name=path, count=count) for path, count in output.top_paths]

    # Return the JobResponse
    return JobResponse(
        lines_total=output.lines_total,
        lines_parsed=output.lines_parsed,
        lines_skipped=output.lines_skipped,
        status_classes=output.status_classes,
        total_bytes=output.total_bytes,
        top_ips=top_ips,
        top_paths=top_paths,
        timespan_start=output.timespan_start,
        timespan_end=output.timespan_end,
        error_rate=output.error_rate
    )