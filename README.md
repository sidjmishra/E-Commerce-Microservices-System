# E-Commerce Microservices System

A microservices-based system for a simple e-commerce application. The system handles user authentication, product management, and order processing. Emphasis is placed on implementing concurrency control and ensuring high availability through clustering.

## Requirements

### Microservices Architecture

1. **User Authentication Service**: Manages user registration, login, and authentication.
2. **Product Management Service**: Manages product CRUD operations with concurrency control.
3. **Order Processing Service**: Manages order creation, retrieval, and processing.

### Technology Stack

- **Programming Language**: Python
- **Framework**: Flask
- **Database**: MongoDB
- **Concurrency Control**: Optimistic locking
- **Clustering**: Docker Swarm or Kubernetes for container orchestration

## Detailed Implementation

### 1. User Authentication Service

**Endpoints**:
- `POST /register`: Register a new user
```bash
{
    "username": "USERNAME",
    "password": "PASSWORD"
}
```
- `POST /login`: Authenticate a user and issue a JWT token
```bash
{
    "username": "USERNAME",
    "password": "PASSWORD"
}
```

**Authentication**: JWT for token-based authentication

### 2. Product Management Service

**Endpoints**:
- `GET /products`: List all products
- `POST /products`: Add a new product
```bash
{
    "name": "NAME",
    "description": "DESCRIPTION",
    "price": "PRICE",
    "stock": "STOCK"
}
```
- `PUT /products/<product_id>`: Update product details
```bash
{
    "name": "NAME",
    "description": "DESCRIPTION",
    "price": "PRICE",
    "stock": "STOCK"
}
```
- `DELETE /products/<product_id>`: Delete a product

**Concurrency Control**: Optimistic locking using a version field

### 3. Order Processing Service

**Endpoints**:
- `POST /orders`: Create a new order
```bash
{
    "product_id": "PRODUCT_ID",
    "quantity": "QUANTITY",
    "total_price": "TOTAL_PRICE"
}
```
- `GET /orders/<order_id>`: Get order details
- `GET /orders/user/<user_id>`: List orders for a specific user
- `PUT /orders/<order_id>`: Update order status
```bash
{
    "status": "STATUS"
}
```

## Implementation Steps

### 1. Set Up Project Structure

Create a directory for each microservice:
- `auth_service/`
- `product_service/`
- `order_service/`

### 2. Create Flask Applications

Initialize Flask applications in each service directory and define the required endpoints.

### 3. Database Integration

Set up MongoDB connections and define the schema for each service.

### 4. Implement Concurrency Control

Add versioning to the product schema and implement optimistic locking in the product update endpoint.

### 5. Set Up Docker and Clustering

Create Dockerfiles for each service and set up a Docker Swarm for clustering.

### 6. Implement Authentication and Authorization

Add JWT-based authentication to the user authentication service and protect the necessary endpoints in other services.

## Running the Microservices

### Running Locally

#### Prerequisites

- Python 3.8 or higher
- MongoDB installed and running on `localhost:27017`
- `pip` for installing Python packages

#### Steps

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd ecommerce_microservices
   ```

2. **Install Dependencies**

   For each service, navigate to its directory and install the required dependencies:

   ```bash
   cd auth_service
   pip install -r requirements.txt
   ```

   ```bash
   cd product_service
   pip install -r requirements.txt
   ```

   ```bash
   cd order_service
   pip install -r requirements.txt
   ```

3. **Run the Services**

   Start each Flask service in separate terminal windows:

   ```bash
   cd auth_service
   python app.py
   ```

   ```bash
   cd product_service
   python app.py
   ```

   ```bash
   cd order_service
   python app.py
   ```

   Each service will run on its default port (e.g., `auth_service` on port 5000, `product_service` on port 5001, and `order_service` on port 5002). You can interact with the APIs using tools like Postman or curl.

## Deployment Instructions

### Clone the Repository

```bash
git clone <repository_url>
cd E-Commerce-Microservices-System
```

### Build Docker Images

```bash
docker build -t auth_service ./auth_service
docker build -t product_service ./product_service
docker build -t order_service ./order_service
```

### Set Up Docker Swarm

```bash
docker swarm init
docker stack deploy -c docker-compose.yml ecommerce
```

### Access the Services

The services will be available on the specified ports. Use tools like Postman or curl to interact with the APIs.