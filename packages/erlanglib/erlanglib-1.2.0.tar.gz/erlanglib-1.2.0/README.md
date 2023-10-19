# erlanglib - An Erlang Library
This Erlang library provides functions to assist in teletraffic engineering, offering functions based on Erlang formulas. Erlang formulas are widely used in the telecommunications industry for calculating various metrics such as call blocking probability, probability of call queuing, service levels, and more.

## Table of Contents

- [Installation](#installation)
- [General Functions](#general-functions)
- [Erlang B Functions](#erlang-b-functions)
- [Erlang C Functions](#erlang-c-functions)
- [Usage](#usage)

## Installation

You can install erlanglib via pip:
```
pip install erlanglib
```

## General Functions

**factorial(n)**  
Calculates the factorial of n.

**calculate_erlangs(call_duration_hours, calls_per_hour)**  
Given the average call duration in hours and calls initiated per hour, it returns the traffic in Erlangs.

**calculate_erlangs_seconds(call_duration_seconds, calls_per_second)**  
Given the average call duration in seconds and calls initiated per second, it calculates the traffic in Erlangs in terms of hours.

**calculate_erlangs_minutes(call_duration_minutes, calls_per_minute)**  
Given the average call duration in minutes and calls initiated per minute, it calculates the traffic in Erlangs in terms of hours.

**calls_per_second_from_erlangs(erlangs, call_duration_seconds)**  
Given the traffic in Erlangs and average call duration, it calculates the calls initiated per second.

**call_duration_from_erlangs(erlangs, calls_per_second)**  
Given the traffic in Erlangs and calls initiated per second, it calculates the average call duration in seconds.

## Erlang B Functions

**erlang_b(N, A)**  
Calculates the blocking probability using the Erlang B formula.

**required_channels(A, target_blocking)**  
Given the traffic in Erlangs and a desired blocking probability, it calculates the required number of channels.

**calculate_erlangs_from_blocking(N, target_blocking)**  
Given the blocking probability and available lines, it calculates the traffic in Erlangs.

## Erlang C Functions

**erlang_c(N, A)**  
Calculates the probability that a call is queued using the Erlang C formula.

**service_level(N, A, Pw, target_time_seconds, AHT_seconds)**  
Given various parameters including the probability a call is queued, it calculates the service level.

**average_speed_of_answer(N, A, Pw, average_handling_time)**  
Given the probability a call is queued, number of agents, traffic in Erlangs, and average handling time, it calculates the Average Speed of Answer.

**immediate_answer_percentage(Pw)**  
Given the probability a call is queued, it calculates the percentage of calls answered immediately.

**occupancy(A, N)**  
Given the traffic in Erlangs and the number of agents, it calculates the agent utilization in percentage.

**required_agents(N_raw, shrinkage_percentage)**  
Given the raw number of agents and shrinkage percentage, it calculates the number of agents required.

## Usage

To use this library, simply import the desired functions and utilize them as per the requirements. Each function is accompanied by its detailed documentation, ensuring ease of use.
