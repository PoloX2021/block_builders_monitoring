import re, json

# Define the path of the input file
input_file_path = "c:/Users/Paul CoW/Documents/MEVBlocker/Agnostic_relay/table"

# Define the path of the output file
output_file_path = "c:/Users/Paul CoW/Documents/MEVBlocker/Agnostic_relay/block19511148.txt"


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
        if i<=57:
            print(a)
        if i>57:
            try: 
                b = json.loads(a[7])
                if int(b['ExecutionPayload']['block_number']) == 19511148:
                    # Write the line to the output file
                    output_file.write(line)
            except:
                print("Error")
                print(a)
        i+=1
        if i%100==0:
            print(i)