# VRI Platform for Inclusive Communication (Uganda)

> **National Multi-Channel Communication Infrastructure for Deaf and Hard of Hearing Persons**

A multi-channel Video Relay Interpreting (VRI) platform designed to bridge the communication gap between Deaf and Hard of Hearing individuals and hearing participants across public service domains including Healthcare, Justice, Education, and Public Administration.

The platform is designed to support different levels of connectivity and device access by providing real-time video communication alongside asynchronous video and SMS/voice-based fallback channels.

---

## System Architecture

The VRI platform follows a multi-channel communication architecture built around graceful degradation. Instead of depending on a single communication method, the system provides alternative channels based on the user's device and network conditions.

### The 3-Layer Communication Model

#### Layer 1 — Real-Time Video

**Technology:** WebRTC

Provides low-latency, live video communication for users with suitable internet connectivity.

This layer is intended for:

- Live sign language interpretation
- Real-time communication between Deaf users, interpreters, and hearing participants
- Interpreter-assisted healthcare, justice, education, and public-service sessions
- Web and mobile video sessions

**Target:** approximately 2–3 seconds or less latency under suitable network conditions.

The latency target is a design goal and depends on network quality, device capability, geographic location, and the underlying WebRTC infrastructure.

---

#### Layer 2 — Asynchronous Video

**Technology:** MMS / Video Messaging Gateway

Provides a store-and-forward communication option when real-time video is not practical because of intermittent or unreliable connectivity.

The intended flow is:

```text
Deaf User
    |
    | Video Message
    v
VRI Platform
    |
    | Queue
    v
Interpreter
    |
    | Response
    v
Deaf User
```

This layer is intended to support:

- Video message creation
- Message queuing
- Delayed delivery
- Interpreter responses
- Retry mechanisms
- Communication in areas with unstable connectivity

---

#### Layer 3 — Text and Voice Relay

**Technology:** GSM / SMS / Voice

Provides a fallback communication method for users with limited connectivity or basic GSM feature phones.

The intended flow is:

```text
Deaf User
    |
    | SMS Request
    v
VRI Platform
    |
    | Route Request
    v
Interpreter
    |
    | Voice Call
    v
Hearing Participant
```

This layer is intended to support:

- SMS-based interpreter requests
- Interpreter notifications
- Voice relay
- Basic phone access
- Communication where video services are unavailable

---

## Unified Technology Stack

| Component | Technology |
|---|---|
| Web Frontend | React.js |
| Mobile Frontend | React Native / Expo |
| Backend API | Python, Django, Django REST Framework |
| Relational Database | PostgreSQL 15 |
| Real-Time Communication | WebRTC |
| Cache / Queue | Redis |
| Containerization | Docker / Docker Compose |
| CI/CD | GitHub Actions |
| Source Control | Git / GitHub |
| Telecom Integration | SMS, MMS and Voice Gateway APIs |

Some communication services and integrations may be introduced incrementally as the platform moves from development to pilot deployment.

---

## Repository Structure

The project is organized as a unified monorepo so that the backend, web application, mobile application, infrastructure, and development workflows can be managed from one repository.

```text
vri-platform-uganda/
│
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── CODEOWNERS
│
├── vri_backend/
│   ├── tests/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
│
├── frontend-web/
│   ├── Dockerfile
│   ├── .eslintrc.json
│   └── package.json
│
├── frontend-mobile/
│   ├── App.js
│   ├── .eslintrc.json
│   └── package.json
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

Note: `Dockerfile`, `docker-compose.yml`, `manage.py`, and `requirements.txt` live at the project root, not inside `vri_backend/`. The backend app code, tests, and settings live inside `vri_backend/`, but the container and dependency setup apply to the whole repo, which is why they sit at the top level.

`frontend-web/` has its own `Dockerfile` so it can run as its own service in `docker-compose.yml` alongside `backend` and `db`. `frontend-mobile/` intentionally does not — see [Mobile Frontend Development](#mobile-frontend-development) for why.

### Workspace Responsibilities

#### `vri_backend/`

Django and Django REST Framework backend responsible for:

- REST API endpoints
- Authentication
- Role-based access control
- User management
- Interpreter management
- Interpreter specialisations
- Session management
- Interpreter routing
- Institution management
- Multi-channel communication orchestration
- Session metadata and audit records

#### `frontend-web/`

React web application supporting:

- Interpreter workspace
- Institution workspace
- Administrator workspace
- Session management
- Interpreter queue
- Guest session access
- WebRTC communication interfaces

#### `frontend-mobile/`

React Native / Expo application primarily designed for Deaf and Hard of Hearing users.

The mobile application is intended to support:

- Simple session initiation
- Interpreter requests
- Real-time video sessions
- Session status
- Asynchronous video communication
- SMS fallback
- Network-aware communication flows

---

# Getting Started

## Prerequisites

Ensure your development workstation has the following installed:

- Git 2.30+
- Docker Desktop
- WSL 2 backend enabled on Windows
- Node.js 20+ for local frontend development

Docker is used to keep service dependencies, configurations, and development environments consistent across the team.

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/shadia-nalubega/vri-platform-uganda.git
cd vri-platform-uganda
```

Build and start the application services:

```bash
docker-compose up --build
```

Depending on the current Docker Compose configuration, the main services are expected to include:

| Service | Address |
|---|---|
| React Web Dashboard | `http://localhost:3000` |
| Django REST API | `http://localhost:8000` |
| Django Admin | `http://localhost:8000/admin` |
| PostgreSQL | `localhost:5432` |

The exact services started by Docker Compose should always be treated as the source of truth for the current development environment.

---

# Backend Development

Backend application code, settings, and tests live inside:

```bash
vri_backend/
```

Day-to-day backend commands (migrations, tests, management commands) should be run **inside the running container**, not directly on your local machine — this keeps everyone on the same Python version and dependencies. The commands below already do this correctly.

### Database Migrations

Run Django migrations inside the backend container:

```bash
docker-compose exec backend python manage.py migrate
```

### Create a Django Superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

After creating the account, access the Django administration panel:

```text
http://localhost:8000/admin
```

### Create a New Django Application

```bash
docker-compose exec backend python manage.py startapp <app_name>
```

---

# Web Frontend Development

The web frontend is located in:

```text
frontend-web/
```

The web frontend runs as its own service in `docker-compose.yml` (`web`), so `docker-compose up --build` starts it automatically alongside the backend and database. The steps below are for working on it locally outside Docker, if you prefer.

Install dependencies:

```bash
cd frontend-web
npm install
```

Run ESLint:

```bash
npm run lint
```

Automatically fix supported linting issues:

```bash
npm run lint:fix
```

Start the web application locally:

```bash
npm start
```

The web application communicates with the Django backend through the configured API URL.

Example local configuration:

```text
REACT_APP_API_URL=http://localhost:8000
```

The actual environment variable name should match the frontend configuration used by the project.

---

# Mobile Frontend Development

The mobile application is located in:

```text
frontend-mobile/
```

Unlike the backend and web frontend, the mobile app is **not containerized**. Expo needs to run against a physical device, emulator, or simulator on your host machine — a Docker container can't provide that, so this workspace is always run locally.

Install dependencies:

```bash
cd frontend-mobile
npm install
```

Run linting:

```bash
npm run lint
```

Start the Expo development server:

```bash
npx expo start
```

or:

```bash
npm start
```

### Connecting to the Backend

When testing on an Android emulator, the local machine is normally accessed through:

```text
http://10.0.2.2:8000
```

For a physical device or iOS simulator, use the development machine's local network IP address where required.

Example:

```text
http://192.168.x.x:8000
```

The device and development computer must be able to communicate over the same local network when using a local IP address.

---

# Testing Suite

Testing is part of the development workflow and should be performed before changes are merged.

The testing strategy covers individual components, APIs, complete workflows, communication channels, and the VRI session lifecycle.

## Testing Levels

| Test Level | Purpose |
|---|---|
| Unit Testing | Test individual functions, services, and components |
| API Testing | Verify REST endpoints, validation, authentication, and permissions |
| Integration Testing | Verify that multiple services work together |
| UI Testing | Verify important user interactions |
| Session Testing | Verify VRI session state transitions |
| Communication Testing | Verify WebRTC, asynchronous video, SMS and voice workflows |
| End-to-End Testing | Verify complete real-world VRI scenarios |

---

## Backend Testing

Backend tests should cover:

- User registration
- Authentication
- Login and logout
- Role-based access control
- Permissions
- Interpreter profiles
- Interpreter availability
- Interpreter specialisations
- Session creation
- Session routing
- Interpreter assignment
- Session completion
- Institution accounts
- API validation
- Invalid requests
- Authentication failures
- Database interactions

Example test organization:

```text
vri_backend/
└── tests/
    ├── test_auth.py
    ├── test_users.py
    ├── test_interpreters.py
    ├── test_sessions.py
    ├── test_routing.py
    └── test_institutions.py
```

Run the backend test suite:

```bash
docker-compose exec backend python manage.py test
```

---

## API Testing

The REST API should be tested for:

- Correct HTTP status codes
- Valid request payloads
- Invalid request handling
- Authentication requirements
- Permission restrictions
- Response structure
- Database changes
- Error handling
- Session state transitions

Core API areas include:

```text
/auth/
/users/
/interpreters/
/sessions/
/routing/
/institutions/
```

---

# VRI Session Lifecycle Testing

The session lifecycle is one of the most important parts of the platform.

A typical session progresses through:

```text
REQUESTED
    ↓
ROUTING
    ↓
QUEUED
    ↓
ASSIGNED
    ↓
CONNECTING
    ↓
ACTIVE
    ↓
COMPLETED
```

Tests should verify that:

1. A valid user can create a session.
2. A new session starts with `REQUESTED`.
3. The routing process receives the session.
4. The session enters the appropriate interpreter queue.
5. An available interpreter can claim the session.
6. The session changes to `ASSIGNED`.
7. The communication connection can be established.
8. The session changes to `ACTIVE`.
9. The session can be ended correctly.
10. The session changes to `COMPLETED`.

Invalid state transitions should also be tested.

For example:

```text
COMPLETED → ACTIVE
```

should not be allowed.

---

# Web Frontend Testing

The React web application should be tested around the main workflows used by interpreters, institutions, and administrators.

Tests should cover:

- Login
- Authentication-protected routes
- Dashboard navigation
- Interpreter availability
- Interpreter queue
- Claiming a session
- Joining a session
- Ending a session
- Institution session requests
- Institution bookings
- Guest access
- Loading states
- Error states
- Session status updates

Example interpreter workflow:

```text
Interpreter Login
      ↓
Interpreter Dashboard
      ↓
View Available Sessions
      ↓
Claim Session
      ↓
Join Communication Session
      ↓
Complete Session
```

---

# Mobile Testing

The React Native application should be tested around the experience of Deaf and Hard of Hearing users.

Tests should cover:

- Application access
- Session initiation
- Service selection
- Interpreter requests
- Request status
- Interpreter assignment
- Joining a video session
- Ending a session
- Network interruption
- Reconnection
- Fallback communication
- Error and loading states

The application should also be tested under poor or unstable network conditions.

---

# Multi-Channel Communication Testing

Because the platform is designed to work across different connectivity conditions, each communication layer requires its own testing strategy.

## Layer 1 — Real-Time Video

Test:

- Video connection
- Audio connection
- Camera permissions
- Microphone permissions
- Interpreter connection
- Session establishment
- Reconnection
- Network interruption
- Session termination
- Connection quality

The 2–3 second latency figure is a target under suitable network conditions and should be validated during performance testing.

---

## Layer 2 — Asynchronous Video

Test:

- Video message creation
- Video upload
- Message queueing
- Delivery
- Interpreter notification
- Response handling
- Failed delivery
- Retry mechanisms
- Message status

Example:

```text
Deaf User
    ↓
Record Video Message
    ↓
Upload
    ↓
Message Queue
    ↓
Interpreter
    ↓
Response
```

---

## Layer 3 — Text and Voice Relay

Test:

- SMS request creation
- Request routing
- Interpreter notification
- Voice call initiation
- Hearing participant connection
- Status updates
- Failed delivery
- Retry mechanisms

Example:

```text
Deaf User
    ↓
SMS Request
    ↓
VRI Platform
    ↓
Interpreter
    ↓
Voice Call
    ↓
Hearing Participant
```

---

# Integration Testing

Integration testing verifies that separate components communicate correctly.

Examples include:

```text
React Web
    ↓
Django REST API
    ↓
PostgreSQL
```

```text
React Native
    ↓
Django REST API
    ↓
Interpreter Routing
    ↓
Interpreter
```

```text
VRI Platform
    ↓
Telecom Gateway
    ↓
SMS / MMS / Voice
    ↓
Mobile Network
```

Integration tests should cover:

- Frontend-to-API communication
- API-to-database communication
- Authentication
- Session creation
- Session persistence
- Interpreter routing
- Session status synchronization
- Telecom gateway communication
- Error handling between services

---

# End-to-End Testing

End-to-end tests should simulate complete real-world VRI workflows.

## Scenario 1 — Deaf User Requests an Interpreter

```text
Deaf User
    ↓
Open Mobile Application
    ↓
Request Interpreter
    ↓
Session Created
    ↓
Interpreter Queue
    ↓
Interpreter Claims Session
    ↓
Communication Connection
    ↓
Interpretation
    ↓
Session Completed
```

## Scenario 2 — Institution Requests an Interpreter

```text
Institution
    ↓
Create Session Request
    ↓
Select Service
    ↓
Submit Request
    ↓
Interpreter Assigned
    ↓
Session Starts
    ↓
Interpretation
    ↓
Session Completed
```

## Scenario 3 — Network Failure

```text
Active Video Session
        ↓
Network Interrupted
        ↓
Connection Lost
        ↓
Reconnect Attempt
        ↓
Connection Restored
```

Where supported, the platform should provide an appropriate fallback communication method when real-time video cannot be maintained.

---

# Test Commands

Run the complete backend test suite:

```bash
docker-compose exec backend python manage.py test
```

Run a specific backend test:

```bash
docker-compose exec backend python manage.py test tests.test_sessions
```

Run frontend linting:

```bash
cd frontend-web
npm run lint
```

Run mobile linting:

```bash
cd frontend-mobile
npm run lint
```

Build the web application:

```bash
cd frontend-web
npm run build
```

The exact commands should match the scripts defined in each workspace's `package.json`.

---

# Testing Before Pull Requests

Before opening a pull request, developers should verify:

```text
[ ] Application starts successfully
[ ] Database migrations work
[ ] Backend tests pass
[ ] Web frontend linting passes
[ ] Mobile frontend linting passes
[ ] Frontend production build passes
[ ] API endpoints work as expected
[ ] Authentication and permissions work
[ ] New functionality has appropriate tests
[ ] Existing functionality has not been broken
[ ] No secrets have been committed
```

Pull requests should not be merged while required CI checks are failing.

---

# Git Branching and Contribution Guidelines

The repository uses a controlled branching workflow to reduce the risk of unstable code reaching shared environments.

## Branch Structure

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready code |
| `develop` | Main integration branch |
| `feature/*` | Individual developer work |

Examples:

```text
feature/backend-user-auth
feature/web-interpreter-dashboard
feature/mobile-vri-call-screen
feature/webrtc-routing
feature/mms-queues
```

Developers should not commit directly to `main` or `develop`.

---

## Development Workflow

### 1. Update the Main Branch

```bash
git checkout main
git pull origin main
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Develop and Test

Run the appropriate tests and quality checks for the component you changed.

Backend:

```bash
docker-compose exec backend python manage.py test
```

Web:

```bash
cd frontend-web
npm run lint
npm run build
```

Mobile:

```bash
cd frontend-mobile
npm run lint
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat(module): description of changes"
```

### 5. Push the Feature Branch

```bash
git push origin feature/your-feature-name
```

### 6. Open a Pull Request

Create a pull request against the appropriate integration branch according to the team's current development workflow.

---

# Repository Governance

The repository should use branch protection and pull request controls to maintain code quality.

## Pull Request Requirements

A pull request should:

- Target the appropriate protected branch
- Receive at least one peer review
- Receive approval from the relevant Code Owner where applicable
- Pass required GitHub Actions CI checks
- Pass relevant backend tests
- Pass frontend quality checks
- Pass required build checks
- Avoid committing secrets or credentials

Direct pushes to protected branches should be disabled.

---

# Continuous Integration

GitHub Actions is used to automatically validate changes submitted through pushes and pull requests.

The CI pipeline should progressively validate:

```text
Developer Push / Pull Request
          ↓
Install Dependencies
          ↓
Backend Tests
          ↓
Frontend Linting
          ↓
Frontend Build
          ↓
Additional Quality Checks
          ↓
CI Result
```

The workflow is located at:

```text
.github/workflows/ci.yml
```

The repository also uses:

```text
.github/CODEOWNERS
```

to define ownership and review responsibilities for relevant areas of the codebase.

A pull request should not be merged while required CI checks are failing.

---

# Security and Environment Configuration

Sensitive configuration must never be committed to the repository.

Local environment-specific values should be stored in `.env` or the appropriate environment configuration system.

Examples include:

- Django secret key
- Database credentials
- API credentials
- Telecom gateway credentials
- WebRTC service credentials
- Third-party integration credentials

The `.env` file must remain excluded through `.gitignore`.

Example:

```text
.env
*.env
```

Do not place real production credentials inside:

- Source code
- README files
- Dockerfiles
- GitHub repositories
- Test fixtures
- Public documentation

If a secret is accidentally committed, it should be revoked and rotated immediately.

---

# Database and Development Data

The platform uses PostgreSQL 15 as its primary relational database.

The database is responsible for storing structured application data such as:

- User profiles
- Interpreter profiles
- Interpreter specialisations
- Institution records
- VRI sessions
- Session states
- Queue records
- Audit metadata

Development environments may use seed or sample data to make testing easier.

Example interpreter specialisations include:

```text
Medical
Legal
General
```

Development seed data must not contain real personal information and must not be used as production data.

---

# Troubleshooting

## PostgreSQL Port Already in Use

If Docker cannot bind to port `5432`, check whether another PostgreSQL installation is already running locally.

You can either stop the local PostgreSQL service or change the port mapping in the Docker Compose configuration.

---

## Reset the Development Database

If the local development database becomes corrupted or needs to be recreated:

```bash
docker-compose down -v
docker-compose up --build
```

> Warning: `docker-compose down -v` removes Docker volumes, including the local development database.

Do not use this command in an environment containing data that needs to be preserved.

---

## Rebuild Containers

If dependencies or Docker configuration have changed:

```bash
docker-compose down
docker-compose up --build
```

---

## Check Running Containers

```bash
docker-compose ps
```

View backend logs:

```bash
docker-compose logs backend
```

Follow backend logs in real time:

```bash
docker-compose logs -f backend
```

---

# Development Status

The platform is being developed incrementally. Some architectural components may be planned or under development rather than fully deployed.

Update this table as implementation progresses.

| Component | Status |
|---|---|
| Django REST API | In Development |
| PostgreSQL Database | Implemented / In Development |
| React Web Application | In Development |
| React Native Mobile Application | In Development |
| Authentication & RBAC | In Development |
| Interpreter Management | In Development |
| Interpreter Routing | In Development |
| VRI Session Management | In Development |
| WebRTC Communication | In Development |
| Asynchronous Video / MMS | Planned / In Development |
| SMS / Voice Relay | Planned / In Development |
| Telecom Integration | Planned |
| Monitoring & Analytics | Planned |
| Production Deployment | Planned |

The status should reflect the actual implementation in the repository and should be updated as features are completed.

---

# Project Vision

The long-term goal of the VRI Platform is to make communication access more practical for Deaf and Hard of Hearing persons across Uganda's essential public services.

The platform is designed around three principles:

### Accessibility

Communication services should be accessible across different devices and levels of connectivity.

### Reliability

When one communication channel is unavailable, the platform should provide an alternative where possible.

### Inclusion

The system should help Deaf and Hard of Hearing people communicate more effectively with healthcare providers, justice institutions, educators, public officers, businesses, and other hearing participants.

The platform is therefore not limited to a single video-calling application. It is intended as a multi-channel communication infrastructure connecting users, interpreters, institutions, and telecom services.

---

# Project Scope

The initial platform focuses on:

- Deaf and Hard of Hearing users
- Uganda Sign Language interpreters
- Healthcare institutions
- Justice institutions
- Educational institutions
- Public administration
- Interpreter routing and availability
- Real-time communication
- Asynchronous communication
- SMS and voice fallback
- Institutional session requests
- Session management
- Audit and operational metadata

Additional integrations and communication capabilities can be introduced as the platform progresses toward pilot deployment and production readiness.

---

# Contributing

Before contributing:

1. Read the repository guidelines.
2. Create a feature branch.
3. Keep changes focused on the feature or issue being addressed.
4. Run the relevant tests and quality checks.
5. Commit using a clear commit message.
6. Push the feature branch.
7. Open a pull request.
8. Respond to code review feedback.
9. Ensure all required CI checks pass before merging.

The goal is to keep `main` stable while allowing developers to work independently through feature branches.

---

# License

Add the project's applicable license here once it has been formally selected.