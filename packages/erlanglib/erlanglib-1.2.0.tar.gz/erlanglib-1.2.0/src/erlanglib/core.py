import math
from decimal import Decimal, getcontext

# Set the precision to a high value
getcontext().prec = 1000


def factorial(n):
    """
    Calculate factorial of n.
    """
    if n == 0:
        return Decimal(1)
    result = Decimal(1)
    for i in range(1, int(n) + 1):
        result *= i
    return result


def calculate_erlangs(call_duration_hours, calls_per_hour):
    """
    Calculate the traffic in Erlangs.

    Parameters:
    - call_duration_hours (float): Average call duration in hours.
    - calls_per_hour (float): Calls initiated per hour.

    Returns:
    - float: traffic in Erlangs
    """
    call_duration_hours = Decimal(call_duration_hours)
    calls_per_hour = Decimal(calls_per_hour)
    return float(call_duration_hours * calls_per_hour)


def calculate_erlangs_seconds(call_duration_seconds, calls_per_second):
    """
    Calculate the traffic in Erlangs based on input in seconds.

    Parameters:
    - call_duration_seconds (float): Average call duration in seconds.
    - calls_per_second (float): Calls initiated per second.

    Returns:
    - float: traffic in Erlangs
    """
    # Convert call duration to hours
    call_duration_hours = Decimal(call_duration_seconds) / Decimal(3600)

    # Convert calls per second to calls per hour
    calls_per_hour = Decimal(calls_per_second) * Decimal(3600)

    return calculate_erlangs(call_duration_hours, calls_per_hour)


def calculate_erlangs_minutes(call_duration_minutes, calls_per_minute):
    """
    Calculate the traffic in Erlangs based on input in minutes.

    Parameters:
    - call_duration_minutes (float): Average call duration in minutes.
    - calls_per_minute (float): Calls initiated per minute.

    Returns:
    - float: traffic in Erlangs
    """
    # Convert call duration to hours
    call_duration_hours = Decimal(call_duration_minutes) / Decimal(60)

    # Convert calls per minute to calls per hour
    calls_per_hour = Decimal(calls_per_minute) * Decimal(60)

    return calculate_erlangs(call_duration_hours, calls_per_hour)



def calls_per_second_from_erlangs(erlangs, call_duration_seconds):

    """
    Calculate calls per second given Erlangs and call duration.

    Parameters:
    - erlangs (float): Offered traffic in Erlangs.
    - call_duration_seconds (float): Average call duration in seconds.

    Returns:
    - float: Calls initiated per second.
    """

    call_duration_hours = call_duration_seconds / 3600
    calls_per_hour = erlangs / call_duration_hours
    return calls_per_hour / 3600


def call_duration_from_erlangs(erlangs, calls_per_second):

    """
    Calculate average call duration given Erlangs and calls per second.

    Parameters:
    - erlangs (float): Offered traffic in Erlangs.
    - calls_per_second (float): Calls initiated per second.

    Returns:
    - float: Average call duration in seconds.
    """

    calls_per_hour = Decimal(calls_per_second) * Decimal(3600)
    return float(erlangs / calls_per_hour * 3600)


def erlang_b(N, A):
    """
    Calculate the blocking probability using the Erlang B formula.

    Parameters:
    - N (int): number of channels
    - A (float): traffic load in Erlangs

    Returns:
    - float: blocking probability
    """
    A, N = Decimal(A), Decimal(N)
    B = (A ** N) / factorial(N)
    denominator_summation = sum((A ** i) / factorial(i) for i in range(int(N) + 1))

    return float(B / denominator_summation)


def required_channels(A, target_blocking):

    """
    Calculate the required number of channels for a given traffic and target blocking probability.

    Parameters:
    - A (float): traffic load in Erlangs
    - target_blocking (float): desired blocking probability

    Returns:
    - int: required number of channels
    """

    N = 1  # Start with 1 channel
    while True:
        blocking_probability = erlang_b(N, A)
        if blocking_probability <= target_blocking:
            return N
        N += 1


def calculate_erlangs_from_blocking(N, target_blocking, max_iterations=1000, tolerance=1e-6):

    """
    Calculate the traffic in Erlangs given the blocking probability and available lines.

    Parameters:
    - N (int): number of channels
    - target_blocking (float): desired blocking probability
    - max_iterations (int, optional): maximum iterations for the approximation. Default is 1000.
    - tolerance (float, optional): the difference in blocking probability to consider as converged. Default is 1e-6.

    Returns:
    - float: traffic in Erlangs
    """

    low, high = 0, N * 1000
    for _ in range(max_iterations):
        mid = (low + high) / 2.0
        current_blocking = erlang_b(N, mid)
        if abs(current_blocking - target_blocking) < tolerance:
            return mid
        elif current_blocking < target_blocking:
            low = mid
        else:
            high = mid
    return mid  # Return the last calculated value if not converged in max_iterations


def erlang_c(N, A):

    """
    Calculate the probability that a call is queued using the Erlang C formula.

    Parameters:
    - N (int): number of servers (agents)
    - A (float): traffic load in Erlangs

    Returns:
    - float: probability that a call is queued
    """
    A = Decimal(A)
    numerator = (A ** N) / factorial(N) * N / (N - A)
    denominator_summation = sum((A ** i) / factorial(i) for i in range(N))
    denominator = denominator_summation + ((A ** N) / factorial(N)) * N / (N - A)
    return float(numerator / denominator)


def service_level(N, A, Pw, target_time_seconds, AHT_seconds):
    """
    Calculate the service level given the probability a call is queued, number of agents, traffic in Erlangs, target answer time, and average handle time.

    Parameters:
    - N (int): number of servers (agents).
    - A (float): traffic load in Erlangs.
    - Pw (float): probability a call is queued.
    - target_time_seconds (float): desired answer time for the calls in seconds.
    - AHT_seconds (float): average handle time for the calls in seconds.

    Returns:
    - float: service level
    """

    A, N, Pw = Decimal(A), Decimal(N), Decimal(Pw)
    exponent = - (N - A) * (Decimal(target_time_seconds) / Decimal(AHT_seconds))
    return float(Decimal(1) - Pw * exponent.exp())


def average_speed_of_answer(N, A, Pw, average_handling_time):
    """
    Calculate the Average Speed of Answer (ASA) given the probability a call is queued, number of agents, traffic in Erlangs, and average handling time.

    Parameters:
    - N (int): number of servers (agents).
    - A (float): traffic load in Erlangs.
    - Pw (float): probability a call is queued.
    - average_handling_time (float): average duration for handling a call in seconds.

    Returns:
    - float: Average Speed of Answer in seconds
    """
    A, N, Pw, average_handling_time = Decimal(A), Decimal(N), Decimal(Pw), Decimal(average_handling_time)
    return float((Pw * average_handling_time) / (N - A))


def immediate_answer_percentage(Pw):
    """
    Calculate the percentage of calls answered immediately given the probability a call is queued.

    Parameters:
    - Pw (float): probability a call is queued.

    Returns:
    - float: percentage of calls answered immediately
    """
    Pw = Decimal(Pw)
    return float(Decimal(1) - Pw) * 100


def occupancy(A, N):

    """
    Calculate the Occupancy (Agent Utilization) given the traffic in Erlangs and the number of agents.

    Parameters:
    - A (float): traffic load in Erlangs.
    - N (int): number of servers (agents).

    Returns:
    - float: Occupancy (Agent Utilization) in percentage.
    """

    return (A / N) * 100


def required_agents(N_raw, shrinkage_percentage):

    """
    Calculate the number of agents required given the raw agents and shrinkage percentage.

    Parameters:
    - N_raw (int): number of raw agents.
    - shrinkage_percentage (float): shrinkage in percentage.

    Returns:
    - int: number of agents required.
    """

    return math.ceil(N_raw / (1 - shrinkage_percentage / 100))





