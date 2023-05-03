import csv
import sys
import collections
import turtle
from collections import Counter
import svgwrite
import xml.etree.ElementTree as ET
import tkinter as tk

file_path1 = sys.argv[1]

file_path2 = sys.argv[2]

def createFlamegraphSVG(file_path, title):
    stack_traces = list()

    unique_functions = list()

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        
        column_values = [row[5] for row in csv_reader]
        
        for value in column_values:
            stack_traces.append(value.split(';'))
            
    barLength = len(stack_traces)
            
    bars = []
            
    for trace in stack_traces:
        for i, element in enumerate(trace):
            if i >= len(bars):
                bars.append([element])
            else:
                bars[i].append(element)
                
    bars = bars[:32]

    count = 0

    dwg = svgwrite.Drawing(title + ".svg", size=(1500, 1000))
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='#181716'))

    functionCount = Counter(bars[0])

    total = sum(functionCount.values())

    min_count = total * 0.05

    functionCount = {k: v for k, v in functionCount.items() if v >= min_count and k != ''}

    total = sum(functionCount.values())

    proportions = {k: v / total for k, v in functionCount.items()}

    proportions = {k: v for k, v in proportions.items() if v >= 0.1 and k}

    def drawFlame(func, offset, proportion, height, depth, width):
        w = width * proportion
        h = 40
        x = offset
        y = height
        if title == 'flamegraph1':
            if func[0:3] == '[k]':
                color = svgwrite.rgb(20, 35, 125, '%')
            elif func[0:3] == 'run':
                color = svgwrite.rgb(25, 30, 125, '%')
            else:
                color = svgwrite.rgb(20, 25, 125, '%')
        else:
            if func[0:3] == '[k]':
                color = svgwrite.rgb(20, 80, 40, '%')
            elif func[0:3] == 'run':
                color = svgwrite.rgb(25, 80, 30, '%')
            else:
                color = svgwrite.rgb(20, 80, 20, '%')
        dwg.add(dwg.rect(insert=(x, y), size=(w, h), fill=color))
        if len(func) > w/4:
            sub = func[:3] + "..."
        else:
            sub = func
        text = dwg.text(sub, insert=(x, y + h / 2), font_size=(14), fill='#000')
        
        if w > 10:
            dwg.add(text)
        
        next_calls = set()
        for trace in stack_traces:
            if func in trace:
                index = trace.index(func)
                if index < len(trace) - 1:
                    next_calls.add(trace[index + 1])
                    
        if len(bars) > depth+1:
        
            functionCount = Counter(bars[depth+1])
            
            functionCount = {k: v for k, v in functionCount.items() if k in next_calls}
            
            if len(functionCount) > 0:
            
                total = sum(functionCount.values())
                
                min_count = total * 0.05

                functionCount = {k: v for k, v in functionCount.items() if v >= min_count and k != ''}

                total = sum(functionCount.values())

                proportions = {k: v / total for k, v in functionCount.items()}

                proportions = {k: v for k, v in proportions.items() if v >= 0.1 and k}
                
                for k, v in proportions.items():
                    drawFlame(k, x, v, height - 40, depth+1, w)
                    x = x + (w * v)
        
        
        

    offset = 100
    width = 1300
    for k, v in proportions.items():
        
        drawFlame(k, offset, v, 900, 0, width)
        
        offset = offset + (width * v)
        
    dwg.save()
    


createFlamegraphSVG(file_path1, "flamegraph1")
createFlamegraphSVG(file_path2, "flamegraph2")
