import re, json

# Define the path of the input file
input_file_path = "c:/Users/Paul CoW/Documents/MEVBlocker/Agnostic_relay/table"

# Define the path of the output file
output_file_path = "c:/Users/Paul CoW/Documents/MEVBlocker/Agnostic_relay/block19511131.txt"


# Open the input file in read mode
with open(input_file_path, "r") as input_file:
    # Read all the lines from the input file
    lines = input_file.readlines()

# Open the output file in write mode
with open(output_file_path, "w") as output_file:
    # Iterate over each line
    i=0
    for line in lines:
        a = re.split(' |\t', line.strip())
        # Check if the line meets the criteria
        if i>57:
            if json.loads(a[7])['ExecutionPayload']['blockNumber'] == 19511131:
                # Write the line to the output file
                output_file.write(line)
        i+=1
    if i%100==0:
        print(i)