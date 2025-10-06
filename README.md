# RAMS Automater Web App

## Setup Overview
This bundle contains:
- FastAPI backend (`rams-backend`)
- React frontend (`rams-frontend`)

### Local Test
Run the backend:
    cd backend
    pip install -r requirements.txt
    uvicorn backend.main:app --reload

Run the frontend:
    cd frontend
    yarn install
    yarn start

### Render Deployment
1. Push to GitHub
2. Connect to Render (render.yaml auto-detects)
3. Render will create:
   - rams-backend
   - rams-frontend
4. Ensure `REACT_APP_API_URL=https://rams-api.onrender.com`

### Demo Accounts
- **Admin:** admin1 / admin123
- **Approver:** approver1 / approver123
- **Creator:** creator1 / creator123

### Troubleshooting
- If the frontend calls localhost, rebuild frontend on Render.
- If CORS errors occur, check backend CORS middleware.
- If upload errors appear, confirm `python-multipart` is installed.
