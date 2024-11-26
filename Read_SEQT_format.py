# Import necessary libraries
import re


# Define the function to read the file and parse the data
def parse_earthquake_phases(input_file):
    # Data storage structures
    events = []
    current_event = None

    with open(input_file, 'r') as file:
        for line in file:
            # Detect event line (starting with event number)
            if re.match(r'\s*\d+\s+\d{4}', line):
                # Save current event if it exists
                if current_event:
                    events.append(current_event)

                # Parse new event details
                event_data = line.split()
                event_id = int(event_data[0])
                origin_time = ' '.join(event_data[1:5])
                relative_time = float(event_data[5])

                # Initialize new event
                current_event = {
                    'event_id': event_id,
                    'origin_time': origin_time,
                    'relative_time': relative_time,
                    'phases': []
                }

            # Detect phase line (starting with network code)
            elif re.match(r'\s+[A-Z]{2}\s+\S+', line):
                # Parse phase details
                phase_data = line.split()
                phase = {
                    'network_code': phase_data[0],
                    'station_code': phase_data[1],
                    'phase_type': phase_data[2],
                    'relative_time': float(phase_data[3]),
                    'magnitude': float(phase_data[4]),
                    'value1': float(phase_data[5]),
                    'value2': float(phase_data[6]),
                    'uncertainty': float(phase_data[7]),
                    'azimuth': float(phase_data[8])
                }
                # Add phase to current event
                current_event['phases'].append(phase)

    # Add the last event
    if current_event:
        events.append(current_event)

    return events


# Function to write parsed earthquake events to a new text file in the specified format
def write_earthquake_data(output_file, events):
    with open(output_file, 'w') as file:
        for event in events:
            # Write event header line
            file.write(f"{event['origin_time']} L {event['relative_time']} ")
            file.write("BER  5 .50 2.9LBER                1\n")
            file.write("GAP=177   BER  1.34       4.2     3.4  8.4 -0.6081E+01  0.6370E+00 -0.1746E+02E\n")
            file.write(
                f"{event['origin_time'].replace(' ', '-')}S.NSN___018                                                 6\n")
            file.write("STAT COM NTLO IPHASE   W HHMM SS.SSS   PAR1  PAR2 AGA OPE  AIN  RES W  DIS CAZ7\n")

            # Write each phase line
            for phase in event['phases']:
                hhmm = f"{int(phase['relative_time'] // 60):02}:{int(phase['relative_time'] % 60):02}"
                ss_sss = f"{phase['relative_time'] % 60:.3f}"
                file.write(f"{phase['station_code']} {phase['network_code']} {phase['phase_type']} IP "
                           f"{hhmm} {ss_sss} BER opt {phase['value1']} {phase['uncertainty']} {phase['azimuth']}\n")


# Example usage
input_file = './input.out'  # Replace with your file name
output_file = './generated.out'
earthquake_data = parse_earthquake_phases(input_file)

# Write the parsed data to the output file
write_earthquake_data(output_file, earthquake_data)

print("Data processing complete. Check the output file:", output_file)
