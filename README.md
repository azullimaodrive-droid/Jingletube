# Jingletube

A comprehensive platform for discovering, managing, and sharing music content with seamless streaming and personalized recommendations.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Deployment Instructions](#deployment-instructions)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Overview

Jingletube is a modern music streaming and discovery platform designed to provide users with an intuitive interface for exploring music, creating playlists, and discovering new artists. Built with scalability and user experience in mind, Jingletube combines powerful backend services with a responsive frontend to deliver a seamless music listening experience.

### Key Objectives

- **Discovery**: Help users discover new music through intelligent recommendations
- **Accessibility**: Provide a smooth, intuitive interface across all devices
- **Community**: Enable users to share and collaborate on playlists
- **Quality**: Deliver high-quality audio streaming with minimal latency

## Features

### Core Music Features
- 🎵 **Streaming**: High-quality audio streaming with adaptive bitrate
- 🎧 **Playlists**: Create, edit, and share custom playlists
- ❤️ **Favorites**: Save and organize your favorite tracks
- 🔍 **Search**: Powerful search functionality across tracks, artists, and albums
- 🎼 **Album Management**: Browse and explore full album collections

### Discovery & Recommendations
- 🤖 **Smart Recommendations**: AI-powered suggestions based on listening history
- 🔥 **Trending**: Discover trending tracks and artists in real-time
- 📊 **Genre Exploration**: Browse music by genre, mood, and era
- 👥 **Artist Following**: Follow favorite artists and get notified of new releases

### User Experience
- 📱 **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- 🌓 **Dark/Light Themes**: Customizable interface themes
- 🔔 **Notifications**: Real-time updates on new releases and recommendations
- 📊 **Listening Stats**: Track your listening habits and generate yearly summaries

### Sharing & Social
- 🔗 **Share Playlists**: Share playlists with friends and family
- 💬 **Playlist Collaboration**: Collaborate with others on shared playlists
- 📤 **Export**: Export playlists to various formats

## Quick Start

### Prerequisites

- Node.js 18.x or higher
- npm 9.x or higher (or yarn/pnpm)
- Git
- A modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/azullimaodrive-droid/Jingletube.git
   cd Jingletube
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env.local
   ```
   
   Update `.env.local` with your configuration:
   ```env
   VITE_API_URL=http://localhost:3000
   VITE_SPOTIFY_CLIENT_ID=your_spotify_client_id
   VITE_YOUTUBE_API_KEY=your_youtube_api_key
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Open in your browser**
   ```
   http://localhost:5173
   ```

### Building for Production

```bash
npm run build
npm run preview
```

## Authentication

### Supported Methods

Jingletube supports multiple authentication mechanisms:

#### 1. OAuth 2.0 (Recommended)

**Spotify OAuth Integration**
```javascript
// Automatically handled by the auth system
// Users click "Sign in with Spotify" button
// Redirects to Spotify authorization
// Returns access token for API calls
```

**Configuration:**
- Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Create an application
- Add redirect URI: `http://localhost:3000/auth/callback`
- Copy Client ID to `.env.local`

#### 2. Email/Password Authentication

```bash
# Create an account
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "User Name"
}

# Login
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### 3. Social Login

- Google Sign-In
- Apple Sign-In
- GitHub OAuth

### Session Management

- JWT tokens stored securely in httpOnly cookies
- Automatic token refresh before expiration
- Logout clears all session data
- Cross-device session management available

### API Authentication

All API requests require authentication headers:
```bash
Authorization: Bearer {access_token}
Content-Type: application/json
```

## Deployment Instructions

### Prerequisites

- Docker & Docker Compose (recommended)
- Or: Node.js, PostgreSQL, Redis server running
- SSL certificate for production

### Option 1: Docker Deployment (Recommended)

1. **Build Docker images**
   ```bash
   docker-compose build
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec api npm run migrate
   ```

### Option 2: Traditional Deployment

#### Backend Setup

```bash
# Install dependencies
npm install

# Configure database
DATABASE_URL=postgresql://user:password@localhost:5432/jingletube
REDIS_URL=redis://localhost:6379

# Run migrations
npm run migrate

# Start backend server
npm run start:server
```

#### Frontend Setup

```bash
# Build frontend
npm run build

# Serve with nginx or similar
# Point to dist/ directory
```

#### Nginx Configuration Example

```nginx
server {
    listen 443 ssl http2;
    server_name jingletube.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        root /var/www/jingletube/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Option 3: Cloud Deployment

#### Vercel (Frontend)

```bash
npm install -g vercel
vercel --prod
```

#### Heroku (Backend)

```bash
heroku login
heroku create jingletube-api
git push heroku main
heroku run npm run migrate
```

#### AWS (Full Stack)

1. Push frontend to S3 + CloudFront
2. Deploy backend to EC2 or ECS
3. Use RDS for database
4. Use ElastiCache for Redis

### Post-Deployment

1. **Verify services**
   ```bash
   curl https://jingletube.example.com/api/health
   ```

2. **Check logs**
   ```bash
   docker-compose logs -f api
   ```

3. **Enable monitoring**
   - Set up error tracking (Sentry)
   - Configure APM (New Relic)
   - Enable analytics

## Testing

### Unit Tests

```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### Integration Tests

```bash
npm run test:integration
```

### E2E Tests

```bash
# Run Cypress tests
npm run test:e2e

# Run specific test file
npm run test:e2e -- --spec "cypress/e2e/login.cy.ts"

# Run headless
npm run test:e2e:headless
```

### Performance Tests

```bash
npm run test:performance

# Lighthouse audits
npm run audit:lighthouse
```

### Test Coverage Targets

- **Overall**: 80%+
- **Critical paths**: 95%+
- **Utilities**: 85%+

### Sample Test Command

```bash
# Run tests matching pattern
npm run test -- --testNamePattern="authentication"

# Debug tests
npm run test:debug
```

## Roadmap

### Version 1.0 (Q1 2025)
- ✅ Core streaming functionality
- ✅ User authentication system
- ✅ Basic playlist management
- ✅ Search functionality
- ⏳ Mobile app MVP

### Version 1.1 (Q2 2025)
- 📅 Advanced recommendation engine
- 📅 Social features (following, sharing)
- 📅 Collaborative playlists
- 📅 Enhanced analytics dashboard
- 📅 Podcast support

### Version 1.2 (Q3 2025)
- 📅 Offline listening mode
- 📅 Family plan support
- 📅 High-fidelity audio streams
- 📅 Advanced equalizer
- 📅 Integration with smart speakers

### Version 1.3 (Q4 2025)
- 📅 Artist direct support
- 📅 Live streaming events
- 📅 Music video integration
- 📅 NFT playlist collection
- 📅 AI DJ feature

### Future Considerations
- 🔮 Blockchain integration for artist royalties
- 🔮 VR/Metaverse music venues
- 🔮 AI-generated personalized concert recommendations
- 🔮 Super fidelity audio (lossless)
- 🔮 Global festival tracking and ticketing

## Contributing

We welcome contributions from the community! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Commit with clear messages: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Coding Standards

- Follow ESLint configuration
- Use TypeScript for type safety
- Write meaningful comments
- Follow existing code style
- Add unit tests for new code

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, perf, test, chore

Example:
```
feat(auth): add Google Sign-In support

Implement OAuth 2.0 flow for Google authentication.
Includes token refresh and session management.

Closes #123
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated**: 2025-12-14

For more information, visit our [documentation](./docs) or join our [Discord community](https://discord.gg/jingletube).
