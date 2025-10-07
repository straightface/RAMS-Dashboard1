# RAMS Automater Combined (v13)

This repo serves the frontend and backend from one Render service.

Local quick test:
- build frontend: cd frontend && yarn install && yarn build
- run backend: uvicorn backend.main:app --reload

Render: the included render.yaml builds frontend then installs backend deps and starts uvicorn.
