# LiveRoomBot Backend - 36 Unique AI Companions! 🌟

A Python FastAPI backend for the LiveRoom AI Companion Platform, featuring 36 unique character-based conversations powered by OpenAI GPT-4, plus Telegram community integration!

## 🚀 New Features

- **36 Unique AI Characters** across 6 categories - each with distinct personalities!
- **Telegram Bot Integration** for community engagement
- **Enhanced AI Responses** with GPT-4 and engagement algorithms
- **Community Features** - rankings, discussions, recommendations
- **Addictive Conversation Patterns** designed to keep users engaged

## 🎭 Character Categories (6 characters each)

### 💕 Romantic Companions
Luna, Valentina, Scarlett, Elena, Aurora, Victoria

### 😘 Flirty Chat
Sophia, Maya, Chloe, Jasmine, Riley, Amber

### 🌈 Mood Boosters
Aria, Sunny, Joy, Bliss, Spark, Hope

### 🎪 Fantasy Roleplay
Isabella (Vampire Queen), Seraphina (Angel), Morgana (Sorceress), Luna Wolf, Celeste (Space Princess), Nyx (Shadow Dancer)

### 💬 Intimate Conversations
Zara, Eva, Diana, Ruby, Phoenix, Velvet

### 🎮 Entertainment & Fun
Astro Baba (Cosmic Comedian), Jester, Melody, Pixel (Gaming Goddess), Nova, Sage

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/LiveRoomBot/LiveRoomBot-Backend.git
cd LiveRoomBot-Backend

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Required: OPENAI_API_KEY
```

### 3. Database Setup

```bash
# Initialize database with sample data
python app/scripts/init_data.py
```

### 4. Run the Server

```bash
# Development server
python run.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.