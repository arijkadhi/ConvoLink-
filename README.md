# Messaging API 🚀

A production-ready RESTful API for messaging functionality built with FastAPI, PostgreSQL, and Docker.

## 📋 Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Real-time Messaging**: Send and receive messages between users
- **Conversation Management**: Create and manage conversations
- **Email Notifications**: SendGrid integration for email notifications
- **RESTful API**: Clean, versioned API endpoints (v1)
- **Interactive Documentation**: Swagger UI and ReDoc
- **Database Migrations**: Alembic for database version control
- **Containerized**: Docker and Docker Compose ready
- **Production Ready**: Comprehensive logging, error handling, and monitoring

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (production) / SQLite (development)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Email**: SendGrid
- **Migrations**: Alembic
- **Testing**: pytest
- **Containerization**: Docker & Docker Compose
- **Web Server**: Uvicorn
- **Reverse Proxy**: Nginx (optional)

## 📁 Project Structure

```
messaging-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── auth.py              # Authentication utilities
│   ├── middleware.py        # Custom middleware
│   ├── logging_config.py    # Logging configuration
│   ├── models/              # SQLAlchemy models
│   ├── routers/             # API route handlers
│   │   ├── auth.py
│   │   ├── messages.py
│   │   └── conversations.py
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
│       └── email_service.py
├── frontend/                # Frontend files
│   ├── index.html
│   └── app.js
├── tests/                   # Test suite
├── alembic/                 # Database migrations
├── nginx/                   # Nginx configuration
├── .github/workflows/       # CI/CD pipeline
├── docker-compose.yml       # Development compose
├── docker-compose.prod.yml  # Production compose
├── docker-compose.dev.yml   # Development with hot reload
├── Dockerfile               # Development Dockerfile
├── Dockerfile.prod          # Optimized production Dockerfile
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── deploy.sh               # Linux/Mac deployment script
├── deploy.bat              # Windows deployment script
├── DEPLOYMENT.md           # Comprehensive deployment guide
├── QUICKSTART.md           # Quick deployment guide
└── DEPLOYMENT_CHECKLIST.md # Pre-deployment checklist
```

## 🚀 Quick Start

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd messaging-api
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   python run.py
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Using Docker (Recommended)

```bash
# Development
docker-compose -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## 📦 Production Deployment

### Quick Deploy (10 minutes)

See [QUICKSTART.md](QUICKSTART.md) for a rapid deployment guide.

**TL;DR:**
```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with production values

# 2. Deploy (Windows)
.\deploy.bat start

# 2. Deploy (Linux/Mac)
chmod +x deploy.sh
./deploy.sh start
```

### Full Deployment Guide

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions covering:
- Docker deployment
- Cloud platforms (AWS, DigitalOcean, Heroku, Railway)
- Traditional VPS deployment
- SSL/HTTPS setup
- Monitoring and backups

### Deployment Checklist

Use [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) before going to production.

## 🔐 Environment Variables

Key environment variables (see `.env.example` for complete list):

```env
# Application
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ENVIRONMENT=production
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email (SendGrid)
SENDGRID_API_KEY=<your-api-key>
SENDGRID_FROM_EMAIL=noreply@yourdomain.com

# CORS
ALLOWED_ORIGINS=https://yourdomain.com
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/register` - Register new user
- `POST /api/v1/login` - Login user
- `POST /api/v1/logout` - Logout user

### Message Endpoints
- `GET /api/v1/messages` - Get all messages
- `POST /api/v1/messages` - Send message
- `GET /api/v1/messages/{id}` - Get specific message
- `PUT /api/v1/messages/{id}` - Update message
- `DELETE /api/v1/messages/{id}` - Delete message

### Conversation Endpoints
- `GET /api/v1/conversations` - Get all conversations
- `POST /api/v1/conversations` - Create conversation
- `GET /api/v1/conversations/{id}` - Get specific conversation
- `DELETE /api/v1/conversations/{id}` - Delete conversation

Full interactive documentation available at `/docs` when running.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## 🔧 Development Scripts

```bash
# Run development server with hot reload
python run.py

# Create database migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 📊 Monitoring & Logs

```bash
# Docker logs
docker-compose -f docker-compose.prod.yml logs -f

# Specific service logs
docker logs messaging-api-prod -f

# Database logs
docker logs messaging-db-prod -f
```

## 🔄 CI/CD

GitHub Actions workflow configured for:
- Automated testing on push/PR
- Code coverage reporting
- Docker image building
- Automated deployment (configure secrets)

See [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)

## 🛡️ Security Features

- JWT token authentication
- Password hashing (bcrypt)
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- Input validation (Pydantic)
- Security headers
- Non-root container user
- Environment variable secrets

## 📈 Performance

- Async/await for I/O operations
- Connection pooling
- Docker multi-stage builds
- Optimized production Dockerfile
- Resource limits configured
- Health checks enabled

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🆘 Support & Troubleshooting

- **Deployment Issues**: See [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting)
- **Configuration**: Check [.env.example](.env.example)
- **API Errors**: Check logs with `docker-compose logs -f`
- **Database Issues**: Verify DATABASE_URL and connection

## 🗺️ Roadmap

- [ ] WebSocket support for real-time messaging
- [ ] File/image attachments
- [ ] Message read receipts
- [ ] User presence status
- [ ] Message search functionality
- [ ] Rate limiting
- [ ] Redis caching
- [ ] Kubernetes deployment manifests

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI**

**Status:** Production Ready ✅
