from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
import threading
from fastapi import status

from . import models, schemas, database, classifier
from .database import SessionLocal, engine

from . import docs  # 👈 import your custom doc module
from .docs import predict_endpoint_docs 



models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Triage API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# at the end of your file
app.openapi = lambda: docs.custom_openapi(app)

# Warm up model on startup
threading.Thread(target=lambda: classifier.classify_text("I need help now"), daemon=True).start()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post(
    "/predict",
    response_model=schemas.StandardResponse,
    **predict_endpoint_docs  # Inject all metadata here cleanly
)
def predict(request: schemas.PatientRequest, db: Session = Depends(get_db)):
    try:
        category, confidence = classifier.classify_text(request.message)

        new_msg = models.PatientMessage(
            name=request.name,
            mobile=request.mobile,
            message=request.message,
            category=category,
            confidence=confidence
        )
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)  # Required to access generated ID

        previous = db.query(models.PatientMessage).filter(
            models.PatientMessage.mobile == request.mobile,
            models.PatientMessage.id != new_msg.id
        ).order_by(models.PatientMessage.timestamp.desc()).all()

        history = [
            schemas.PredictionResult(
                message=msg.message,
                category=msg.category,
                confidence=msg.confidence
            ) for msg in previous
        ]

        return schemas.StandardResponse(
            success=True,
            data=schemas.PatientResponse(
                current_result=schemas.CurrentResult(
                    category=category,
                    confidence=confidence
                ),
                history=history
            ),
            error=None
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=schemas.StandardResponse(
                success=False,
                data=None,
                error={"message": str(e)}
            ).dict()
        )

# Friendly error messages for validation
FRIENDLY_MESSAGES = {
    "mobile": "Mobile number must be 10 digits and start with 6 or 7 or 8 or 9.",
    "name": "Name must be at least 2 characters long.",
    "message": "Message cannot be empty.",
}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    field = first_error['loc'][-1]
    message = FRIENDLY_MESSAGES.get(field, "Invalid input.")

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(schemas.StandardResponse(
            success=False,
            data=None,
            error={
                "field": field,
                "message": message
            }
        ))
    )
