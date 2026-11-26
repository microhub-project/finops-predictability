import uvicorn, json
from redis import Redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from predict import suggest_scale, predict_year, predict_infra, predict_year_infra
from analysis import infra_analysis_year

class Prediction(BaseModel):
    cpu: int
    ram: float
    monthly_cost: float
    infra_multiplier: float
    scale_type: str
    
class YearPrediction(BaseModel):
    mac: str
    cpu: int
    ram: float
    monthly_cost: float
    infra_multiplier: list[float]
    
class Instance(BaseModel):
    mac: str
    cpu: int
    ram: float
    monthly_cost: float
    
class InfraPrediction(BaseModel):
    instances: list[Instance]
    infra_multiplier: float
    
class InfraYearPrediction(BaseModel):
    instances: list[Instance]
    infra_multiplier: list[float]
    
class Infra(BaseModel):
    company: str
    instances: int
    cpus: int
    ram: float

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(host="localhost", port=6379, decode_responses=True)
    yield
    app.state.redis.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict/")
def predict_endpoint(prediction: Prediction):
    return suggest_scale(prediction.cpu, prediction.ram, prediction.monthly_cost, prediction.infra_multiplier, prediction.scale_type)
    
@app.post("/predict-year/")
def predict_year_endpoint(prediction: YearPrediction):
    return predict_year(prediction.mac, prediction.cpu, prediction.ram, prediction.monthly_cost, prediction.infra_multiplier)
    
@app.post("/predict-infra/")
def predict_infra_endpoint(prediction: InfraPrediction):
    return predict_infra(prediction.instances, prediction.infra_multiplier)

@app.post("/predict-year-infra/")
def predict_year_infra_endpoint(prediction: InfraYearPrediction):
    return predict_year_infra(prediction.instances, prediction.infra_multiplier)

@app.post("/infra-analysis-year/")
def infra_analysis_year_endpoint(infra: Infra):
    key = f"infra_analysis_year:{infra.company}"
    cached = app.state.redis.get(key)
    
    if cached is not None:
        return json.loads(cached)
    
    response = infra_analysis_year(infra.company)
    app.state.redis.set(key, json.dumps(response), ex=3600)
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)