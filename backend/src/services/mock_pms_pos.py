# conci-ai-assistant/backend/src/services/mock_pms_pos.py
# This file simulates interaction with a PMS (Property Management System)
# and a POS (Point of Sale, e.g., HotSOS for task creation) system.

import asyncio
from typing import Dict

class MockPmsPosService:
    """
    Mocks functionalities typically found in a PMS/POS system,
    such as booking spa slots and creating maintenance tasks.
    """
    async def book_spa_slot(self, booking_details: Dict) -> str:
        """
        Simulates the process of booking a spa slot.
        """
        print(f"Mock PMS/POS: Attempting to book spa slot with details: {booking_details}")
        await asyncio.sleep(0.2) # Simulate API call/processing delay

        # In a real application, this would involve calling a PMS API.
        # Example: pms_api.book_slot(booking_details)
        return (f"Spa slot for {booking_details.get('service')} on "
                f"{booking_details.get('date')} at {booking_details.get('time')} "
                f"for {booking_details.get('customer_name')} confirmed.")

    async def create_hotsos_task(self, task_description: str, priority: str = "medium") -> str:
        """
        Simulates the process of creating a HotSOS maintenance task.
        """
        print(f"Mock PMS/POS: Attempting to create HotSOS task: '{task_description}' (Priority: {priority})")
        await asyncio.sleep(0.2) # Simulate API call/processing delay

        # In a real application, this would involve calling the HotSOS API.
        # Example: hotsos_api.create_task(description=task_description, priority=priority)
        return f"HotSOS task '{task_description}' with '{priority}' priority created successfully."

# Instantiate the Mock PMS/POS Service. This instance will be used across your API endpoints.
mock_pms_pos_service = MockPmsPosService()