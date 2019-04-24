import csv

reader = csv.reader(open('Firms with PSD Permissions (CSV).csv'))
reader1 = csv.reader(open('new.csv'))
data = {}
for new_list in reader1:
    data[new_list[0]] = new_list[6]
print(data)
for list in reader:
    if list[0] != 'FRN' and list[0] in data:
        list[6] = data[list[0]]
    with open('new1.csv', 'a', newline='') as t_file:
       csv_writer = csv.writer(t_file)
       csv_writer.writerow(list)