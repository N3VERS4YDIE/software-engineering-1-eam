from fastapi import APIRouter, HTTPException
from peewee import fn
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from app.entities.news_article_entity import NewsArticleEntity

test_router = APIRouter()


@test_router.get("/test/central-tendency")
async def test_central_tendency(newspaper_id: int):
    # Fetching articles count for central tendency calculation
    articles_query = (
        NewsArticleEntity.select(fn.COUNT(NewsArticleEntity.id).alias("count"))
        .where(NewsArticleEntity.newspaper_id == newspaper_id)
        .group_by(NewsArticleEntity.date_uploaded)  # Group by date
    )

    articles_count = [row.count for row in articles_query]

    if not articles_count:
        raise HTTPException(
            status_code=404, detail="No articles found for this newspaper"
        )

    mean_calculated = float(np.mean(articles_count))  # Convert to float
    expected_mean = 100  # Replace with your expected value

    return {
        "calculated_mean": mean_calculated,
        "expected_mean": expected_mean,
        "is_mean_correct": mean_calculated < (expected_mean * 0.8),  # Threshold of 80%
    }


@test_router.get("/test/dispersion")
async def test_dispersion(newspaper_id: int):
    # Fetching articles count for dispersion calculation
    articles_query = (
        NewsArticleEntity.select(fn.COUNT(NewsArticleEntity.id).alias("count"))
        .where(NewsArticleEntity.newspaper_id == newspaper_id)
        .group_by(NewsArticleEntity.date_uploaded)  # Group by date
    )

    articles_count = [row.count for row in articles_query]

    if not articles_count:
        raise HTTPException(
            status_code=404, detail="No articles found for this newspaper"
        )

    std_dev_calculated = float(np.std(articles_count, ddof=1))  # Convert to float
    expected_std_dev = 15  # Replace with your expected value

    return {
        "calculated_std_dev": std_dev_calculated,
        "expected_std_dev": expected_std_dev,
        "is_std_dev_correct": std_dev_calculated
        < (expected_std_dev * 0.8),  # Threshold of 80%
    }


@test_router.get("/test/regression")
async def test_regression(newspaper_id: int):
    # Fetching articles data for regression analysis
    articles_query = (
        NewsArticleEntity.select(
            NewsArticleEntity.date_uploaded,
            fn.COUNT(NewsArticleEntity.id).alias("count"),
        )
        .where(NewsArticleEntity.newspaper_id == newspaper_id)
        .group_by(NewsArticleEntity.date_uploaded)
        .order_by(NewsArticleEntity.date_uploaded)
    )

    dates = [row.date_uploaded.toordinal() for row in articles_query]
    counts = [row.count for row in articles_query]

    if len(dates) < 2:  # Need at least 2 points for regression
        raise HTTPException(status_code=404, detail="Not enough data for regression")

    # Reshape the data for the regression model
    dates = np.array(dates).reshape(-1, 1)
    model = LinearRegression()
    model.fit(dates, counts)

    # Simulate using Monte Carlo method to get expected values
    simulated_counts = np.random.normal(
        loc=model.predict(dates), scale=np.std(counts), size=(1000,)
    )
    expected_value = float(np.mean(simulated_counts))  # Convert to float
    calculated_average = float(np.mean(counts))  # Convert to float

    return {
        "expected_value": expected_value,
        "calculated_average": calculated_average,
        "is_average_matching": np.isclose(
            expected_value, calculated_average, rtol=0.1
        ).item(),  # Convert to boolean
    }


@test_router.get("/test/canonical")
async def test_canonical(newspaper_id: int):
    # Fetching articles count for canonical analysis
    articles_query = (
        NewsArticleEntity.select(fn.COUNT(NewsArticleEntity.id).alias("count"))
        .where(NewsArticleEntity.newspaper_id == newspaper_id)
        .group_by(NewsArticleEntity.date_uploaded)  # Group by date
    )

    articles_count = [row.count for row in articles_query]

    if not articles_count:
        raise HTTPException(
            status_code=404, detail="No articles found for this newspaper"
        )

    # Assuming we have some expected count data
    expected_count_data = np.array([50, 100, 150])  # Example expected counts
    observed_count_data = np.array(articles_count)

    # Perform Canonical Analysis (use dummy class labels)
    lda = LinearDiscriminantAnalysis()
    lda.fit(
        observed_count_data.reshape(-1, 1), np.zeros_like(observed_count_data)
    )  # Dummy classes

    # Get probabilities for expected counts
    probabilities = lda.predict_proba(expected_count_data.reshape(-1, 1))

    return {
        "expected_count": expected_count_data.tolist(),
        "observed_count": observed_count_data.tolist(),
        "probabilities": probabilities.tolist(),
    }


def get_test_router():
    return test_router
