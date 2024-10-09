from statistics import mean, stdev
from fastapi import APIRouter, HTTPException
from peewee import fn
from datetime import date, timedelta

from app.controllers.newspaper_controller import get_newspaper_controller
from app.entities.news_article_entity import NewsArticleEntity
from app.entities.newspaper_entity import NewspaperEntity
from app.models.articles_by_day_report import ArticlesByDayReport

report_router = APIRouter()


def get_report_router():
    return report_router


@report_router.get("/verify-articles/{newspaper_id}")
async def verify_articles(newspaper_id: int):
    today = date.today()
    weekday = today.weekday()

    # Calculate the date 6 months ago
    six_months_ago = today - timedelta(days=6 * 30)  # Approximation of 6 months

    # Verify if the newspaper with the given ID exists
    newspaper = await get_newspaper_controller().get_by_id(newspaper_id)
    if not newspaper:
        raise HTTPException(status_code=404, detail="Newspaper not found")

    # Query articles uploaded on the same day of the week, excluding today, over the last 6 months
    articles_query = NewsArticleEntity.select(
        fn.COUNT(NewsArticleEntity.id).alias("count"),
        fn.WEEKDAY(NewsArticleEntity.date_uploaded).alias("weekday"),
        NewsArticleEntity.date_uploaded,
    ).where(
        (NewsArticleEntity.newspaper_id == newspaper_id)
        & (NewsArticleEntity.date_uploaded >= six_months_ago)
        & (NewsArticleEntity.date_uploaded < today)
        & (fn.WEEKDAY(NewsArticleEntity.date_uploaded) == weekday)
    )

    # Collect the article counts from the query
    articles_count = [row.count for row in list(articles_query)]

    if not articles_count:
        raise HTTPException(status_code=404, detail="No data found for this newspaper")

    # Phase 1: Calculate the average and threshold (80% of average)
    avg_articles = mean(articles_count)
    threshold = avg_articles * 0.8  # 80% threshold

    # Query to count today's articles
    today_count_query = NewsArticleEntity.select(
        fn.COUNT(NewsArticleEntity.id).alias("count")
    ).where(
        (NewsArticleEntity.newspaper_id == newspaper_id)
        & (NewsArticleEntity.date_uploaded == today)
    )
    today_count = today_count_query.scalar()

    # Check if today's count is below the threshold
    if today_count < threshold:
        # Phase 2: Calculate the Coefficient of Variation (CV)
        if len(articles_count) > 1:  # stdev requires at least 2 values
            std_dev = stdev(articles_count)
            cv = std_dev / avg_articles
        else:
            cv = 0

        # If CV is high, calculate interquartile range (IQR)
        if cv > 0.5:  # Arbitrary threshold for high variability
            sorted_articles = sorted(articles_count)
            q1 = sorted_articles[len(sorted_articles) // 4]
            q3 = sorted_articles[(len(sorted_articles) * 3) // 4]
            iqr = q3 - q1

            # Check if today's count is below Q1
            if today_count < q1:
                return {
                    "message": f"Today's article count is below the first quartile (Q1={q1})."
                }
            else:
                return {
                    "message": f"Today's article count is within acceptable interquartile range (IQR={iqr})."
                }

        # Phase 3: If CV is low, check frequency distribution
        else:
            freq_dist = {x: articles_count.count(x) for x in set(articles_count)}
            most_frequent_count = max(freq_dist, key=freq_dist.get)

            # Check if today's count is within the most frequent category
            if today_count == most_frequent_count:
                return {
                    "message": f"Today's article count matches the most frequent count ({most_frequent_count})."
                }
            else:
                return {
                    "message": f"Today's article count ({today_count}) does not match the most frequent count ({most_frequent_count})."
                }
    else:
        return {
            "message": f"Today's article count ({today_count}) is above the 80% threshold ({threshold:.2f})."
        }


@report_router.get(
    "/report-articles-by-day/{newspaper_id}", response_model=list[ArticlesByDayReport]
)
async def report_articles_by_day(newspaper_id: int):
    today = date.today()

    # Find the Monday of the current week
    last_monday = today - timedelta(days=today.weekday())

    # Find the Monday of the previous week (7 days before the last Monday)
    start_date = last_monday - timedelta(days=7)

    # Verify if the newspaper with the given ID exists
    newspaper = get_newspaper_controller().get_by_id(newspaper_id)

    # Generate a list of dates starting from the previous Monday (7 days range)
    date_range = [start_date + timedelta(days=i) for i in range(7)]

    # Query to count articles grouped by date_uploaded, filtering by newspaper_id
    query = (
        NewsArticleEntity.select(
            NewsArticleEntity.date_uploaded,
            fn.COUNT(NewsArticleEntity.id).alias("count"),
        )
        .where(
            (NewsArticleEntity.newspaper_id == newspaper_id)
            & (NewsArticleEntity.date_uploaded >= start_date)
            & (NewsArticleEntity.date_uploaded < last_monday)
        )
        .group_by(NewsArticleEntity.date_uploaded)
        .order_by(NewsArticleEntity.date_uploaded)
    )

    # Fetch the data
    articles_by_day = {row.date_uploaded: row.count for row in query}

    # Ensure each day in the last week is represented, even with 0 articles
    report = [
        ArticlesByDayReport(date=day, article_count=articles_by_day.get(day, 0))
        for day in date_range
    ]

    return report
