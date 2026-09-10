# VRI Platform for Inclusive Communication (Uganda)

A national, multi-channel Video Relay Interpreting (VRI) infrastructure designed to bridge the communication gap between Deaf or Hard of Hearing individuals and hearing participants across public service domains including Healthcare, Justice, Education, and Public Administration.

---

## System Architecture and Unified Tech Stack

This repository contains the unified local development environment and system configuration designed to ensure absolute consistency across all developer machines, testing environments, and deployment targets.

### The 3-Layer Communication Model
To guarantee communication access regardless of network bandwidth or device type, the platform utilizes a graceful degradation model:
1. Layer 1: Real-Time Video (WebRTC) - Encrypted, low-latency live video streaming (targeting under 2 to 3 seconds latency) for high-speed network environments.
2. Layer 2: Asynchronous Video (MMS Gateway) - Queued sign-language video messages for areas with intermittent network coverage.
3. Layer 3: Text and Voice Relay (GSM/SMS) - Offline fallback where Deaf users interact via SMS and interpreters call the hearing participant vocally.

### Unified Technology Stack
* Web Frontend: React.js
* Mobile Frontend: React Native
* Backend API Server: Python (Django and Django REST Framework)
* Relational Database: PostgreSQL 15
* Local Containerization: Docker and Docker Compose

---

## Getting Started (Local Development Sandbox)

We use Docker to containerize our application services. This guarantees that dependencies, configurations, and network setups are identical across all developer workstations.

### Prerequisites
Ensure your local workstation has the following installed:
* Git (v2.30+)
* Docker Desktop (with the WSL 2 backend enabled on Windows)

---

### Step 1: Initial Local Setup
Clone this repository to your local machine and navigate into the project root:

```bash
git clone https://github.com/YOUR_USERNAME/vri-platform-uganda.git
cd vri-platform-uganda
Verify that you have the necessary configuration files in your root folder:
Dockerfile (Django environment specification)
docker-compose.yml (Service orchestration blueprint)
requirements.txt (Backend package list)
.env (Local environment variables)
.gitignore (Excludes local database volumes and system secrets)

### Step 2: Running the System
To build, configure, and start the local Django backend and PostgreSQL database, run a single command in your terminal:
docker-compose up
What is happening under the hood:
Docker pulls the official PostgreSQL 15 (Alpine) database image and initializes vri_uganda_db.
Docker builds our Django application container from the lightweight python:3.12-slim image, installs compile-time dependencies, and links our Python package requirements.
A shared local network is configured, dynamically exposing the PostgreSQL port (5432) and mounting the Django app on port 8000 with hot-reloading enabled. Any code edits you make locally will immediately refresh the container.
Step 3: Running Django Management Commands
Because your database and backend are isolated inside the Docker network, you run management commands inside the active container. Open a new terminal window in VS Code (Ctrl + ~) and use these standard commands:

1.  --- Run Database Migrations

Keep your PostgreSQL schema updated with our models:
docker-compose exec backend python manage.py migrate

2. ---Create a Platform Superuser

====== To access the built-in Django Admin Panel:=======
docker-compose exec backend python manage.py createsuperuser
After creating your credentials, navigate to http://localhost:8000/admin in your web browser to log in.
Git Branching and Collaboration Guidelines
To maintain production-grade software standards, we enforce strict branching controls in our repository. Never commit directly to the main or develop branches.
Branch Structure
main: Represents production-ready, stable code. Only merged during release phases.
develop: The primary integration branch. All feature branches are merged here.
feature/feature-name: Individual workspaces for developer tasks (e.g., feature/webrtc-routing, feature/mms-queues).


====== DevOps Support and Troubleshooting =======
If you hit any environment errors during setup:
Ensure no local PostgreSQL instances are running on your machine and blocking port 5432.
If your database state gets corrupted, wipe the volume and start clean:
docker-compose down -v
docker-compose up