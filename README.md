# IntelliPost 📬

> **Postathon Hackathon Project** — Intelligent postal mail processing powered by AI vision

A FastAPI backend for a mobile app that automates postal mail sorting by extracting address information from envelope images using AI vision models and routing them to the appropriate sorting centers.

## 🚀 Features

- **AI-Powered Mail Extraction**: Upload envelope/postcard images and automatically extract sender & receiver details (name, address, pincode) using vision AI
- **Smart Sorting Center Assignment**: Automatically resolves the correct postal sorting division based on the extracted pincode using India Post's API
- **Pincode Caching**: Intelligent caching of pincode lookups to minimize external API calls
- **Secure Image Storage**: Cloudflare R2 integration for secure, pre-signed URL-based image uploads
- **User Authentication**: JWT-based authentication system for secure access
- **Background Processing**: Async task processing for mail extraction without blocking the API
- **Processing Status Tracking**: Track mail processing status (Pending → Processing → Completed/Failed)

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI** — High-performance async Python API framework
- **SQLModel** — ORM combining SQLAlchemy + Pydantic for type-safe database models
- **AsyncPG** — Async PostgreSQL driver for non-blocking database operations

### AI & Vision
- **Pydantic AI** — AI agent framework for structured LLM outputs
- **OpenAI Vision API** — Extracts postal information from envelope images

### Storage & Database
- **PostgreSQL** — Primary database for users, mail records, and pincode cache
- **Cloudflare R2** — S3-compatible object storage for envelope images
- **Alembic** — Database migrations and schema management

### External APIs
- **India Post Pincode API** — Resolves pincodes to sorting divisions/districts

### Security
- **Passlib/Bcrypt** — Secure password hashing
- **JWT (PyJWT)** — Token-based authentication

### DevOps
- **Docker** — Containerized deployment
- **Docker Compose** — Multi-service orchestration

## 📁 Project Structure

```
📁 IntelliPost/
├── 📁 backend/
│   ├── 📁 alembic/                 # Database migrations
│   │   └── 📁 versions/            # Migration files
│   ├── 📁 app/
│   │   ├── 📁 api/                 # API layer
│   │   │   └── 📁 v1/
│   │   │       └── 📁 routers/     # API endpoints (auth, mail)
│   │   ├── 📁 controllers/         # Business logic (mail processing, R2)
│   │   ├── 📁 core/                # Config, JWT, security
│   │   ├── 📁 crud/                # Database CRUD operations
│   │   ├── 📁 db/                  # Database connection setup
│   │   ├── 📁 models/              # SQLModel data models
│   │   ├── 📁 prompts/             # AI agent prompt templates
│   │   ├── 📁 schemas/             # Pydantic request/response schemas
│   │   ├── 📁 services/            # Services (AI agent, R2, pincode lookup)
│   │   └── 📁 utils/               # Utility functions
│   └── 📄 alembic.ini
├── 📄 Dockerfile
├── 📄 docker-compose.yml
├── 📄 pyproject.toml
└── 📄 README.md
```

## 🔄 How It Works

### The Mail Processing Pipeline

```
1. 📱 Mobile App uploads envelope image
         ↓
2. 🔗 Backend generates pre-signed R2 upload URL
         ↓
3. 📤 Image uploaded directly to Cloudflare R2
         ↓
4. ⚡ Backend triggers background processing task
         ↓
5. 🤖 AI Vision extracts: sender/receiver name, address, pincode
         ↓
6. 🔍 Pincode API lookup → Sorting division resolved
         ↓
7. ✅ Mail record updated with extracted data & sorting center
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Login and receive JWT token |
| `POST` | `/api/v1/mail/generate_upload_url` | Get pre-signed URL for image upload |
| `POST` | `/api/v1/mail/process` | Trigger mail processing (background task) |
| `GET`  | `/api/v1/mail/` | Get all processed mails (paginated) |
| `GET`  | `/api/v1/mail/{mail_id}` | Get specific mail details |

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- OpenAI API key (with vision model access)
- Cloudflare R2 bucket + credentials

### Environment Variables

Create a `.env` file with the following:

```env
# App
PROJECT_NAME=IntelliPost
MODE=development

# Database
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=intellipost

# JWT
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Cloudflare R2
R2_ACCOUNT_ID=your-r2-account-id
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=your-bucket-name
```

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd IntelliPost
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -e .
   ```

3. **Run database migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

4. **Start the application**
   ```bash
   uvicorn backend.app.main:app --reload
   ```

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testing

```bash
pytest test/
```

## 📋 Data Models

### Mail Record

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `user_id` | UUID | Owner of the mail record |
| `image_s3_key` | string | R2 storage key for the envelope image |
| `status` | enum | `PENDING` / `PROCESSING` / `COMPLETED` / `FAILED` |
| `receiver_name` | string | Extracted recipient name |
| `receiver_address` | string | Extracted recipient address |
| `receiver_pincode` | string | 6-digit Indian postal code |
| `sender_name` | string | Extracted sender name |
| `sender_address` | string | Extracted sender address |
| `sender_pincode` | string | 6-digit Indian postal code |
| `assigned_sorting_center` | string | Postal sorting division |
| `raw_ai_response` | JSON | Full AI extraction response |

## 🏆 Hackathon

Built for **Postathon** — a hackathon focused on innovating postal services in India.

## 📄 License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- India Post for the Pincode API
- OpenAI for vision model capabilities
- Cloudflare for R2 object storage
- FastAPI community for the excellent framework

## 📞 Support

For support and questions, please create an issue in the repository or contact the development team.

---

**Built with ❤️ for Smart India Hackathon**