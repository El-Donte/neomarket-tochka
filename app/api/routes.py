from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/stub")
def stub():
    return{
        "success": True,
        "data": [],
        "message": "This is a stub endpoint"
    }