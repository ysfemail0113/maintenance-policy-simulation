import simpy
import numpy as np
import pandas as pd

#KPI Variables
ASIS_total_downtime = 0
ASIS_completed = 0

TOBE_total_downtime = 0
TOBE_completed = 0

#Clenaning empty columns
df = pd.read_csv("train_FD001.txt", sep=" ", header=None)
df = df.dropna(axis=1)

columns = (
    ["engine_id", "cycle"] +
    [f"os{i}" for i in range(1, 4)] +
    [f"s{i}" for i in range(1, 22)]
)
df.columns = columns

failure_cycles = df.groupby("engine_id")["cycle"].max()
failure_dict = failure_cycles.to_dict() #Convertion from Pandas to python dictionary


#Simulation parameters
MAINTENANCE_CAPACITY_AsIs = 1
MAINTENANCE_DURATION = 30 #Time for service

MAINTENANCE_CAPACITY_Tobe = 2
PREVENTIVE_THRESHOLD = 50  #Regular service
MAINTENANCE_DURATION_TOBE = 22

# KPI tracking
total_downtime = 0
completed_maintenances = 0


#ENGINE PROCESS
def engine_process(env, engine_id, failure_time, maintenance_bay):
    global ASIS_total_downtime, ASIS_completed


    yield env.timeout(failure_time)
    breakdown_time = env.now

    with maintenance_bay.request() as request:
        yield request
        yield env.timeout(MAINTENANCE_DURATION)


    downtime = env.now - breakdown_time
    ASIS_total_downtime += downtime
    ASIS_completed += 1

def engine_process_preventive(env, engine_id, failure_time, maintenance_bay):
        global TOBE_total_downtime, TOBE_completed


        maintenance_time = max(failure_time - PREVENTIVE_THRESHOLD, 0)
        yield env.timeout(maintenance_time)

        request_time = env.now

        with maintenance_bay.request() as request:
            yield request
            yield env.timeout(MAINTENANCE_DURATION_TOBE)

        downtime = env.now - request_time
        TOBE_total_downtime += downtime
        TOBE_completed += 1



#RUNNING AS-IS SIMULATION
env_asis = simpy.Environment()
maintenance_bay_asis = simpy.Resource(env_asis, capacity=MAINTENANCE_CAPACITY_AsIs)

for engine_id, failure_time in failure_dict.items():
    env_asis.process(
        engine_process(env_asis, engine_id, failure_time, maintenance_bay_asis)
    )

env_asis.run()

ASIS_avg_downtime = ASIS_total_downtime / ASIS_completed


#RUNNING TO-BE SIMULATION
env_tobe = simpy.Environment()
maintenance_bay_tobe = simpy.Resource(env_tobe, capacity=MAINTENANCE_CAPACITY_Tobe)

for engine_id, failure_time in failure_dict.items():
    env_tobe.process(
        engine_process_preventive(env_tobe, engine_id, failure_time, maintenance_bay_tobe)
    )

env_tobe.run()
TOBE_avg_downtime = TOBE_total_downtime / TOBE_completed



#Comparison
improvement = (
    (ASIS_avg_downtime - TOBE_avg_downtime)
    / ASIS_avg_downtime
) * 100

print("\nRESULTS")
print("-------")
print(f"AS-IS avg downtime : {ASIS_avg_downtime:.2f}")
print(f"TO-BE avg downtime : {TOBE_avg_downtime:.2f}")
print(f"Improvement        : {improvement:.2f}%")