"""Database package bootstrap for VYOM."""

from __future__ import annotations

from app.database.database import Database
from app.database.market_repository import MarketRepository
from app.database.models import (
    MarketSnapshot,
    PortfolioRecord,
    RecommendationRecord,
    TradeRecord,
)
from app.database.portfolio_repository import PortfolioRepository
from app.database.recommendation_repository import RecommendationRepository
from app.database.trade_repository import TradeRepository


class Repositories:
    """Container for all application repositories bound to a single database."""

    __slots__ = ("market", "portfolio", "recommendation", "trade")

    def __init__(
        self,
        market: MarketRepository,
        portfolio: PortfolioRepository,
        recommendation: RecommendationRepository,
        trade: TradeRepository,
    ) -> None:
        self.market = market
        self.portfolio = portfolio
        self.recommendation = recommendation
        self.trade = trade


def create_all_tables(database: Database) -> Repositories:
    """Create repository instances and their tables for the given database."""
    repositories = Repositories(
        market=MarketRepository(database),
        portfolio=PortfolioRepository(database),
        recommendation=RecommendationRepository(database),
        trade=TradeRepository(database),
    )

    for repository in (
        repositories.market,
        repositories.portfolio,
        repositories.recommendation,
        repositories.trade,
    ):
        repository.create_table()

    return repositories


__all__ = [
    "Database",
    "Repositories",
    "MarketRepository",
    "PortfolioRepository",
    "RecommendationRepository",
    "TradeRepository",
    "MarketSnapshot",
    "PortfolioRecord",
    "RecommendationRecord",
    "TradeRecord",
    "create_all_tables",
]