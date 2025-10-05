# Todo Application

A simple, modern todo application built with React and Azure Functions, using Azure Table Storage for data persistence.

## Tech Stack

### Frontend
- React 18 with Vite
- Vanilla CSS for styling
- Fetch API for data fetching

### Backend
- Azure Functions v4 (Python)
- Azure Table Storage for data persistence
- Python 3.13 

## Project Structure

```
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── services/       # API service layer
│   │   ├── App.jsx        # Main application component
│   │   └── index.css      # Global styles
│   ├── .env               # Environment variables
│   └── package.json
│
├── backend/                # Azure Functions backend
│   ├── function_app.py    # Function app with endpoints
│   ├── storage.py         # Azure Table Storage client
│   └── requirements.txt    # Python dependencies
│
└── main.bicep             # Infrastructure as Code
```

## Features
- Create new tasks
- List all tasks
- Clean and responsive UI
- Error handling and loading states
- Cross-Origin Resource Sharing (CORS) enabled

## Local Development

### Prerequisites
- Node.js 18 or higher
- Python 3.13 or higher
- Azure Functions Core Tools v4
- Azure CLI (for deployment)
- Azure Storage Account (for Table Storage)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `local.settings.json` file:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AzureWebJobsStorage": "YOUR_STORAGE_CONNECTION_STRING"
     }
   }
   ```

4. Start the Functions host:
   ```bash
   func start
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file:
   ```
   VITE_API_BASE_URL=http://localhost:7071/api
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`

## Deployment to Azure

### Prerequisites
- Azure subscription
- Azure CLI installed and logged in

### Deployment Steps

1. Login to Azure:
   ```bash
   az login
   ```

2. Create a resource group:
   ```bash
   az group create --name todo-app-rg --location eastus
   ```

3. Deploy the infrastructure using Bicep:
   ```bash
   az deployment group create \
     --resource-group todo-app-rg \
     --template-file main.bicep
   ```

4. Deploy the backend:
   ```bash
   cd backend
   func azure functionapp publish <your-function-app-name>
   ```

5. Deploy the frontend:
   ```bash
   cd frontend
   npm run build
   az storage blob upload-batch -d '$web' -s dist --account-name <your-storage-account-name>
   ```

### Infrastructure Components (Bicep)

The `main.bicep` file creates:
- Storage Account for frontend static hosting
- Storage Account for backend data
- Function App for backend API
- Application Insights for monitoring

### Environment Configuration

After deployment, update these settings:
1. Function App application settings with storage connection string
2. Frontend environment variables with production API URL
3. CORS settings in Function App to allow frontend domain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License