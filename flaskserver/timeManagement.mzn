include "globals.mzn";   

int: num_tasks;
int: num_slots;
int: num_days;

set of int: slots = 1..num_slots;
set of int: tasks = 1..num_tasks+1;
set of int: days  = 1..num_days;

array[slots,days] of var tasks: schedule;
      
                                                                                       
array[slots,days] of var 0..1: Scheduled_tasks; 


                           %Tasks  1 2 3 4 5 6 7
array[tasks] of int: duration; 
array[tasks] of int: priority; 
array[tasks] of int: start_date;
array[tasks] of int: end_date;

constraint forall(i in slots, j in days)(if Scheduled_tasks[i,j] = 1 then schedule[i,j] = num_tasks + 1 endif);

var set of tasks: s;
s = array2set(array1d(schedule));

constraint forall(t in s)(if t <= num_tasks then count(schedule,t) = duration[t] endif);

constraint forall(i in slots, j in days)(if Scheduled_tasks[i,j] = 0 /\ schedule[i,j] <= num_tasks then  j >= start_date[schedule[i,j] ] /\ j <= end_date[schedule[i,j] ] endif);

var int: cost = sum([priority[i] | i in s]);

solve maximize cost;

output[show2d(schedule)];