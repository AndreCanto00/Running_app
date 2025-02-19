from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from mylib.load import trimp, trimp_lt, hrrs


app = FastAPI()


class Run(BaseModel):
    avg_hr: float
    max_hr: float
    rest_hr: float
    workout_duration: float
    lt_hr: float


@app.get("/")
async def root():
    """Home Page with GET HTTP Method"""

    return {"message": "Hello, I am your load running calculator!"}


# Creaimo una funzione per calcolare il TRIMP partendo dai dati inseriti dall'utente in FastAPI

@app.post("/trimp/")
async def trimp_post(run: Run):
    """Calculate TRIMP value"""
    try:
        avg_hr = run.avg_hr
        max_hr = run.max_hr
        rest_hr = run.rest_hr
        workout_duration = run.workout_duration

        trimp_value = trimp(avg_hr, max_hr, rest_hr, workout_duration)
        return {"TRIMP value": trimp_value}
    except ValueError as e:
        return {"Error": str(e)}


# Creaimo una funzione per calcolare il TRIMP_LT partendo dai dati inseriti dall'utente
@app.post("/trimp_lt/")
async def trimp_lt_post(run: Run):
    """Calculate TRIMP_LT value"""
    try:
        lt_hr = run.lt_hr
        max_hr = run.max_hr
        rest_hr = run.rest_hr

        trimp_lt_value = trimp_lt(lt_hr, max_hr, rest_hr)
        return {"TRIMP_LT value": trimp_lt_value}
    except ValueError as e:
        return {"Error": str(e)}


# Creaimo una funzione per calcolare l'HRRS partendo dai dati inseriti dall'utente
@app.post("/hrrs/")
async def hrrs_post(run: Run):
    """Calculate HRRS value"""
    try:
        avg_hr = run.avg_hr
        max_hr = run.max_hr
        rest_hr = run.rest_hr
        workout_duration = run.workout_duration
        lt_hr = run.lt_hr

        hrrs_value = hrrs(avg_hr, max_hr, rest_hr, workout_duration, lt_hr)
        return {"HRRS value": hrrs_value}
    except ValueError as e:
        return {"Error": str(e)}


if __name__ == "__main__":

    uvicorn.run(app, port=8080, host="0.0.0.0")
