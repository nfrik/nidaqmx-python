import pprint
import nidaqmx

pp = pprint.PrettyPrinter(indent=4)

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("AI/ai0")

    print('1 Channel 1 Sample Read Raw: ')
    data = task.read_raw()
    pp.pprint(data)

    print('1 Channel N Samples Read Raw: ')
    data = task.read_raw(number_of_samples_per_channel=8)
    pp.pprint(data)

    task.ai_channels.add_ai_voltage_chan("AI/ai1:3")

    print('N Channel 1 Sample Read Raw: ')
    data = task.read_raw()
    pp.pprint(data)

    print('N Channel N Samples Read Raw: ')
    data = task.read_raw(number_of_samples_per_channel=8)
    pp.pprint(data)