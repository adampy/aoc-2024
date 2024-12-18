f = open("day2/input.txt", "r")
reports = [line.strip() for line in f.readlines()]
f.close()

# --- Part 1 ---

def is_report_safe(report):
    levels = report.split(" ")
    curr = None
    is_safe = True
    increasing = None
    for level in levels:
        if curr is None:
            curr = int(level)
            
        else:
            if increasing is None:
                increasing = curr < int(level)
            
            if increasing and int(level) < curr:
                is_safe = False
                break
            elif not increasing and int(level) > curr:
                is_safe = False
                break  
            
            diff = abs (curr - int(level))
            if diff > 3 or diff < 1:
                is_safe = False
                break
            
            curr = int(level)
            
    return is_safe

safe_reports = sum([is_report_safe(report) for report in reports])
print(f"Safe reports: {safe_reports}")

# --- Part 2 ---
is_potentially_safe = 0
for report in reports:
    # remove each level and check if it's still safe
    levels = report.split(" ")
    for i in range(len(levels)):
        new_report = " ".join(levels[:i] + levels[i+1:])
        if is_report_safe(new_report):
            is_potentially_safe += 1
            break
print(f"Potentially safe reports: {is_potentially_safe}")