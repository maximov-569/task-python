from src.service_state.models import StateChoice


async def calculate_sla(history, time_now, dates):
    """
    Calculate the service level agreement (SLA) based on the given service history, current time, and date interval.

    Args:
        history (list[SHServiceStateHistory]): The list of service state history objects.
        time_now (datetime): The current time.
        dates (ServiceSlaInput): The date interval for calculating SLA.

    Returns:
        str: The calculated SLA as a percentage.
    """
    # Sort the history list by time_in
    times = list(sorted(history, key=lambda x: x.time_in))

    # If there is only one item in the history, return 0 if the state is down or 100 if the state is up
    if len(times) == 1:
        return "0%" if times[0].state == StateChoice.down else "100%"

    # If the interval end is greater than the current time, set it to the current time
    if dates.interval_end > time_now:
        dates.interval_end = time_now

    # Set the time_in of the first item in the history to the interval start if it is earlier than the interval start
    times[0].time_in = (
        dates.interval_start
        if times[0].time_in < dates.interval_start
        else times[0].time_in
    )

    # Set the time_out of the last item in the history to the interval end
    times[-1].time_out = dates.interval_end

    # Calculate the full time and down time
    full_time = (times[-1].time_out - times[0].time_in).total_seconds()
    down_time = sum(
        [
            (time.time_out - time.time_in).total_seconds()
            for time in times
            if time.state == StateChoice.down
        ]
    )

    # Calculate the SLA
    result = ((full_time - down_time) / full_time) * 100

    # Return the SLA as a percentage
    return str(round(result, 3)) + "%"
