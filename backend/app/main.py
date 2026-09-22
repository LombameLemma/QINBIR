from fastapi import FastAPI

app = FastAPI(
    title="QINBIR API",
    description="Smart University Course Scheduling System",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to QINBIR",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "QINBIR API",
    }