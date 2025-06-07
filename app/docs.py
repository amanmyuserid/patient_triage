# app/docs.py

from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Patient Triage API",
        version="1.0.0",
        description="This API classifies patient messages into medical triage categories and stores historical interactions.",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://img.icons8.com/external-flat-icons-inmotus-design/344/external-medical-healthcare-flat-icons-inmotus-design.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema



success_example = {
    "success": True,
    "data": {
        "current_result": {
            "category": "emergency",
            "confidence": 0.9432
        },
        "history": [
            {
                "message": "I want to talk to doctor",
                "category": "follow-up",
                "confidence": 0.8923
            }
        ]
    },
    "error": None
}

validation_error_example = {
    "success": False,
    "data": None,
    "error": {
        "field": "mobile",
        "message": "Mobile number must be 10 digits and start with 6 or 7 or 8 or 9."
    }
}

predict_endpoint_docs = {
    "summary": "Predict triage category",
    "description": "Classifies a patient message and returns triage category + message history for the user.",
    "responses": {
        200: {
            "description": "Successful prediction",
            "content": {
                "application/json": {
                    "example": success_example
                }
            }
        },
        422: {
            "description": "Validation error (customized)",
            "content": {
                "application/json": {
                    "example": validation_error_example
                }
            }
        }
    }
}