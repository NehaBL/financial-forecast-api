from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Record(BaseModel):
    Revenue: float
    Profit: float
    Headcount: int

class InputData(BaseModel):
    data: List[Record]

@app.post("/forecast")
async def forecast(data: InputData):
    results = []
    for row in data.data:
        margin = round((row.Profit / row.Revenue) * 100, 2)
        alert = None
        if row.Revenue < 100000:
            alert = "Low Revenue"
        if margin < 20:
            alert = "Low Profit Margin"
        if row.Headcount > 25 and margin < 20:
            alert = "Resource Inefficiency"
        results.append({
            "Revenue": row.Revenue,
            "Profit": row.Profit,
            "Margin": margin,
            "Headcount": row.Headcount,
            "Alert": alert
        })
    return {"summary": results}
