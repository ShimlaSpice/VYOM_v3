"""
Main application controller for VYOM.
"""

from loguru import logger

from config import ConfigManager
from core.logger import LoggerManager


class Application:
    """Main application lifecycle controller."""

    def __init__(self) -> None:
        self.settings = ConfigManager.get_settings()

    def initialize(self) -> None:
        """Initialize all core components."""

        LoggerManager.configure()

        logger.info("=" * 60)
        logger.info(f"Starting {self.settings.APP_NAME} v{self.settings.APP_VERSION}")
        logger.info("=" * 60)

        logger.info("Configuration loaded.")
        logger.info("Logging initialized.")

    def run(self) -> None:
        """Run the application."""

        self.initialize()

        logger.success("Application started successfully.")

        from app.pipeline.market_pipeline import MarketPipeline

        pipeline = MarketPipeline()

        recommendations = pipeline.run()

        logger.success(
            f"Generated {len(recommendations)} recommendations."
        )

        for recommendation in recommendations:

            logger.info(
                f"{recommendation.symbol:<15}"
                f"{recommendation.recommendation:<12}"
                f"Confidence: {recommendation.confidence}"
            )

    def shutdown(self) -> None:
        """Gracefully shut down the application."""

        logger.info("Shutting down application...")
        logger.success("Application stopped.")