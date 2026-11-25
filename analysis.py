from dotenv import load_dotenv
from datetime import datetime
from s3 import connect
import os, json

load_dotenv()

client = connect()

def get_historical_file(company_name):
    company_name = company_name.lower()
    file_key = f"03-client-gold/{company_name}_historical.json"
    
    try:
        response = client.get_object(Bucket=os.getenv("bucket"), Key=file_key)
        content = response["Body"].read().decode("utf-8")
        return json.loads(content)
    except:
        return None

def infra_analysis_year(company_name):
    file = get_historical_file(company_name)
    if file is None:
        raise ValueError(f"Não foi encontrado o arquivo de dados históricos da empresa {company_name}")
    
    now = datetime.now()
    cpus_month = [0] * now.month
    ram_month = [0.0] * now.month
    
    for instance in file["instancias"]:
        cpu_max = [0] * now.month
        ram_max = [0.0] * now.month

        for reading in instance["leituras"]:
            timestamp = datetime.fromisoformat(reading["timestamp"])

            if timestamp.year != now.year or timestamp.month > now.month:
                continue

            idx = timestamp.month - 1
            cpu_max[idx] = max(cpu_max[idx], reading["tipo"]["cpu"])
            ram_max[idx] = max(ram_max[idx], reading["tipo"]["ram"])

        for idx in range(now.month):
            cpus_month[idx] += cpu_max[idx]
            ram_month[idx] += ram_max[idx]

    return {"cpus_month": cpus_month, "ram_month": ram_month}