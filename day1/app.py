# --- Part 1 ---
l1 = []
l2 = []

for line in open("day1/input1.txt"):
    num1, num2 = line.split("   ")
    l1.append(int(num1))
    l2.append(int(num2))
    
sorted_l1 = sorted(l1)
sorted_l2 = sorted(l2)

distance = 0
for i in range(len(sorted_l1)):
    distance += abs(sorted_l1[i] - sorted_l2[i])
    
print(distance)

# --- Part 2 ---
similarity = 0
for num in l1:
    similarity += num * l2.count(num)
    
print(similarity)