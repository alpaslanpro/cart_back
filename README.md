# Korzina Cart API

A RESTful API for managing shopping carts built with FastAPI and MongoDB. The API provides comprehensive cart management features including product lookup, automatic price calculation, and checkout functionality.

## Features

- **Cart Management**: Create, retrieve, update, and delete shopping carts
- **Product Integration**: Automatic product name and price lookup
- **Real-time Calculations**: Automatic total price calculation based on product prices and quantities
- **Comprehensive CRUD**: Full cart and item management operations
- **Checkout Process**: Complete order processing with detailed summaries
- **Administrative Tools**: List all carts for management purposes

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database with Motor async driver
- **Pydantic**: Data validation and serialization
- **Python 3.8+**: Required Python version

## Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cart_back
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Create a `requirements.txt` file with the following content:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
motor==3.3.2
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
pymongo==4.6.0
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB=cartdb
```

For MongoDB Atlas, use:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB=cartdb
```

### 5. Project Structure

Ensure your project structure looks like this:

```
cart_back/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── mongo.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cart.py
│   │   └── product.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── cart.py
│   │   └── product.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── cart.py
│   │   └── product.py
│   └── routers/
│       ├── __init__.py
│       ├── cart.py
│       └── product.py
├── requirements.txt
├── .env
└── README.md
```

### 6. Run the Application

```bash
# Make sure virtual environment is activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## API Endpoints

### Product Endpoints

#### Create Product
```http
POST /api/v1/products/
Content-Type: application/json

{
  "name": "iPhone 15",
  "description": "Latest Apple smartphone",
  "price": 1299.99,
  "in_stock": 10
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "iPhone 15",
  "description": "Latest Apple smartphone",
  "price": 1299.99,
  "in_stock": 10
}
```

#### Get All Products
```http
GET /api/v1/products/
```

#### Get Product by ID
```http
GET /api/v1/products/{product_id}
```

### Cart Endpoints

#### 1. Create New Cart
```http
POST /api/v1/carts/
Content-Type: application/json

{
  "items": [
    {
      "productId": "507f1f77bcf86cd799439011",
      "quantity": 2
    }
  ]
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439012",
  "items": [
    {
      "product_id": "507f1f77bcf86cd799439011",
      "product_name": "iPhone 15",
      "quantity": 2,
      "price": 1299.99,
      "total_price": 2599.98
    }
  ],
  "total_amount": 2599.98
}
```

#### 2. Get Cart by ID
```http
GET /api/v1/carts/{cart_id}
```

#### 3. Add Item to Cart
```http
POST /api/v1/carts/{cart_id}/items
Content-Type: application/json

{
  "productId": "507f1f77bcf86cd799439013",
  "quantity": 1
}
```

#### 4. Update Item Quantity
```http
PUT /api/v1/carts/{cart_id}/items/{item_id}
Content-Type: application/json

{
  "quantity": 5
}
```

#### 5. Remove Item from Cart
```http
DELETE /api/v1/carts/{cart_id}/items/{item_id}
```

#### 6. Clear Cart
```http
DELETE /api/v1/carts/{cart_id}
```

#### 7. Checkout Cart
```http
POST /api/v1/carts/{cart_id}/checkout
Content-Type: application/json

{}
```

**Response:**
```json
{
  "cart_id": "507f1f77bcf86cd799439012",
  "items": [
    {
      "product_id": "507f1f77bcf86cd799439011",
      "product_name": "iPhone 15",
      "quantity": 2,
      "price": 1299.99,
      "total_price": 2599.98
    }
  ],
  "total_amount": 2599.98,
  "status": "processed"
}
```

#### 8. Get All Carts (Administrative)
```http
GET /api/v1/carts/
```

## Data Models

### Product Model
```json
{
  "id": "string",
  "name": "string",
  "description": "string (optional)",
  "price": "number (>0)",
  "in_stock": "integer (>=0)"
}
```

### Cart Item Model
```json
{
  "product_id": "string",
  "product_name": "string",
  "quantity": "integer (>0)",
  "price": "number",
  "total_price": "number"
}
```

### Cart Model
```json
{
  "id": "string",
  "items": "CartItem[]",
  "total_amount": "number"
}
```

## Usage Examples

### Complete Workflow Example

1. **Create a product:**
```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro",
    "description": "Professional laptop",
    "price": 2499.99,
    "in_stock": 5
  }'
```

2. **Create a cart:**
```bash
curl -X POST "http://localhost:8000/api/v1/carts/" \
  -H "Content-Type: application/json" \
  -d '{
    "items": []
  }'
```

3. **Add item to cart:**
```bash
curl -X POST "http://localhost:8000/api/v1/carts/{cart_id}/items" \
  -H "Content-Type: application/json" \
  -d '{
    "productId": "{product_id}",
    "quantity": 1
  }'
```

4. **Checkout:**
```bash
curl -X POST "http://localhost:8000/api/v1/carts/{cart_id}/checkout" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT, DELETE operations
- `201 Created`: Successful POST operations
- `400 Bad Request`: Invalid request data or product not found
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server errors

### Common Error Responses

```json
{
  "detail": "Product not found"
}
```

```json
{
  "detail": "Cart not found"
}
```

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting
```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGO_DB` | Database name | `cartdb` |

## Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGO_URI=mongodb://mongo:27017
      - MONGO_DB=cartdb
    depends_on:
      - mongo

  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

Run with:
```bash
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs` endpoint

## Changelog

### Version 0.1.0
- Initial release
- Basic cart and product management
- Automatic price calculation
- Checkout functionality
- MongoDB integration