<div align="center">
  <img src="frontend/public/logo.ico" alt="Ordo Logo" width="128" height="128" />
  
  # 🐬 Ordo - AI-Powered Meeting Intelligence Platform
  
  > **Transform your meetings into actionable insights with cutting-edge AI**
</div>

Ordo is a sophisticated, full-stack platform that automatically transcribes, analyzes, and extracts meaningful insights from your meeting recordings. Built with modern technologies and powered by OpenAI's latest models, it turns hours of audio into searchable transcripts, visual summaries, and actionable intelligence.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=flat&logo=vuedotjs&logoColor=4FC08D)](https://vuejs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)

## ✨ Key Features

### 🎤 **Advanced Audio Processing**

- **Multi-format Support**: MP3, MP4, WAV, M4A, MOV, AVI, FLAC, AAC, WebM, MKV, WMV, MPEG
- **Speaker Diarization**: Automatically identify and label different speakers using PyAnnote
- **High-Quality Transcription**: Powered by OpenAI Whisper with 99% accuracy
- **Large File Support**: Handle files up to 500MB with optimized processing

### 🧠 **AI-Powered Intelligence**

- **Smart Summaries**: Generate concise meeting summaries with key points highlighted
- **Action Item Extraction**: Automatically identify tasks, deadlines, and assignments
- **Decision Tracking**: Capture important decisions with context and ownership
- **Visual Summaries**: Generate decision tree flowcharts using DALL·E 3
- **Automated Labeling**: Custom labeling rules for meeting categorization

### 🔍 **Advanced Search & Discovery**

- **Semantic Search**: Find content by meaning, not just keywords
- **Full-Text Search**: Search across transcripts, summaries, and metadata
- **Speaker-Specific Search**: Find what specific participants said
- **Timeline Navigation**: Jump to exact moments in recordings

### 🏗️ **Production-Ready Architecture**

- **Microservices Design**: Scalable backend with FastAPI and async processing
- **Background Processing**: Redis-based task queue for heavy operations
- **Cloud Storage**: Supabase integration for secure file storage
- **Database Migrations**: Alembic-powered schema management
- **Docker Deployment**: Full containerization with Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API key
- Supabase account (for storage and database)

### 1. Clone & Setup

```bash
git clone https://github.com/HattoriHanzo16/ordo
cd ordo
make setup
```

### 2. Configure Environment

Copy and edit the environment file:

```bash
cp server/env.example server/.env
```

Configure your `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
STORAGE_BUCKET_NAME=uploads

# Database Configuration
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### 3. Launch

```bash
make dev
```

Your application will be available at:

- **Frontend**: <http://localhost:3000>
- **Backend API**: <http://localhost:8000>
- **API Documentation**: <http://localhost:8000/docs>

## 🛠️ Technology Stack

### Backend

```yaml
Core Framework: FastAPI (Python 3.11+)
Database: PostgreSQL with SQLAlchemy ORM
Task Queue: Redis + RQ for background processing
AI Models:
  - OpenAI Whisper (transcription)
  - OpenAI GPT-4 (analysis)
  - OpenAI DALL·E 3 (visual summaries)
  - PyAnnote Audio (speaker diarization)
Storage: Supabase (PostgreSQL + file storage)
Deployment: Docker with multi-stage builds
```

### Frontend

```yaml
Framework: Vue.js 3 with Composition API
Styling: Tailwind CSS with custom design system
Icons: Heroicons
Build Tool: Vite
HTTP Client: Axios
Routing: Vue Router 4
```

### Infrastructure

```yaml
Containerization: Docker & Docker Compose
Database: PostgreSQL (via Supabase)
Cache & Queue: Redis
File Storage: Supabase Storage
AI Services: OpenAI API
```

## 📁 Project Structure

```
ordo/
├── frontend/                    # Vue.js 3 Frontend
│   ├── src/
│   │   ├── components/         # UI Components
│   │   │   ├── HomePage.vue    # Landing page with features
│   │   │   ├── RecordingsPage.vue  # Recordings list
│   │   │   ├── RecordingDetailPage.vue  # Detailed view
│   │   │   ├── UploadSection.vue       # Drag & drop upload
│   │   │   └── SettingsPage.vue        # User settings
│   │   ├── router/             # Vue Router configuration
│   │   └── main.js            # Application entry point
│   └── tailwind.config.js     # Custom design system
│
├── server/                     # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/            # API endpoints
│   │   │   ├── endpoints/     # Route handlers
│   │   │   │   ├── upload.py     # File upload
│   │   │   │   ├── recordings.py # Recording management
│   │   │   │   ├── search.py     # Search functionality
│   │   │   │   └── labeling.py   # Automated labeling
│   │   │   └── api.py         # API router
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py      # Environment settings
│   │   │   ├── middleware.py  # CORS & security
│   │   │   └── exceptions.py  # Error handling
│   │   ├── models/            # Database models
│   │   │   ├── recording.py   # Recording model
│   │   │   └── labeling_rule.py # Labeling rules
│   │   ├── services/          # Business logic
│   │   │   ├── transcription_service.py    # Whisper integration
│   │   │   ├── analysis_service.py         # GPT-4 analysis
│   │   │   ├── visual_summary_service.py   # DALL·E 3 generation
│   │   │   ├── storage_service.py          # Supabase storage
│   │   │   └── labeling_service.py         # Auto-labeling
│   │   └── tasks/             # Background tasks
│   │       └── processing_tasks.py  # Async processing
│   ├── migrations/            # Database migrations
│   └── requirements.txt       # Python dependencies
│
├── docker-compose.yml         # Development environment
├── Dockerfile.backend         # Backend container
├── Dockerfile.frontend        # Frontend container
└── Makefile                  # Development commands
```

## 🎯 Core Features Deep Dive

### 📊 Meeting Analysis Pipeline

1. **Upload**: Drag & drop interface for multiple file formats
2. **Transcription**: OpenAI Whisper converts speech to text
3. **Speaker Diarization**: PyAnnote identifies individual speakers
4. **AI Analysis**: GPT-4 extracts summaries, action items, and decisions
5. **Visual Generation**: DALL·E 3 creates decision tree flowcharts
6. **Labeling**: Custom rules automatically categorize meetings

### 🎨 Visual Summaries

Ordo generates intelligent visual summaries using DALL·E 3:

- **Decision Trees**: Flowcharts showing decision paths and outcomes
- **Process Diagrams**: Visual representation of action items and workflows
- **Priority Mapping**: Color-coded visualizations for task priorities
- **Timeline Views**: Sequential flow of decisions and actions

### 🏷️ Smart Labeling System

Create custom rules for automatic meeting categorization:

```python
# Example labeling rules
rules = [
    {
        "label": "Effective Meeting",
        "criteria": "Clear decisions made, action items assigned, under 60 minutes",
        "color": "#10B981"
    },
    {
        "label": "Follow-up Required", 
        "criteria": "Open questions, pending decisions, action items without owners",
        "color": "#F59E0B"
    }
]
```

### 🔍 Advanced Search Capabilities

- **Semantic Search**: Find meetings by meaning and context
- **Speaker Search**: "What did Sarah say about the budget?"
- **Topic Search**: Find all discussions about specific subjects
- **Action Item Search**: Locate pending tasks and deadlines
- **Decision Search**: Find past decisions and their rationale

## 🖥️ API Documentation

### Core Endpoints

#### Upload & Processing

```http
POST /api/v1/upload
Content-Type: multipart/form-data

# Upload meeting recording for processing
```

#### Recordings Management

```http
GET /api/v1/recordings                    # List all recordings
GET /api/v1/recordings/{id}              # Get specific recording
DELETE /api/v1/recordings/{id}           # Delete recording
```

#### Search & Discovery

```http
GET /api/v1/search/semantic?query=...    # Semantic search
```

#### Labeling & Rules

```http
GET /api/v1/labeling/rules               # List labeling rules
POST /api/v1/labeling/rules              # Create new rule
PUT /api/v1/labeling/rules/{id}          # Update rule
DELETE /api/v1/labeling/rules/{id}       # Delete rule
```

### Response Examples

#### Recording Detail

```json
{
  "id": 123,
  "original_filename": "team-standup-2024.mp3",
  "duration": 1847.5,
  "transcript": "Full transcript with speaker labels...",
  "summary": "Team discussed Q4 goals, identified three key action items...",
  "action_items": [
    {
      "description": "Complete user research analysis",
      "assignee": "Sarah Johnson",
      "due_date": "2024-01-15",
      "priority": "high"
    }
  ],
  "decisions": [
    {
      "description": "Approved budget increase for Q1 marketing",
      "owner": "Mike Chen",
      "context": "Based on Q4 performance metrics",
      "impact": "15% increase in lead generation capacity"
    }
  ],
  "visual_summary_url": "https://storage.supabase.co/...",
  "labels": ["Effective", "Weekly Standup"],
  "processing_status": "completed"
}
```

## 🐳 Development & Deployment

### Available Make Commands

```bash
make help           # Show all available commands
make setup          # Initial project setup
make build          # Build all containers
make dev            # Start development environment
make logs           # View logs from all services
make clean          # Remove containers and volumes
make backend-shell  # Access backend container
make frontend-shell # Access frontend container
```

### Development Workflow

1. **Backend Development**: Hot reload with uvicorn
2. **Frontend Development**: Vite dev server with HMR
3. **Database Changes**: Alembic migrations with auto-generation
4. **Background Tasks**: Redis-based queue with worker processes

### Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with environment variables
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Configuration

The application supports multiple configuration methods:

- Environment variables
- `.env` files
- Docker secrets
- Cloud provider environment injection

## 🔧 Configuration

### Required Services

1. **OpenAI API**: For transcription, analysis, and visual generation
2. **Supabase**: For database and file storage
3. **Redis**: For background task processing

### Optional Integrations

- **HuggingFace**: For enhanced speaker diarization
- **Custom Storage**: Alternative to Supabase storage
- **External Databases**: PostgreSQL alternatives

### Performance Tuning

```yaml
# Memory optimization for ML models
Environment Variables:
  TORCH_HOME: /tmp/torch
  HF_HOME: /tmp/huggingface
  OMP_NUM_THREADS: 1
  CUDA_VISIBLE_DEVICES: ""

# Container limits
memory: 4g
shm_size: 1g
```

## 📈 Monitoring & Observability

### Logging

- Structured logging with timestamps and context
- Different log levels for development and production
- File-based logging with rotation
- Real-time log streaming via Docker

### Health Checks

```http
GET /api/v1/health    # Service health status
```

### Metrics

- Processing time tracking
- File upload statistics
- Error rate monitoring
- Resource utilization

## 🛡️ Security & Privacy

### Data Protection

- Secure file upload with type validation
- Encrypted storage via Supabase
- API key protection for external services
- CORS configuration for web security

### Privacy Considerations

- No permanent storage of API keys in code
- Optional data retention policies
- Secure deletion of uploaded files
- Audit logging for sensitive operations

### Code Standards

- **Backend**: Black formatting, type hints, comprehensive tests
- **Frontend**: ESLint configuration, Vue 3 best practices
- **Documentation**: Clear comments and API documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing cutting-edge AI models
- **Supabase** for excellent developer experience
- **PyAnnote** for speaker diarization capabilities
- **Vue.js** and **FastAPI** communities for robust frameworks

---

<div align="center">

**Built with ❤️ for better meetings**


</div>
