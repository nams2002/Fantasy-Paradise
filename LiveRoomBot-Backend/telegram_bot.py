#!/usr/bin/env python3
"""
Telegram Bot for LiveRoom - AI Companion Platform
Run this script to start the Telegram bot for community engagement
"""

import asyncio
import logging
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.telegram_service import TelegramBotService
from app.core.config import settings

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the Telegram bot"""
    
    # Check if Telegram bot token is configured
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not configured. Please set it in your environment variables or .env file")
        logger.info("To get a bot token:")
        logger.info("1. Message @BotFather on Telegram")
        logger.info("2. Send /newbot command")
        logger.info("3. Follow the instructions to create your bot")
        logger.info("4. Copy the token and set TELEGRAM_BOT_TOKEN environment variable")
        return
    
    logger.info("Starting LiveRoom Telegram Bot...")
    logger.info(f"Bot token configured: {settings.TELEGRAM_BOT_TOKEN[:10]}...")
    
    # Create and run the bot service
    bot_service = TelegramBotService()
    
    try:
        await bot_service.run(settings.TELEGRAM_BOT_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown complete")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)
