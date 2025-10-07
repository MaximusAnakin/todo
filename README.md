# Todo Application

A simple, modern todo application built with React and Azure Functions, using Azure Table Storage for data persistence.

Deployed app: https://lively-sky-06633ca03.1.azurestaticapps.net/

## Tech Stack

### Frontend
- React 18 with Vite 6
- Vanilla CSS for styling
- Fetch API for data fetching

### Backend
- Azure Functions v4  (Python v2 isolated worker)
- Azure Table Storage for data persistence (cloud-only)
- Python 3.13 

## Project Structure

```
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── services/       # API service layer
│   │   ├── App.jsx         # Main application component
│   │   └── index.css       # Global styles
│   ├── .env                # Environment variables
│   └── package.json
│
├── backend/                # Azure Functions backend
│   ├── function_app.py     # Function app with endpoints
│   ├── storage.py          # Azure Table Storage client
│   └── requirements.txt    # Python dependencies
│
└── main.bicep              # Infrastructure as Code
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
- Azure Storage Account (for Table Storage, no local emulator needed)

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
       "AzureWebJobsStorage": "STORAGE_CONNECTION_STRING"
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
- GitHub repository secrets:
   - AZURE_STATIC_WEB_APPS_API_TOKEN
   - API_BASE_URL (set to your Function App’s /api endpoint)


### Deployment Steps

1. Login to Azure:
   ```bash
   az login
   ```

2. Create a resource group:
   ```bash
   az group create --name todo-app-rg --location westeurope
   ```

3. Create the Storage Account (required by the Bicep file)

   ```bash
   az storage account create \
   --name todostorageassignment \
   --resource-group todo-app-rg \
   --location westeurope \
   --sku Standard_LRS \
   --kind StorageV2
   ```

3. Deploy the infrastructure using Bicep:
   ```bash
   az deployment group create \
     --resource-group todo-app-rg \
     --template-file main.bicep
     --parameters existingStorageName=todostorageassignment \
              repoUrl=<github repo link here to use GitHub actions> \
              repoBranch=main
   ```

4. Deploy the backend:
   ```bash
   cd backend
   func azure functionapp publish todo-backend-func --python
   ```

5. Deploy the frontend:
   ⚠️ Make sure your GitHub repository is connected to the Static Web App via the Azure Portal. This enables CI/CD and injects the required deployment token (AZURE_STATIC_WEB_APPS_API_TOKEN) into your repository secrets.
   
   You must also add the GitHub Actions workflow file manually to your repository (unless Azure created it for you). The file should be located at .github/workflows/azure-static-web-apps.yml and include steps to build and upload the frontend from frontend/dist.

   ```bash
   git commit --allow-empty -m "Trigger frontend deploy"
   git push origin main
   ```

### Infrastructure Components (Bicep)

The `main.bicep` file creates:
- Azure Storage Account (for Table Storage)
- Azure Function App (Python v2 backend)
- Azure Static Web App (frontend)
- Linux Consumption Plan
- Application Insights


### Environment Configuration

After deployment, update these settings:
1. Add AzureWebJobsStorage to Function App settings
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