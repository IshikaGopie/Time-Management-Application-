import timeManagementTwo

# ----------------
# TASK DATA
# ----------------

tasks_dates = ['2022-04-11', '2022-04-09', '2022-04-03', '2022-04-17', '2022-04-18']

start_time_tasks = ['08:00 AM', '10:00 AM', '11:00 AM', '04:00 PM', '05:00 PM']

task_duration = [2, 1, 3, 1, 2]


# ---------------
# ASSIGNMENT DATA
# ---------------

assignment_id = [1235, 1658, 4859, 7468, 7146]

assignment_title = ['COMP 3608 A1', 'INFO 2606 A2', 'INFO 3606 A4', 'COMP 3601 A3', 'COMP 3602 A5']

assignment_durations = [5, 3, 7, 4, 1]

priorities = [5, 1, 4, 2, 1]

assignment_start_dates = ['2022-04-11', '2022-04-09', '2022-04-03', '2022-04-17', '2022-04-18']

assignment_end_dates = ['2022-04-20', '2022-04-18', '2022-04-17', '2022-04-30', '2022-05-03']


# --------------
# MODULE USE
# --------------

timeline = []
timeline = timeManagementTwo.get_timeline(assignment_start_dates, assignment_end_dates, timeline)

scheduled_tasks = timeManagementTwo.init_schedule(start_time_tasks, tasks_dates, task_duration, timeline)

scheduled_assignments = timeManagementTwo.get_scheduled_assignments(scheduled_tasks, assignment_id, assignment_title,
                                                                    assignment_durations, priorities,
                                                                    assignment_start_dates, assignment_end_dates,
                                                                    timeline)

print(timeline)
print("\n")

for i in scheduled_tasks:
    print(i)

print("\n")

for i in scheduled_assignments:
    print(i)
