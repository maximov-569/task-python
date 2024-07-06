from src.db import new_session
from src.service_state.models import Service, ServiceStateHistory
from src.service_state.schemas import SHService, SHServiceStateHistory, ServiceSlaInput
from sqlalchemy import select, or_


class ServiceRepository:
    @classmethod
    async def insert_or_update(cls, service: SHService):
        """
        Insert or update a service in the database.

        Args:
            service (SHService): The service object to be inserted or updated.
        """
        async with new_session() as session:
            # Check if the service already exists in the database
            query = select(Service).where(Service.name == service.name)
            service_object = await session.execute(query)
            service_object = service_object.scalars().first()

            # Retrieve the last state of the service for history tracking
            last_state = await session.execute(
                select(ServiceStateHistory)
                .where(ServiceStateHistory.service.has(name=service.name))
                .order_by(ServiceStateHistory.time_in.desc())
                .limit(1)
            )
            last_state = last_state.scalar()

            # Insert a new service if it doesn't exist
            if service_object is None:
                service_object = Service(**service.model_dump())
                session.add(service_object)
                await session.flush()

            # Create a new service state history entry
            service_history = ServiceStateHistory(
                state=service.state,
                description=service.description,
                service_id=service_object.id,
            )

            session.add(service_history)
            await session.flush()

            # Update the time_out of the previous state if it exists
            if last_state is not None:
                last_state.time_out = service_history.time_in
                session.add(last_state)

            await session.commit()

    @classmethod
    async def get_services(cls):
        """
        Get all services from the database.

        Returns:
            list[SHService]: A list of all services.
        """
        async with new_session() as session:
            query = select(Service)
            result_query = await session.execute(query)
            result = [
                SHService.model_validate(service, from_attributes=True)
                for service in result_query.scalars().all()
            ]
            return result

    @classmethod
    async def get_history_by_name(cls, *, service_name: str):
        """
        Get the history of a service by name from the database.

        Args:
            service_name (str): The name of the service.

        Returns:
            list[SHServiceStateHistory]: A list of service state history objects.
        """
        async with new_session() as session:
            query = select(ServiceStateHistory).where(
                ServiceStateHistory.service.has(name=service_name)
            )
            result_query = await session.execute(query)
            result = [
                SHServiceStateHistory.model_validate(service, from_attributes=True)
                for service in result_query.scalars().all()
            ]
            return result

    @classmethod
    async def get_history_by_name_for_sla(
        cls,
        *,
        service_name: str,
        dates: ServiceSlaInput,
    ):
        """
        Get the history of a service by name for SLA calculation from the database.

        Args:
            service_name (str): The name of the service.
            dates (ServiceSlaInput): The date interval for calculating SLA.

        Returns:
            list[SHServiceStateHistory]: A list of service state history objects for SLA.
        """
        async with new_session() as session:
            query = select(ServiceStateHistory).where(
                ServiceStateHistory.service.has(name=service_name),
                or_(
                    ServiceStateHistory.time_out >= dates.interval_start,
                    ServiceStateHistory.time_out.is_(None),
                ),
                ServiceStateHistory.time_in <= dates.interval_end,
            )
            result_query = await session.execute(query)
            result = [
                SHServiceStateHistory.model_validate(service, from_attributes=True)
                for service in result_query.scalars().all()
            ]
            return result
