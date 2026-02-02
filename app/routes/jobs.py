from fastapi import APIRouter

from app.jobs.stock_monitor_job import run_stock_monitor_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/stock-monitor")
def run_stock_monitor_job_endpoint():
    '''
    Dispara manualmente o job de monitoramento de estoques.
    '''
    run_stock_monitor_job()
    return {"message": "Stock monitor job started"}
