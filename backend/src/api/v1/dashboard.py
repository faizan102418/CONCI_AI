# conci-ai-assistant/backend/src/api/v1/dashboard.py
# This file defines API endpoints for the centralized receptionist dashboard.

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

# Import models for tasks and staff
from ...core.models import Task, TaskUpdateRequest, StaffMember, OperationResponse

# Import the TaskManager service
from ...services.task_manager import task_manager

# Create an API router specific to dashboard-related endpoints
router = APIRouter()

@router.get("/tasks/", response_model=List[Task], summary="Get all current tasks for the dashboard")
async def get_all_tasks_api():
    """
    Retrieves a list of all tasks currently managed by the system.
    Tasks are typically sorted by creation date, newest first.
    """
    try:
        tasks = task_manager.get_all_tasks()
        return tasks
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )

@router.get("/tasks/{task_id}", response_model=Task, summary="Get a specific task by ID")
async def get_task_by_id_api(task_id: str):
    """
    Retrieves details for a single task identified by its unique ID.
    """
    task = task_manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found."
        )
    return task

@router.put("/tasks/{task_id}", response_model=Task, summary="Update an existing task (e.g., status, assignment)")
async def update_task_api(task_id: str, request: TaskUpdateRequest):
    """
    Updates the details of an existing task.
    Can be used to change status (pending, assigned, completed, cancelled)
    or to assign the task to a staff member.
    """
    updated_task = task_manager.update_task(task_id, request)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found or update failed."
        )
    return updated_task

@router.get("/staff/", response_model=List[StaffMember], summary="Get list of available staff members")
async def get_staff_members_api():
    """
    Retrieves a list of all available staff members who can be assigned tasks.
    """
    try:
        staff = task_manager.get_staff_members()
        return staff
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve staff members: {str(e)}"
        )

# Note: Task creation is handled by the voice/text command endpoints
# where the LLM identifies a task and passes it to the task_manager.