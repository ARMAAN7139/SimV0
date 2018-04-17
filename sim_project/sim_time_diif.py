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
        yield env.timeout(0.000005)#wait 10micorsecond between sampling
# method to calculate expected gap. 
def expected_Gap(): 
    st = 1500  #size of the trailing packet. 
    li = 100 #link rate respectivley
    sh = 64  #size of the heading packet
    delta = abs((st/li) - (sh/li))  # dispercsiom gap calculation
    EG = abs((st/li) + delta)  #expected gap calculation. take absolute value of it
    print("eg is : "+ str( EG))
    return EG

#mthod ot calculate measured gap.
def measured_Gap(EG, tqh, tqt): 
    MG = abs(EG - (tqh - tqt))
    return MG


#method to compare the result. 
def compare_result(EG, MG):
    data = []
    if EG > MG: 
        data.append()



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
    #out_rate = int(input('Enter the output link rate in Mbps: '))
    out_rate = 100

    pkt_Size = int(input('Eneter the packet size in bytes: '))
    #pkt_Size = 64
    link_speed = int(input('Enter the input link rate in Mbps: '))
    #link_speed = 100
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
    flow1 = float(input('flow 1 rate in mbps: '))
    #flow1 = np.random.uniform(20.6, 30.8)
    flow1_rate = calc_rate(flow1,pkt_Size)
    flow2 = float(input('flow 2 rate in mbps: '))
    #flow2 = np.random.uniform(1.0,20.3 )
   
    flow2_rate = calc_rate(flow2,pkt_Size)
    flow3 = float(input('flow 3 rate in mbps: '))
    #flow3 = np.random.uniform(10.1, 25.5 )
    flow3_rate = calc_rate(flow3,pkt_Size)
    flow4 = float(input('flow 4 rate in mbps: '))
    #flow4 = np.random.uniform(1.1, 20.5)
    flow4_rate = calc_rate(flow4,pkt_Size)
    """
    #put rates in ascending order. 
    flows = [flow1_rate, flow2_rate, flow3_rate]
    asc_order = sorted(flows)
    sml_rate = asc_order[0]
    med_rate = asc_order[1]
    lrg_rate = asc_order[2]
    """
    print(flow1_rate, flow2_rate, flow3_rate)
    t_flow = flow1 + flow2 + flow3 + flow4
    if t_flow > out_rate:# the total flow can not exceed  output link 
        
        print('Total flow can not be more than {}mbps input link'.format(out_rate))
        sys.exit()

    """
    with open("C:\\Users\\Joykill\\Desktop\\sim_project\\usrinpt_100mpbs.txt", "a+") as f: 
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
        self.adist = adist #flow rate   
        self.sdist = sdist  # size of the packet
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
    def __init__(self, env, out_rate, rec_arrivals=False, absolute_arrivals=False, rec_departure=False, absolute_departure=False, rec_waits=True, debug=False, selector=None):
        self.res = simpy.Resource(env, capacity=1)
        self.env = env
        self.rec_waits = rec_waits
        self.rec_arrivals = rec_arrivals
        self.rec_departure = rec_departure
        self.absolute_arrivals = absolute_arrivals
        self.absolute_departure = absolute_departure
        self.waits_ph = []
        self.waits_pt = []
        self.arrivals = []
        self.departure = []
        self.debug = debug
        self.packets_rec = 0
        self.bytes_rec = 0
        self.selector = selector
        self.last_arrival = 0.0
        self.last_departure = 0.0
        self.out_rate = out_rate
        self.time_delay = 0.0

    def put(self, pkt):
        if not self.selector or self.selector(pkt):
            tqh = 0.0
            tqt = 0.0
            #record time delay
            now = self.env.now 
            if self.rec_waits:
                if pkt.src == "ph":
                    tqh = self.env.now - pkt.time
                    self.waits_ph.append(self.env.now - pkt.time)
                elif pkt.src == "pt":
                    tqt = self.env.now - pkt.time
                    self.waits_pt.append(self.env.now - pkt.time)
            EG = expected_Gap()
            measured_Gap(EG,tqh, tqt)
                    
            #record arrival time.
            if self.rec_arrivals:
                if self.absolute_arrivals:
                    if pkt.src == "ph" or  pkt.src == "pt":
                        self.arrivals.append(now)
                    else:
                        self.arrivals.append(now - self.last_arrival)
                    self.last_arrival = now
            self.packets_rec += 1
            self.bytes_rec += pkt.size

            #call resrouce(router)
            env.process(call_res(self.res,self.env,pkt.src,self.out_rate))

            #record departure time.
            if self.rec_departure: 
                if self.absolute_departure:
                    if pkt.src == "ph" or  pkt.src == "pt":
                        self.departure.append(now)
                    else: 
                        self.departure.append(now - self.last_departure)
                    self.last_departure = now
            
            #print the packet if debug is set to true. 
            if self.debug:
                print(pkt)
        
#tmp var time = int(input('Enter time in Micro seconds, how long you want to run the simulation for: ')) 
time = 0.001
microsec_time = time / 10**6  # put this in run variables. 
env = simpy.Environment()
#res = simpy.Resource(env,capacity=1)
pram = cross_traffic_gen(env )# store it in param tuple. 
print(pram)
# packet generator takes environmetn, label, link rate, packet size, initial delay( defaulted to 0 )
p0  = PacketGenerator(env,'flow1',pram[2],pram[5])
p1  = PacketGenerator(env,'flow2',pram[3],pram[5])
p2  = PacketGenerator(env,'flow3',pram[4],pram[5])
p3  = PacketGenerator(env,'flow4',pram[6],pram[5])

#Probing packets with no Intraprobe gap. 
ph  = PacketGenerator(env,'ph',0.00000512, 64 )
pt  = PacketGenerator(env, 'pt',0.00012, 1500)


ps  = PacketSink(env,pram[1],debug=True)
p0.out = ps 
p1.out = ps 
p2.out = ps
p3.out = ps
ph.out = ps
pt.out = ps
env.process(monitor(env, ps.res, ps.time_delay))
env.run(until = time)

#draw the plot
plt.figure()
plt.plot(mon_t,que_len)
plt.xlabel('time (\u00B5)')
plt.ylabel('Queue length(packets)')
#picName = "plot" + tm.strftime("%Y%m%d-%H%M%S") + '.png'
#plt.savefig(os.sep.join([os.path.expanduser('~'), 'Desktop\\plots_100mpbs', picName ]))
plt.show()
print(ps.waits_ph)
print("*****************************pt***************************************")
print(ps.waits_pt)