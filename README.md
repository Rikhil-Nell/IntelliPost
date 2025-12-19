# SIH Sentiment Analysis

A FastAPI-based backend system for analyzing sentiment in stakeholder comments on legislative drafts for the Ministry of Corporate Affairs. The system enables users to upload draft documents (PDF), generate AI-powered summaries, and collect comments with automated sentiment analysis.

## 🚀 Features

- **User Authentication**: Secure JWT-based registration and login system
- **PDF Processing**: Upload and extract text from legislative draft documents
- **AI-Powered Summarization**: Generate draft summaries using GPT-4.1 and GPT-5-nano
- **Sentiment Analysis**: Automated sentiment analysis of stakeholder comments
- **Batch Processing**: Support for CSV upload of multiple comments
- **RESTful API**: Complete REST API with proper authentication and validation
- **Database Management**: PostgreSQL backend with async operations and migrations

## 🛠️ Technologies Used

### Backend Framework
- **FastAPI**: High-performance Python web framework for building APIs
- **SQLModel**: ORM and data validation library built on SQLAlchemy and Pydantic
- **AsyncPG**: Asynchronous PostgreSQL driver for efficient database access

### Database & Migrations
- **PostgreSQL**: Primary database for storing all application data
- **Alembic**: Database migrations and schema management

### AI & ML
- **pydantic-ai**: Integration with LLMs (OpenAI GPT-4.1, GPT-5-nano)
- **OpenAI API**: Powers summary generation and sentiment analysis
- **PyPDF2**: PDF parsing and text extraction

### Security & Authentication
- **Passlib/Bcrypt**: Secure password hashing and verification
- **JWT (python-jose, pyjwt)**: Authentication via JSON Web Tokens

### Development & Deployment
- **Docker**: Containerization for reproducible environments
- **Pydantic**: Data validation and settings management

## 📁 Project Structure

```
📁 SIH Sentiment Analysis/
├── 📁 backend/
│   ├── 📁 alembic/                 # Database migrations
│   │   └── 📁 versions/            # Migration files
│   ├── 📁 app/
│   │   ├── 📁 api/                 # API layer
│   │   │   └── 📁 v1/
│   │   │       └── 📁 routers/     # API endpoints
│   │   ├── 📁 controllers/         # Business logic
│   │   ├── 📁 core/               # Core configuration
│   │   ├── 📁 crud/               # Database operations
│   │   ├── 📁 db/                 # Database setup
│   │   ├── 📁 models/             # Data models
│   │   ├── 📁 prompts/            # LLM prompt templates
│   │   ├── 📁 schemas/            # Pydantic schemas
│   │   └── 📁 utils/              # Utility functions
│   └── 📄 main.py                 # Application entry point
├── 📄 Dockerfile                  # Docker configuration
├── 📄 pyproject.toml              # Project dependencies
└── 📄 README.md                   # This file
```

## 🏗️ Architecture Overview

### Core Components

- **Models**: SQLModel-based models for Users, Drafts, and Comments with UUID primary keys
- **Schemas**: Pydantic schemas for request/response validation
- **CRUD Layer**: Generic and custom CRUD classes for async database operations
- **Controllers**: Business logic layer handling PDF extraction and LLM calls
- **Routers**: FastAPI routers organizing endpoints with authentication
- **Agents**: LLM-powered agents for summarization and sentiment analysis

### Data Flow

1. **Authentication**: JWT-based user authentication for all protected endpoints
2. **Draft Processing**: PDF upload → Text extraction → AI summarization → Database storage
3. **Comment Analysis**: Comment submission → Sentiment analysis → Database storage
4. **Data Retrieval**: Authenticated access to user-scoped drafts and comments

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SIH-Sentiment-Analysis
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv install

   # Or using pip
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup

```bash
# Build and run with Docker
docker build -t sih-sentiment .
docker run -p 8000:8000 sih-sentiment
```

## 📚 API Documentation

Once the application is running, visit:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/drafts/` - Upload draft document
- `GET /api/v1/drafts/` - List user drafts
- `POST /api/v1/comments/` - Submit comment
- `POST /api/v1/comments/batch` - Batch upload comments via CSV

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Application
DEBUG=false
```

### Custom Prompts

Modify prompt templates in the `app/prompts/` directory:
- `draft_summary.md` - Instructions for draft summarization
- `sentiment_analysis.md` - Instructions for sentiment analysis

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 🚀 Deployment

Deployment instructions will be added based on your target platform (AWS, GCP, Azure, etc.).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Ministry of Corporate Affairs for the project requirements
- OpenAI for providing the LLM capabilities
- FastAPI community for the excellent framework

## 📞 Support

For support and questions, please create an issue in the repository or contact the development team.

---

**Built with ❤️ for Smart India Hackathon**