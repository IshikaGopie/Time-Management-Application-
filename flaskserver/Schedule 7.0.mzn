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
array[tasks] of var int: duration; 
array[tasks] of var int: priority; 
array[tasks] of var int: start_date;
array[tasks] of var int: end_date;

var int: total_time = sum([duration[i] | i in 1..num_tasks]);
var int: available_slots = num_slots * num_days;
var int: remainder_slots = available_slots - total_time;

constraint if total_time < available_slots then duration[num_tasks + 1] = remainder_slots else duration[num_tasks + 1] = 0 endif;

constraint forall(i in slots, j in days)(if Scheduled_tasks[i,j] = 1 then schedule[i,j] = num_tasks + 1 endif);

% Returns the number of occurrences of y in x .
function int: count(array[$X] of int: x, int: y);

constraint forall(i in slots, j in days)(count(schedule,schedule[i,j]) = duration[schedule[i,j]]);

var set of tasks: s;
s = array2set(array1d(schedule));
var int: cost = sum([priority[i] |  i in s]);

solve maximize cost;

output[show2d(schedule)];