from datetime import datetime, UTC

from fastapi import APIRouter

from src.service_state.repository import ServiceRepository
from src.service_state.schemas import SHService, SHServiceStateHistory, ServiceSlaInput
from src.service_state.utils import calculate_sla

router = APIRouter(
    prefix="/service",
    tags=["service"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def post_service(service: SHService) -> dict[str, str]:
    """
    Endpoint to insert or update a service.

    Args:
        service (SHService): The service object to be inserted or updated.

    Returns:
        dict[str, str]: A dictionary with the state of the operation.
    """
    await ServiceRepository.insert_or_update(service)
    return {"state": "success"}


@router.get("/")
async def get_service() -> list[SHService]:
    """
    Endpoint to get all services.

    Returns:
        list[SHService]: A list of all services.
    """
    result = await ServiceRepository.get_services()
    return result


@router.get("/{service_name}")
async def get_service_state(service_name: str) -> list[SHServiceStateHistory]:
    """
    Endpoint to get the history of a specific service by name.

    Args:
        service_name (str): The name of the service.

    Returns:
        list[SHServiceStateHistory]: A list of service state history objects.
    """
    result = await ServiceRepository.get_history_by_name(service_name=service_name)
    return result


@router.post("/{service_name}/sla")
async def get_sla(service_name: str, dates: ServiceSlaInput) -> {}:
    """
    Endpoint to calculate SLA for a specific service.

    Args:
        service_name (str): The name of the service.
        dates (ServiceSlaInput): The date interval for calculating SLA.

    Returns:
        dict: A dictionary containing the service name and its calculated SLA.
    """
    history = await ServiceRepository.get_history_by_name_for_sla(
        service_name=service_name,
        dates=dates,
    )
    if not history:
        return {"details": "No history found"}
    result = await calculate_sla(history, datetime.now(UTC), dates)
    return {"service_name": service_name, "sla": result}
