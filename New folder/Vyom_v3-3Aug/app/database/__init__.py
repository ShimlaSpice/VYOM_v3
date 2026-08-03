"""
VYOM Database Package.

Composition root for the persistence layer: construct a Database, then
call create_all_tables() once at startup to get back every repository,
ready to use, with its schema already created.
"""

from __future__ import annotations

from app.database.database import Database
from app.database.market_repository import MarketRepository
from app.database.portfolio_repository import PortfolioRepository
from app.database.recommendation_repository import RecommendationRepository
from app.database.repository import Repository
from app.database.trade_repository import TradeRepository


class Repositories:
    """Typed bundle of every repository, wired to one Database."""

    __slots__ = ("market", "recommendation", "trade", "portfolio")

    def __init__(
        self,
        market: MarketRepository,
        recommendation: RecommendationRepository,
        trade: TradeRepository,
        portfolio: PortfolioRepository,
    ) -> None:
        self.market = market
        self.recommendation = recommendation
        self.trade = trade
        self.portfolio = portfolio


def create_all_tables(database: Database) -> Repositories:
    """Construct every repository against `database` and ensure their
    tables exist. This is the single entry point the rest of VYOM
    should use to stand up persistence."""
    repositories = Repositories(
        market=MarketRepository(database),
        recommendation=RecommendationRepository(database),
        trade=TradeRepository(database),
        portfolio=PortfolioRepository(database),
    )

    repositories.market.create_table()
    repositories.recommendation.create_table()
    repositories.trade.create_table()
    repositories.portfolio.create_table()

    return repositories


__all__ = [
    "Database",
    "Repository",
    "MarketRepository",
    "RecommendationRepository",
    "TradeRepository",
    "PortfolioRepository",
    "Repositories",
    "create_all_tables",
]