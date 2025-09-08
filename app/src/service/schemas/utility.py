from datetime import date, datetime

from fastapi import Query

from .message import MessagesQuery


def query_params(
    start_date: datetime | date = Query(..., description="Start date"),
    end_date: datetime | date = Query(..., description="End date"),
    order: str = Query(default="asc", description="Order by time"),
) -> MessagesQuery:
    return MessagesQuery(start_date=start_date, end_date=end_date, order=order)
