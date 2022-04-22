from datetime import datetime, timedelta
from minizinc import Instance, Model, Solver

schedule = Model("./flaskserver/timeManagement.mzn")

chuffed = Solver.lookup("chuffed")

instance = Instance(chuffed, schedule)

time_slots = ['08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM',
              '03:00 PM', '04:00 PM', '05:00 PM', '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM']


def get_timeline(assignment_start_dates, assignments_end_dates, timeline):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(min(assignment_start_dates), date_format)
    end = datetime.strptime(max(assignments_end_dates), date_format)
    step = timedelta(days=1)
    while start <= end:
        timeline.append(str(start.date()))
        start += step
    return timeline


def get_date_numbers(assignment_start_dates, assignment_end_dates, timeline, assignment_start_indexes,
                     assignment_end_indexes):
    for i in assignment_start_dates:
        s = timeline.index(i)
        assignment_start_indexes.append(s + 1)
    for j in assignment_end_dates:
        e = timeline.index(j)
        assignment_end_indexes.append(e + 1)
    assignment_start_indexes.append(0)
    assignment_end_indexes.append(0)
    return assignment_start_indexes, assignment_end_indexes


def set_data(assignment_durations, priority, assignment_start_dates, assignment_end_dates, timeline):
    num_tasks = len(assignment_durations)
    assignment_durations.append(0)
    priority.append(0)
    start_indexes = []
    end_indexes = []
    start_indexes, end_indexes = get_date_numbers(assignment_start_dates, assignment_end_dates, timeline, start_indexes,
                                                  end_indexes)
    num_days = len(timeline)
    num_slots = len(time_slots) - 1
    return assignment_durations, priority, start_indexes, end_indexes, num_days, num_tasks, num_slots


def init_schedule(start_time_tasks, tasks_dates, tasks_durations, timeline):
    scheduled_tasks = [[0 for i in range(len(timeline))] for j in range(len(time_slots)-1)]
    for i in range(0, len(start_time_tasks)):
        row = time_slots.index(start_time_tasks[i])
        col = timeline.index(tasks_dates[i])
        if tasks_durations[i] > 1:
            for j in range(0, tasks_durations[i]):
                scheduled_tasks[row][col] = 1
                row += 1
        else:
            scheduled_tasks[row][col] = 1
    return scheduled_tasks


def assignment_handler(scheduled_tasks, assignment_durations, priorities, assignment_start_dates, assignment_end_dates,
                       timeline):
    assignment_durations, priorities, start_indexes, end_indexes, num_days, num_tasks, num_slots = set_data(
        assignment_durations, priorities, assignment_start_dates, assignment_end_dates, timeline)
    instance["num_tasks"] = num_tasks
    instance["num_slots"] = num_slots
    instance["num_days"] = num_days
    instance["Scheduled_tasks"] = scheduled_tasks
    instance["duration"] = assignment_durations
    instance["priority"] = priorities
    instance["start_date"] = start_indexes
    instance["end_date"] = end_indexes
    result = instance.solve()
    result = result["schedule"]
    return result, num_tasks


def get_scheduled_assignments(calendar_id, scheduled_tasks, assignment_id, assignment_title, assignment_durations, priorities,
                              assignment_start_dates, assignment_end_dates, timeline):
    scheduled_assignments = []
    results, num_tasks = assignment_handler(scheduled_tasks, assignment_durations, priorities,
                                            assignment_start_dates, assignment_end_dates, timeline)

    for x in range(0, num_tasks):
        count = 0
        for i, j in enumerate(results):
            for k, l in enumerate(j):
                if l == x + 1:
                    #print(x)
                    #print(count)
                    scheduled_assignments.append({'calendarID': calendar_id[x][count],
                                                  'id': assignment_id[x],
                                                  'title': assignment_title[x],
                                                  'start_time': time_slots[i],
                                                  'end_time': time_slots[i+1],
                                                  'date': timeline[k]})
                    count+=1
    return scheduled_assignments, results
