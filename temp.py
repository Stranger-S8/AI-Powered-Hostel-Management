data = [{'name': 'Zeeshan Abbas', 'attendance': {'lunch': True, 'breakfast': True, 'dinner': True}}]

for row in data:
    for value in row.values():
        print(value)
    