
import logging
import os
import signal
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import pandas_market_calendars as mcal
import requests
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from minitrade.trader import BacktestLog, BacktestRunner, TradePlan, Trader
from minitrade.utils.config import config
from minitrade.utils.telegram import TelegramBot

logging.getLogger("urllib3").setLevel(logging.ERROR)
logger = logging.getLogger('uvicorn.error')

app = FastAPI(title='Minitrade runner')
bot = TelegramBot.get_instance()
if not bot:
    logger.error('Telegram bot not started')
scheduler = AsyncIOScheduler(
    # run job sequentially. yfinance lib may throw "Tkr {} tz already in cache" exception
    # when multiple processes run in parallel. Also jobs are not designed/protected against
    # race conditions.
    executors={'default': ProcessPoolExecutor(1)},
    job_defaults={'coalesce': True, 'max_instances': 1}
)


def __call_scheduler(method: str, path: str, params: dict | None = None):
    url = f'http://{config.scheduler.host}:{config.scheduler.port}{path}'
    resp = requests.request(method=method, url=url, params=params)
    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code >= 400:
        raise RuntimeError(f'Scheduler {method} {url} {params} returns {resp.status_code} {resp.text}')


def run_trader_after_backtest(plan: TradePlan, force: bool = False) -> BacktestLog | None:
    calendar = mcal.get_calendar(plan.market_calendar)
    today = datetime.now(ZoneInfo(plan.market_timezone)).replace(hour=0, minute=0, second=0, microsecond=0)
    trading_days = calendar.valid_days(start_date=(today - timedelta(days=30)).strftime('%Y-%m-%d'),
                                       end_date=today.strftime('%Y-%m-%d'), tz=plan.market_timezone)
    if today in trading_days or force:
        log = BacktestRunner(plan).execute()
        __call_scheduler('PUT', '/trader')
        return log
    else:
        logger.info(f'Plan "{plan.name}" skipped, not a trading day.')


def schedule_plan(plan: TradePlan) -> Job | None:
    ''' Schedule a trade plan'''
    if plan.enabled:
        trade_time = [datetime.strptime(t, '%H:%M:%S').time() for t in plan.trade_time_of_day.split(',')]
        trigger = OrTrigger([CronTrigger(day_of_week='mon-fri', hour=t.hour, minute=t.minute,
                             second=t.second, timezone=plan.market_timezone) for t in trade_time])
        job = scheduler.add_job(
            run_trader_after_backtest,
            trigger,
            [plan],
            misfire_grace_time=180,
            coalesce=True,
            max_instances=1,
            id=plan.id,
            name=plan.name,
            replace_existing=True
        )
        return job
    else:
        try:
            # this throws apscheduler.jobstores.base.JobLookupError if id is not found
            scheduler.remove_job(plan.id)
        except Exception:
            pass


def schedule_trader():
    ''' Load trader '''
    scheduler.add_job(
        Trader().execute,
        'cron',
        minute='*/20',
        misfire_grace_time=3600,
        id='trader_runner',
        name='trader_runner',
        replace_existing=True
    )


def load_plans() -> dict[str, Job | None]:
    ''' Reload all trade plans '''
    return {plan.name: jobinfo(schedule_plan(plan)) for plan in TradePlan.list_plans()}


def jobinfo(job: Job | None) -> dict | None:
    if job:
        return {'job_id': job.id, 'job_name': job.name, 'job_frequency': str(job.trigger), 'next_run_time': job.next_run_time}


@app.on_event('startup')
async def startup():
    bot and await bot.startup()
    scheduler.start()
    load_plans()
    schedule_trader()


@app.on_event('shutdown')
async def shutdown():
    scheduler.shutdown()
    bot and await bot.shutdown()


@app.get('/jobs')
def get_jobs():
    ''' Return the currently scheduled jobs '''
    return [jobinfo(job) for job in scheduler.get_jobs()]


@app.get('/jobs/{plan_id}')
def get_job_by_id(plan_id: str):
    ''' Return the specific job '''
    job = scheduler.get_job(job_id=plan_id)
    return jobinfo(job) if job else Response(status_code=204)


@app.put('/jobs/{plan_id}')
def put_jobs(plan_id: str):
    ''' Reschedule a single trade plan '''
    plan = TradePlan.get_plan(plan_id)
    if plan:
        job = schedule_plan(plan)
        return jobinfo(job) if job else Response(status_code=204)
    else:
        raise HTTPException(404, f'TradePlan {plan_id} not found')


@app.delete('/jobs/{plan_id}')
def delete_jobs(plan_id: str):
    ''' Unschedule a single trade plan '''
    try:
        scheduler.remove_job(plan_id)
    except Exception:
        pass
    return Response(status_code=204)


class Message(BaseModel):
    text: str | None = None
    html: str | None = None
    silent: bool | None = False


@app.post('/messages')
async def post_messages(data: Message):
    '''Send Telegram message'''
    bot and await bot.send_message(data.html or data.text, parse_mode='HTML' if data.html else None, silent=data.silent)
    return Response(status_code=204)


@app.put('/trader')
def put_trade():
    ''' Run trader immediately'''
    job = scheduler.get_job(job_id='trader_runner')
    job.modify(next_run_time=datetime.now() + timedelta(seconds=1))
    return Response(status_code=204)


@app.delete('/')
def exit_scheduler():
    ''' Stop the scheduler '''
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=204)
