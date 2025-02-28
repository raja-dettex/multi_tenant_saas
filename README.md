# Multi-Tenant SaaS API with FastAPI, Citus, MongoDB

## Step 1: Clone the Repository
Clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-folder>
```

## Step 2: Set Up Environment Variables
Rename the `.env.example` file to `.env` and update the database credentials if necessary:

```bash
cp .env.example .env
```

Edit the `.env` file and configure:

```ini
DATABASE_URL=postgresql://postgres:password@citus_coordinator:5432/multi_tenant_db
MONGO_URI=mongodb://admin:secret@mongodb:27017/audit_logs_db
SECRET_KEY=your-secret-key
```

## Step 3: Build and Run with Docker
Run the following command to build and start all services:

```bash
docker-compose up --build -d
```

This will start:

- FastAPI (API server)
- PostgreSQL with Citus (sharded database)
- MongoDB (audit logs)

## Step 4: Verify Running Containers
Check if all containers are running:

```bash
docker ps
```



## Step 5: Run Database Migrations
Once the services are running, initialize the PostgreSQL database and distribute tables in Citus:

```bash
docker exec -it multi_tenant_api bash -c "python -m app.db.init_db"
```

## Step 6: Access the API
Once the database is initialized, you can access the FastAPI docs at:

```
http://localhost:8000/docs
```

Use this interactive documentation to test API endpoints.

### API Usage

#### Tenant Management
- **Create a Tenant:**

```bash
curl -X POST "http://localhost:8000/tenants/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Corp"}'
```

#### User Authentication
- **Register a New User:**

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -H "X-Tenant: test_corp" \
     -d '{"username": "admin", "email": "admin@testcorp.com", "password": "password123"}'
```

- **Login and Get a JWT Token:**

```bash
curl -X POST "http://localhost:8000/auth/login/" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@testcorp.com", "password": "password123"}'
```

- **Access a Protected Endpoint:**

```bash
curl -X GET "http://localhost:8000/users/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "X-Tenant: test_corp"
```

## Testing
Run unit tests with:

```bash
pytest
```

## Scaling and Deployment
This system is designed to scale by:

- Running multiple FastAPI instances behind a load balancer.
- Using Citus to shard PostgreSQL for multi-tenancy.
- Implementing MongoDB sharding for high-volume audit logs.

To deploy on Kubernetes, consider using Helm charts and Cloud-managed databases.

## Contributing
1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to your fork and create a pull request.

## Future Improvements
- Implement background tasks for asynchronous processing.
- Add WebSockets for real-time notifications.
- Enhance tenant-based billing system using Stripe.

```bash
docker logs multi_tenant_api
```

