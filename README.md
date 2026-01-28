# God Incorporated

A modular AI-powered oracle platform exploring wisdom, inquiry, and value-for-value interaction.

## Overview

God Incorporated is a FastAPI-based backend service that provides an intelligent oracle platform. It combines AI-powered wisdom generation, inquiry management, voice interaction, and value-for-value participation in a modular, extensible architecture.

## Features

### 🧠 Inquiry Module
- Submit questions and receive intelligent responses
- Support for different inquiry types (wisdom, guidance, insight, general)
- Contextual understanding for better answers
- Inquiry history tracking

### 💡 Wisdom Module
- AI-powered responses using OpenAI GPT
- Multiple response strategies based on inquiry type
- Confidence scoring for answers
- Graceful fallback when AI is unavailable

### 🎙️ Voice Interaction Module
- Text-to-speech capabilities
- Speech-to-text transcription
- Voice-based inquiry submission
- Modular voice processing

### 💰 Value-for-Value Participation
- Contribution tracking system
- Transaction management
- Support for multiple payment providers (configurable)
- Flexible value exchange model

## Installation

### Prerequisites
- Python 3.11+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/God-Incorporated-AI/godincorporated.git
cd godincorporated
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker Deployment

Build and run using Docker:

```bash
# Build the image
docker build -t godincorporated .

# Run the container
docker run -p 8000:8000 --env-file .env godincorporated
```

Or using Docker Compose:

```bash
docker-compose up -d
```

## Configuration

Key environment variables (see `.env.example`):

- `OPENAI_API_KEY`: Your OpenAI API key for wisdom generation
- `OPENAI_MODEL`: Model to use (default: gpt-4)
- `ENABLE_PAYMENTS`: Enable/disable payment processing
- `ENABLE_VOICE`: Enable/disable voice features
- `DATABASE_URL`: Database connection string
- `ALLOWED_ORIGINS`: CORS allowed origins

## API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Main Endpoints

#### Inquiry
- `POST /inquiry/submit` - Submit a new inquiry
- `GET /inquiry/history/{inquiry_id}` - Get inquiry details

#### Voice
- `POST /voice/process` - Process voice input
- `GET /voice/status` - Check voice module status

#### Value
- `POST /value/contribute` - Make a contribution
- `GET /value/transaction/{transaction_id}` - Get transaction details
- `GET /value/status` - Check value module status

#### Health
- `GET /health` - Service health check
- `GET /` - API information

## Project Structure

```
godincorporated/
├── app/
│   ├── api/              # API route handlers
│   │   ├── inquiry.py    # Inquiry endpoints
│   │   ├── voice.py      # Voice endpoints
│   │   ├── value.py      # Value endpoints
│   │   └── health.py     # Health check endpoints
│   ├── models/           # Pydantic models
│   │   └── __init__.py   # Request/Response models
│   ├── modules/          # Core business logic
│   │   ├── inquiry.py    # Inquiry processing
│   │   ├── wisdom.py     # AI wisdom generation
│   │   ├── voice.py      # Voice processing
│   │   └── value.py      # Value exchange
│   ├── config.py         # Configuration management
│   └── __init__.py
├── tests/                # Test suite
│   ├── test_inquiry.py
│   ├── test_voice.py
│   ├── test_value.py
│   └── test_health.py
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

## Development

### Adding New Modules

1. Create a new module in `app/modules/`
2. Define the module's business logic
3. Create API routes in `app/api/`
4. Register the router in `main.py`
5. Add tests in `tests/`

### Code Style

This project follows Python best practices:
- PEP 8 style guide
- Type hints where applicable
- Comprehensive docstrings
- Modular, testable code

## Architecture

The application follows a modular architecture:

1. **API Layer** (`app/api/`): Handles HTTP requests and responses
2. **Module Layer** (`app/modules/`): Contains business logic
3. **Model Layer** (`app/models/`): Defines data structures
4. **Configuration** (`app/config.py`): Centralized settings management

Each module is independent and can be enabled/disabled via configuration.

## Future Enhancements

- Database persistence for inquiries and transactions
- User authentication and authorization
- Rate limiting and quota management
- Advanced AI model selection
- Real-time voice streaming
- Payment gateway integration
- Analytics and insights dashboard
- Multi-language support

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
