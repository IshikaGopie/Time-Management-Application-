import timeManagement
from collections import Counter
from datetime import datetime

file = open('test_file1.txt', 'r')
lines = file.readlines()

calendar_id = 12345

count = 0
tasks_dates = []
start_time_tasks = []
task_duration = []

assignment_id = []
assignment_title = []
assignment_durations = []
priorities = []
assignment_start_dates = []
assignment_end_dates = []

for line in lines:
    count += 1
    x = line.strip()
    if x == '-1':
        break
    x = x.split(",")
    tasks_dates.append(x[0])
    start_time_tasks.append(x[1])
    task_duration.append(int(x[2]))

i = count
while i < len(lines):
    x = lines[i].split(",")
    assignment_id.append(int(x[0]))
    assignment_title.append(x[1])
    assignment_durations.append(int(x[2]))
    priorities.append(int(x[3]))
    assignment_start_dates.append(x[4])
    assignment_end_dates.append(x[5].strip())
    i += 1

print("****Input Data****")
print('Task Data', '\n')
print(tasks_dates, '\n')
print(start_time_tasks, '\n')
print(task_duration, '\n')

print('Assignment Data', '\n')
print(assignment_id, '\n')
print(assignment_title, '\n')
print(assignment_durations, '\n')
print(priorities, '\n')
print(assignment_start_dates, '\n')
print(assignment_end_dates, '\n')

# --------------
# MODULE USE
# --------------

timeline = []
timeline = timeManagement.get_timeline(assignment_start_dates, assignment_end_dates, timeline)

print("****Time Line****")
print(timeline)
print("\n")

print("****Scheduled_Tasks****")
scheduled_tasks = timeManagement.init_schedule(start_time_tasks, tasks_dates, task_duration, timeline)

for i in scheduled_tasks:
    print(i)
print("\n")

print("****Scheduled_Assignments****")
scheduled_assignments, results = timeManagement.get_scheduled_assignments(calendar_id, scheduled_tasks, assignment_id,
                                                                          assignment_title,
                                                                          assignment_durations, priorities,
                                                                          assignment_start_dates, assignment_end_dates,
                                                                          timeline)

for i in scheduled_assignments:
    print(i)

print('\n')

# --------
# TESTING
# -------

print("****Tests****")


def checkDurations():
    c = Counter()
    for assignment in scheduled_assignments:
        c[assignment["id"]] += 1
    keys = c.keys()
    for k in keys:
        index = assignment_id.index(k)
        if assignment_durations[index] != c[k]:
            return False
    return True


def checkScheduledDate():
    for i in scheduled_assignments:
        id = i['id']
        index = assignment_id.index(id)
        date = i['date']
        scheduled_date = datetime.strptime(date, "%Y-%m-%d")
        start_date = datetime.strptime(assignment_start_dates[index], "%Y-%m-%d")
        end_date = datetime.strptime(assignment_end_dates[index], "%Y-%m-%d")
        if start_date > scheduled_date >= end_date:
            return False
    return True


def checkBlockedTimeSlots():
    for i, j in enumerate(scheduled_tasks):
        for k, l in enumerate(j):
            if scheduled_tasks[i][k] == 1 and results[i][k] != len(assignment_id) + 1:
                return False
    return True


if checkDurations():
    print('Durations test passed!')
else:
    print('Durations test failed!')

if checkScheduledDate():
    print('Date Test Passed!')
else:
    print('Date Test Failed!')

if checkBlockedTimeSlots():
    print('Blocked time slots test passed!')
else:
    print('Blocked time slots test failed!')