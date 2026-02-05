Project Overview###

This project uses discrete-event simulation (SimPy) to evaluate different maintenance policies and their impact on machine downtime. Rather than proposing a single optimal solution, the goal is to quantitatively compare alternative policies under controlled assumptions and demonstrate measurable improvements.

The simulation is designed as a decision-support tool, enabling managers or engineers to assess trade-offs between operational performance and cost.

Objectives###

Model an AS-IS (reactive maintenance) system
Model multiple TO-BE (policy-based) maintenance scenarios
Measure and compare average machine downtime
Extend the model with cost–benefit based decision policies

System Description###

AS-IS Model (Baseline)
Machines operate until failure
Upon failure, machines request a maintenance resource
If the maintenance bay is busy, machines queue
Downtime includes:
Waiting time in queue
Actual repair time

TO-BE Model (Policy-Based)

Maintenance is triggered before failure using a preventive threshold
Policy parameters may include:
Preventive maintenance threshold
Reduced maintenance duration
Increased maintenance capacity
The simulation measures how these policies affect average downtime per machine

Key Assumptions & Simplifications###

To keep the model interpretable and analytically valid, the following assumptions are made:
Identical machines (homogeneous fleet)
Single failure event per machine
Deterministic maintenance duration (policy-dependent)
No partial failures or repair quality degradation
Failure time derived from historical operational data
These assumptions are intentional and acceptable for policy comparison, not for exact real-world prediction.

KPIs ###

Average Downtime per Machine,
Number of completed maintenance operations,
Queue-induced waiting time (implicit),
Improvement is reported as:Improvement (%) = (AS-IS Avg Downtime − TO-BE Avg Downtime) / AS-IS Avg Downtime

<img src="./img.png">

