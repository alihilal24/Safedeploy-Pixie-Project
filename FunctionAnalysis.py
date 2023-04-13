import csv
import sys
import collections

file_path = sys.argv[1]

exclude = sys.argv[2]

func = ""

if len(sys.argv) > 3:
    func = sys.argv[3]
    func = func + ';'
    trace = True
else:
    trace = False

stack_traces = list()

unique_functions = list()

with open(file_path, 'r') as file:
    csv_reader = csv.reader(file)
    
    column_values = [row[5] for row in csv_reader]
    
    for value in column_values:
        if trace:
            index = value.find(func)  # or use index = text.index(keyword)
            if index == -1:
                insert = None  # keyword not found
            else:
                insert = value[index+len(func):].strip() 
            if insert != None:
                stack_traces.append(insert.split(';'))
        else:
            stack_traces.append(value.split(';'))
        
for trace in stack_traces:
    for function in trace:
        unique_functions.append(function)
        
runtime = 'runtime.'
kernel = '[k]'

string_counts = collections.Counter(unique_functions)

if exclude == 'true':
    string_counts = {k: v for k, v in string_counts.items() if not k.startswith(runtime)}
    string_counts = {k: v for k, v in string_counts.items() if not k.startswith(kernel)}

sorted_counts = sorted(string_counts.items(), key=lambda x: x[1], reverse=True)


for item in sorted_counts:
    print(item[0], ':', item[1])