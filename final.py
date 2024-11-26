import re, os, sys
import numpy as np  # Import numpy for array handling
from obspy import Stream, Trace, UTCDateTime
import json

def parse_earthquake_phases(input_file):
    # Data storage structures
    events = []
    current_event = None
    stream = Stream()  # Initialize an empty obspy Stream

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
                
                # Convert origin_time to UTCDateTime
                start_time = UTCDateTime(origin_time)

                # Initialize new event
                current_event = {
                    'event_id': event_id,
                    'origin_time': start_time,
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

                # Create Trace object for each phase
                trace = Trace(data=np.array([phase['magnitude']] * 100))  # Use a NumPy array for data
                trace.stats.network = phase['network_code']
                trace.stats.station = phase['station_code']
                trace.stats.starttime = current_event['origin_time'] + phase['relative_time']
                trace.stats.sampling_rate = 1.0  # Adjust based on actual sampling rate
                
                # Append to the Stream
                stream.append(trace)

    # Add the last event
    if current_event:
        events.append(current_event)

    return events, stream


def write_earthquake_data(output_file, event):
    with open(output_file, 'w') as file:
        for event in events:
            print(event)
            # Write event header line

            # origin_time: 2012 306 0042 40.5 (YYYY day_of_year HHMM SS.1f) -> 1 houses microseconds
            formatted_origin_time = event['origin_time'].strftime('%Y %j %H%M') + f" {event['origin_time'].second + event['origin_time'].microsecond / 1e6:.1f}"
            
            file.write(f"{formatted_origin_time} L {str(event['relative_time'])} ")
            file.write("BER  5 .50 2.9LBER                1\n")
            file.write("GAP=177   BER  1.34       4.2     3.4  8.4 -0.6081E+01  0.6370E+00 -0.1746E+02E\n")

            # origin_time: 2012-11-01-00:42:40.507 (YYYY-MM-DD-HH:MM:SS.3f) -> 3 houses microseconds
            final_origin_time = event['origin_time'].strftime("%Y-%m-%d-%H:%M:%S.") + f"{event['origin_time'].microsecond // 1000:03d}"

            file.write(
                f"{final_origin_time}S.NSN___018                                                 6\n")
            file.write("STAT COM NTLO IPHASE   W HHMM SS.SSS   PAR1  PAR2 AGA OPE  AIN  RES W  DIS CAZ7\n")

            # Write each phase line
            for phase in event['phases']:
                hhmm = f"{int(phase['relative_time'] // 60):02}:{int(phase['relative_time'] % 60):02}"
                ss_sss = f"{phase['relative_time'] % 60:.3f}"
                phase_type = ""
                if phase['phase_type'] == "P":
                    phase_type = "IP"
                else:
                    phase_type = "ISg"
                """
                file.write(f"{phase['station_code']} HHZ {phase['network_code']}   {phase_type}\t  "
                           f"{hhmm} {ss_sss} BER opt {phase['value1']} {phase['uncertainty']} {phase['azimuth']}\n")
                """
                file.write(f"{phase['station_code']} HHZ {phase['network_code']}   {phase_type}\t  "
                        f"{hhmm} {ss_sss} BER opt {phase['value1']} {phase['uncertainty']} {phase['azimuth']}\n")

   

# Usage
# Load CSV file
input_file = os.path.join(os.getcwd(), 'input.out')
output_file = os.path.join(os.getcwd(), 'output.csv')
events, stream = parse_earthquake_phases(input_file)

print(events[0])

# Write the parsed data to the output file
write_earthquake_data(output_file, events[0])

'''
for trace in stream:
    trace.plot()
'''