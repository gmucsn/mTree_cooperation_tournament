

path1 = "./logs/tournament_test-2021_08_26-02_54_48_PM-experiment.data"
experiment_log = open(path1, "r")

log_data = experiment_log.readlines()  #each line turns into str

result = []

counter = 1
for line in log_data:
    #if counter < 91:
        #counter = counter +1 
    #else:
        line = line.rstrip()
        line_str = line.split("\t")
        
        timestamp = float(line_str[0])
        data = line_str[1]
        result.append((timestamp,data))

result.sort(key=lambda tup: tup[0])

path2 = "./logs/data.txt"
path3 = "./logs/results.txt"

output_log = open(path2,"w")

for line in result: 
    line = str(line)
    line = line[1:-1]
    output_log.write(str(line)+"\n")

output_log.close()

results_log = open(path3,"w")

write_lines = []
for x in range(len(result)):
    if result[x][1] == "game completed":
        write_lines.append(result[x])
        for y in range(5):
            if "Agent" in result[x+y][1]:
                write_lines.append(result[x+y])
        #write_lines.append(result[x+2])
        #write_lines.append(result[x+4])

for line in write_lines:
    line = str(line)
    line = line[1:-1]
    results_log.write(str(line)+"\n")


results_log.close()

print(f"Converted {path1} to {path2}")

#df = pd.DataFrame(result)
#df.to_csv("data_file.csv",index=False)
