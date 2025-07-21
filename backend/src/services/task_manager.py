# conci-ai-assistant/backend/src/services/task_manager.py
# This file manages the creation, retrieval, and updating of tasks for the dashboard.
# Currently uses an in-memory list to simulate a database.

import uuid
from typing import List, Optional, Dict
from datetime import datetime

# Import the Task and StaffMember models
from ..core.models import Task, StaffMember, TaskCreateRequest, TaskUpdateRequest

class TaskManager:
    """
    Manages hotel tasks, including guest requests and staff assignments.
    Uses an in-memory list for task storage.
    """
    def __init__(self):
        self.tasks: List[Task] = []
        # Mock staff members for assignment
        self.staff_members: List[StaffMember] = [
            StaffMember(id="staff_hk_001", name="Maria Rodriguez", role="Housekeeping"),
            StaffMember(id="staff_mt_002", name="David Chen", role="Maintenance"),
            StaffMember(id="staff_rs_003", name="Sarah Lee", role="Room Service"),
            StaffMember(id="staff_fr_004", name="Tom Jenkins", role="Front Desk"),
        ]
        print("TaskManager initialized with mock staff and empty task list.")

    def get_all_tasks(self) -> List[Task]:
        """Retrieves all current tasks."""
        # Sort tasks by creation time, newest first
        return sorted(self.tasks, key=lambda t: t.created_at, reverse=True)

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieves a single task by its ID."""
        return next((task for task in self.tasks if task.id == task_id), None)

    def create_task(self, request: TaskCreateRequest) -> Task:
        """
        Creates a new task based on a guest request.
        Generates a unique ID and sets initial status to 'pending'.
        """
        new_task = Task(
            id=str(uuid.uuid4()), # Generate a unique ID for the task
            guest_request=request.guest_request,
            room_number=request.room_number,
            category=request.category,
            priority=request.priority,
            status="pending",
            created_at=datetime.now()
        )
        self.tasks.append(new_task)
        print(f"TaskManager: Created new task: {new_task.id} - '{new_task.guest_request}'")
        return new_task

    def update_task(self, task_id: str, update_data: TaskUpdateRequest) -> Optional[Task]:
        """
        Updates an existing task's status or assignment.
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None # Task not found

        # Update status if provided
        if update_data.status:
            task.status = update_data.status
            if update_data.status == "completed":
                task.completed_at = datetime.now()
            elif update_data.status == "assigned" and not task.assigned_at:
                task.assigned_at = datetime.now() # Set assigned_at only once

        # Assign staff if assigned_to_id is provided
        if update_data.assigned_to_id:
            staff = next((s for s in self.staff_members if s.id == update_data.assigned_to_id), None)
            if staff:
                task.assigned_to = staff
                if task.status == "pending": # Automatically set to assigned if pending
                    task.status = "assigned"
                if not task.assigned_at:
                    task.assigned_at = datetime.now()
            else:
                print(f"TaskManager: Warning - Staff member with ID {update_data.assigned_to_id} not found.")

        print(f"TaskManager: Updated task {task.id}. New status: {task.status}, Assigned to: {task.assigned_to.name if task.assigned_to else 'None'}")
        return task

    def get_staff_members(self) -> List[StaffMember]:
        """Retrieves the list of available staff members."""
        return self.staff_members

# Instantiate the TaskManager. This instance will be used across your API endpoints.
task_manager = TaskManager()