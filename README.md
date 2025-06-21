# Ordo

Audio processing application with automated transcription and analysis.

## Tech Stack

- **Frontend**: Vue.js 3 + Vite + TailwindCSS
- **Backend**: FastAPI + SQLAlchemy
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **AI**: OpenAI API
- **Audio Processing**: PyAnnote, Torch

## Quick Start

1. **Setup environment**
   ```bash
   make setup
   ```

2. **Configure your `.env`**
   Edit `server/.env` with your API keys:
   - Supabase URL and keys
   - OpenAI API key
   - Database connection

3. **Start development**
   ```bash
   make dev
   ```

4. **Access the app**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Development

```bash
# Build containers
make build

# Start services
make up

# View logs
make logs

# Stop services
make down

# Clean up
make clean
```

## Project Structure

```
├── frontend/          # Vue.js frontend
├── server/           # FastAPI backend
├── Dockerfile.frontend
├── Dockerfile.backend
└── docker-compose.yml
```

---

*This README will be updated as the project evolves.* 