import nidaqmx
import matplotlib.pyplot as plt
import numpy as np
import time
import logging

logger = logging.getLogger(__name__)
def simple_experiment():
    with nidaqmx.Task() as taskin, nidaqmx.Task() as taskout:
        taskout.ao_channels.add_ao_voltage_chan("AO/ao0")
        taskin.ai_channels.add_ai_voltage_chan("AI/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
        taskin.ai_channels.add_ai_voltage_chan("AI/ai1",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
        taskin.timing.cfg_samp_clk_timing(1000,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
        t=np.linspace(0,1,30)
        signal=np.sin(2*np.pi*3*t)
        signal=0*np.ones(100)
        taskout.write(signal, auto_start=True)
        result=[]
        # for s in signal:
        #     # time.sleep(0.01)
        #     taskout.write(s, auto_start=True)
        #     # result.append(taskin.read(number_of_samples_per_channel=2))

        result = taskin.read(number_of_samples_per_channel=100)
        # taskout.write(0, auto_start=True)
        print(result)

    plt.figure()
    plt.subplot(211)
    plt.plot(result[0])
    plt.plot(result[1])
    plt.subplot(212)
    plt.plot(signal)
    plt.show()


def nidaq_single_sim(X,y, inputids, outputids, eq_time):

    logger.debug("Setting up inputs: {} for outputs: {} ".format(X, y))

    with nidaqmx.Task() as taskin, nidaqmx.Task() as taskout:
        for inputid, idnum in zip(inputids, range(len(inputids))):
            taskout.ao_channels.add_ao_voltage_chan("AO/ao{}".format(inputid))
        taskout.write(X, auto_start=True)

        time.sleep(eq_time)

        outvals = []
        # print("Done equilibrating, reading output values")
        logger.info("Done equilibrating, reading output values")
        for outid in outputids:
            taskin.ai_channels.add_ai_voltage_chan("AI/ai{}".format(outid),min_val=-10.0, max_val=10.0,terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
        result = taskin.read(number_of_samples_per_channel=1)
        outvals.append(result)

        outvals.append(y)
    return outvals

def nidaq_circuit_eval(X, y, inputids, outputids, eq_time):
    results = []

    for xx,yy in zip(X,y):
        results.append(nidaq_single_sim(X=xx,y=yy,inputids=inputids,outputids=outputids,eq_time=eq_time))

    return results

def main():
    # X=[1,2,3]
    # y=[0]
    # outvals1 = nidaq_single_sim(X,y,inputids=[0,1,2],outputids=[0,1,2],eq_time=0.1)
    # print(outvals1)
    # X = [-1, -2, -3]
    # outvals2 = nidaq_single_sim(X, y, inputids=[0,1,2], outputids=[0, 1,2], eq_time=0.1)
    # print(outvals2)
    # X=[[1,2,3],[-1,-2,-3],[7.23,7.24,-7.25]]
    n=10
    # X=np.random.random((n,3))*3
    X=np.ones((n,3))*3.001
    y=np.ones(n)
    result = nidaq_circuit_eval(X,y,inputids=[0,1,2],outputids=[0,1,2],eq_time=0.00)
    print(X)
    print(result)
    # 2.9996851733847802], [2.9996851733847802], [3.0009987072145923]
    # plt.figure()
    # plt.subplot(211)
    # plt.plot(outvals1)
    # plt.show()
    # print(outvals2)

if __name__ == "__main__":
    main()