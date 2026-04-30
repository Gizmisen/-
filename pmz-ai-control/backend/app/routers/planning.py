from fastapi import APIRouter

router = APIRouter(prefix='/planning', tags=['planning'])

@router.get('/health')
def health():
    return {'module':'planning','status':'ready','message':'Module scaffold is ready for implementation'}
