import simpy
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time as tm



"""
assuming the env.now is  in microsecond. 


"""

mon_t = []
que_len = []
def monitor(env, res, time_delay):
    while True: 
        mon_t.append(env.now)
        que_len.append(len(res.queue))
        yield env.timeout(0.000005)#wait 5micorsecond between sampling
# method to calculate expected gap. 
def expected_Gap(): 
    st = None  #size of the trailing packet. 
    li = None #link rate respectivley
    sh = None  #size of the heading packet
    delta = (st/li) - (sh/li)  # dispercsiom gap calculation
    eG = (st/li) + delta  #expected gap calculation. 

    return eG
#mthod ot calculate measured gap.
def measured_Gap(): 
    pass

#calling resource method 
def call_res(res, env, p, out_rate):
    #request a resource 
    with  res.request() as req:
        try:

            print('{} :packet arrived at {:f}'.format(p, env.now))
            yield req
            print("{} :packet is being  processed {:f}".format(p, env.now))
            yield env.timeout(out_rate)
            #yield env.timeout(np.random.exponential(1.0/3.0))
            print("{} :packet is departed {:f}".format(p , env.now))
        except simpy.Interrupt:
            print("Inturrepted by simpy {:f}".format(env.now)) 

    
def calc_rate(mbps, pkt_size):
    byte = 8
    micro_sec = 10**6 # ten to the power of 6 = 1 micro second
    rate = (pkt_size *byte)/(mbps * micro_sec)
    return rate

    
def cross_traffic_gen(env):
    #tmp varout_rate = int(input('Enter the output link rate in Mbps: '))
    out_rate = 1000
    #tmp varpkt_Size = int(input('Eneter the packet size in bytes: '))
    pkt_Size = 64
    #tmp varlink_speed = int(input('Enter the input link rate in Mbps: '))
    link_speed = 1000
    #outpt_rate = out_rate
    inpt_rate = calc_rate(link_speed, pkt_Size)
    outpt_rate = calc_rate(out_rate, pkt_Size)
    

    if not pkt_Size and not link_speed: 
        print("All values needs to be entered.  Values given are Pakcet size given: {} packet size, {} link speed ) ".format(pkt_Size,link_speed))
    else: 
        print('================================================================================')
        print('input link rate is: {:f} (micro sec) '.format(inpt_rate))
        print('output link rate is: {:f} (micro sec)'.format(outpt_rate))
        print('================================================================================')
    print('\nPausing...  (Hit ENTER to continue, type quit or q  to exit.)')
   
    """
    try:
        response = input()
        if response == 'quit' or response == 'q':
            sys.exit()
        else:
            print ('Resuming...')
    except KeyboardInterrupt:
        print ('Resuming...')
    """
    #tmp varflow1 = float(input('flow 1 rate in mbps: '))
    #flow1 = np.random.uniform(20.6, 300.8)
    flow1 = 245.7699965381952
    flow1_rate = calc_rate(flow1,pkt_Size)
    #tmp varflow2 = float(input('flow 2 rate in mbps: '))
    #flow2 = np.random.uniform(20.0,200.3 )
    flow2 = 106.2091476282832
    flow2_rate = calc_rate(flow2,pkt_Size)
    #tmp varflow3 = float(input('flow 3 rate in mbps: '))
    #flow3 = np.random.uniform(200.1, 300.5 )
    flow3 = 212.3763543491658
    flow3_rate = calc_rate(flow3,pkt_Size)
    flow4 = 172.28077668021533
    #flow4 = np.random.uniform(10, 200.5)
    flow4_rate = calc_rate(flow4,pkt_Size)
    """
    #put rates in ascending order. 
    flows = [flow1_rate, flow2_rate, flow3_rate]
    asc_order = sorted(flows)
    sml_rate = asc_order[0]
    med_rate = asc_order[1]
    lrg_rate = asc_order[2]
    """
    print(flow1_rate, flow2_rate, flow3_rate,flow4_rate)
    t_flow = flow1 + flow2 + flow3 + flow4
    if t_flow > out_rate:# the total flow can not exceed  output link 
        
        print('Total flow can not be more than {}mbps input link'.format(out_rate))
        sys.exit()
    """
    with open("C:\\Users\\Joykill\\Desktop\\sim_project\\usrinpt_1000mpbs.txt", "a+") as f: 
        t = (str(flow1_rate) + '|' + str(flow2_rate)+' |' + str(flow3_rate) + '|' + str(flow4_rate))
        f.write(str(flow1))
        f.write('\n')
        f.write(str(flow2))
        f.write('\n')
        f.write(str(flow3))
        f.write('\n')
        f.write(str(flow4))
        f.write('\n')
        f.write(t)
        f.write('\n')
        f.write("time is:  " + tm.strftime("%Y%m%d-%H%M%S")+'---------------------------\n')

    """
    return inpt_rate, outpt_rate, flow1_rate, flow2_rate, flow3_rate, pkt_Size, flow4_rate
class Packet(object):
    def __init__(self, time, size, id, src="a", dst="z", flow_id=0):
        self.time = time
        self.size = size
        self.id = id
        self.src = src
        self.dst = dst
        self.flow_id = flow_id
        
    def __repr__(self):
        return "id: {}, src: {}, time: {}, size: {}".\
            format(self.id, self.src, self.time, self.size)
class PacketGenerator(object):
    def __init__(self, env, id,  adist, sdist, initial_delay=0, finish=float("inf"), flow_id=0):
        self.id = id
        self.env = env
        self.adist = adist
        self.sdist = sdist
        self.initial_delay = initial_delay
        self.finish = finish
        self.out = None
        self.packets_sent = 0
        self.action = env.process(self.run())  # starts the run() method as a SimPy process
        self.flow_id = flow_id

    def run(self):
        """The generator function used in simulations.
        """
        yield self.env.timeout(self.initial_delay)
        while self.env.now < self.finish:
            # wait for next transmission
            yield self.env.timeout(self.adist)
            self.packets_sent += 1
            p = Packet(self.env.now, self.sdist, self.packets_sent, src=self.id, flow_id=self.flow_id)
            self.out.put(p)
class PacketSink(object):
    def __init__(self, env, out_rate,  rec_arrivals=False, absolute_arrivals=False, rec_waits=True, debug=False, selector=None):
        self.res = simpy.Resource(env, capacity=1)
        self.env = env
        self.rec_waits = rec_waits
        self.rec_arrivals = rec_arrivals
        self.absolute_arrivals = absolute_arrivals
        self.waits = []
        self.arrivals = []
        self.debug = debug
        self.packets_rec = 0
        self.bytes_rec = 0
        self.selector = selector
        self.last_arrival = 0.0
        self.out_rate = out_rate
        self.time_delay = 0.0

    def put(self, pkt):
        if not self.selector or self.selector(pkt):
            now = self.env.now
            env.process(call_res(self.res,self.env,pkt.id,self.out_rate))
            time_delay = self.env.now - pkt.time
            if self.rec_waits:
                self.waits.append(self.env.now - pkt.time)

            if self.rec_arrivals:
                if self.absolute_arrivals:
                    self.arrivals.append(now)
                else:
                    self.arrivals.append(now - self.last_arrival)
                self.last_arrival = now
            self.packets_rec += 1
            self.bytes_rec += pkt.size
            if self.debug:
                print(pkt)
        
#tmp var time = int(input('Enter time in Micro seconds, how long you want to run the simulation for: ')) 
time = 0.001
microsec_time = time / 10**6  # put this in run variables. 
env = simpy.Environment()
#res = simpy.Resource(env,capacity=1)
pram = cross_traffic_gen(env )# store it in param tuple. 
p0  = PacketGenerator(env,'flow1',pram[2],pram[5])
p1  = PacketGenerator(env,'flow2',pram[3],pram[5])
p2  = PacketGenerator(env,'flow3',pram[4],pram[5])
p3  = PacketGenerator(env,'flow4',pram[6],pram[5])
ps  = PacketSink(env,pram[1],debug=True)
p0.out = ps 
p1.out = ps 
p2.out = ps
p3.out = ps
env.process(monitor(env, ps.res, ps.time_delay))
env.run(until = time)

"""
#draw the plot
plt.figure()
plt.plot(mon_t,que_len)
plt.xlabel('time (\u00B5)')
plt.ylabel('Queue length(packets)')
picName = "plot" + tm.strftime("%Y%m%d-%H%M%S") + '.png'
plt.savefig(os.sep.join([os.path.expanduser('~'), 'Desktop\\plots_1000mpbs', picName ]))
#plt.show()
"""


#plot library for showing on the prentation
import plotly
from plotly import __version__
from plotly.offline import download_plotlyjs,init_notebook_mode, plot, iplot
import plotly.plotly as py
import plotly.graph_objs as go
try:

    trace0 = go.Scatter(x = mon_t, y=que_len, mode = 'lines', name='queue_length')
    data = [trace0]
    layout = go.Layout(
        title='Queque Length for 1Gbps; 64bit',titlefont=dict(
                family='Helvetica,Courier New, monospace',
                size=36,
                color='#C71585'
            ),
        xaxis=dict(
            title='Time in microsecond',
            titlefont=dict(
                family='Helvetica,Courier New, monospace',
                size=36,
                color='#C71585'
            )
        ),
        yaxis=dict(
            title='Packets',
            titlefont=dict(
                family='Helvetica,Courier New, monospace',
                size=36,
                color='#C71585'
                
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig)
except: 
    print('could not do that')

