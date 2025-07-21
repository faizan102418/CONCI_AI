# conci-ai-assistant/backend/src/api/v1/pms_pos.py
# This file defines API endpoints for mocking PMS/POS interactions.

from fastapi import APIRouter, HTTPException, status

# Import the mock PMS/POS service and Pydantic models
from ...services.mock_pms_pos import mock_pms_pos_service
from ...core.models import SpaBookingRequest, HotSOSCreationRequest, OperationResponse

# Create an API router specific to PMS/POS related endpoints
router = APIRouter()

@router.post("/book_spa_slot/", response_model=OperationResponse, summary="Simulate booking a spa slot")
async def book_spa_slot_endpoint(request: SpaBookingRequest):
    """
    **Endpoint to simulate booking a spa slot.**

    Expects a JSON body with details for the booking (date, time, service, customer_name).
    Uses the mock PMS/POS service to simulate the booking operation.
    """
    try:
        # Call the mock PMS/POS service to simulate booking
        message = await mock_pms_pos_service.book_spa_slot(request.dict())
        return OperationResponse(status="success", message=message)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred during spa slot booking: {str(e)}"
        )

@router.post("/create_hotsos_task/", response_model=OperationResponse, summary="Simulate creating a HotSOS maintenance task")
async def create_hotsos_task_endpoint(request: HotSOSCreationRequest):
    """
    **Endpoint to simulate creating a HotSOS maintenance task.**

    Expects a JSON body with task details (description, priority).
    Uses the mock PMS/POS service to simulate task creation.
    """
    try:
        # Call the mock PMS/POS service to simulate task creation
        message = await mock_pms_pos_service.create_hotsos_task(request.description, request.priority)
        return OperationResponse(status="success", message=message)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred during HotSOS task creation: {str(e)}"
        )