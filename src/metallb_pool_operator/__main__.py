import logging
from datetime import datetime

import structlog
from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.schedulers.blocking import BlockingScheduler

from metallb_pool_operator.env import Env
from metallb_pool_operator.kube import patch_ipv6_pool
from metallb_pool_operator.ros import get_ipv6_pools

# Completely disable APScheduler logs
logging.getLogger("apscheduler").disabled = True
log: structlog.stdlib.BoundLogger = structlog.get_logger()


def listener(event: JobExecutionEvent) -> None:
    if event.exception:
        log.exception("job failed", exc_info=event.exception)
        sched.shutdown(wait=False)


def tick() -> None:
    e = Env.load()
    log.info("starting tick")

    pools = get_ipv6_pools()
    log.info("got pools", addresses=pools)

    patch_ipv6_pool(name=e.pool_name, namespace=e.pool_namespace, new_addresses=pools)
    log.info("patched pool", name=e.pool_name, namespace=e.pool_namespace)


sched = BlockingScheduler()
sched.add_listener(listener, EVENT_JOB_ERROR)
sched.add_job(tick, "interval", seconds=3600, next_run_time=datetime.now())
sched.start()
