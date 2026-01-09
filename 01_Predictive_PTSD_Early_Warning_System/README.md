# Predictive PTSD Early Warning System

## Overview
Multi-modal passive monitoring system that predicts mental health decline 30-90 days before crisis, enabling early intervention without stigma.

## Architecture

### System Components
- **Backend API**: FastAPI-based RESTful service with PostgreSQL
- **ML Pipeline**: Gradient boosting ensemble with LSTM for time-series patterns
- **Data Ingestion**: Secure API integration with military health systems
- **Privacy Layer**: Federated learning - data never leaves local installation
- **Frontend Dashboard**: React-based commander view
- **Mobile App**: React Native for wellness check-ins

### Tech Stack
- **Backend**: Python, FastAPI, PostgreSQL (with encryption at rest)
- **ML**: TensorFlow, Scikit-learn, XGBoost
- **Data Pipeline**: Apache Airflow for ETL
- **Frontend**: React dashboard
- **Mobile**: React Native
- **Security**: FIPS 140-2 compliant encryption, HIPAA-aligned data handling
- **Deployment**: Kubernetes on DoD secure cloud

## Key Features
1. Passive Monitoring (no surveys required)
2. Privacy-Preserving (aggregated patterns)
3. Actionable Alerts (tiered: green/yellow/red)
4. Unit-Level Analytics
5. Outcome Tracking
6. Predictive Timeline (30/60/90-day forecasting)
7. Resource Integration
8. Stigma-Free Design

## Project Structure
```
├── backend/              # FastAPI backend
├── frontend/             # React dashboard
├── mobile/               # React Native app
├── ml_pipeline/          # ML models and training
├── data_pipeline/        # ETL processes
├── docker/               # Docker configurations
└── docs/                 # Additional documentation
```

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Docker & Docker Compose

### Installation
See individual component READMEs for detailed setup instructions.

## Security & Compliance
- HIPAA-aligned data handling
- FIPS 140-2 compliant encryption
- DoD IL4+ security requirements
- Federated learning for privacy preservation

