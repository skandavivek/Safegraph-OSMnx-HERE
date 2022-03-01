import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict
import json
import pickle
#import osmnx as ox
import networkx as nx




def trips_OD(G,OD_in,name):
    routes_raw = []
    tt = []
    length = []
    d = defaultdict(int)
    len_edges = np.zeros(len(OD_in))
    trips = []

    for i in range(0, len(OD_in)):
        if nx.has_path(G,OD_in['ID_osm_start'][i],OD_in['ID_osm_end'][i]):
            a1=nx.shortest_path(G,source=OD_in['ID_osm_start'][i],target=OD_in['ID_osm_end'][i], weight='travel_time')
            tt.append(nx.shortest_path_length(G,source=OD_in['ID_osm_start'][i],target=OD_in['ID_osm_end'][i], weight='travel_time'))
            length.append(nx.shortest_path_length(G,source=OD_in['ID_osm_start'][i],target=OD_in['ID_osm_end'][i], weight='length'))
            routes_raw.append(a1)
            len_edges[i]=len(a1)
            #default dict for future finding nodes and relative importance
            trips.append(int(OD_in['trips'][i]))
            for j in range(len(a1)):
                d[a1[j]]+=int(OD_in['trips'][i])
            print(i)


    with open('routes_raw_tt_io'+name+'.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(routes_raw, filehandle)

    with open('tt_io'+name+'.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(tt, filehandle)


    with open('length_io'+name+'.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(length, filehandle)

    routes=np.zeros((len(d),2))
    routes[:,0]=np.array(list(d.keys()))
    routes[:,1]=np.array(list(d.values()))
    np.savetxt('routes_tt_io2'+name+'.txt',routes)

    trips2=np.array(trips)
    np.savetxt('trips_tt_io2'+name+'.txt',trips2)



def tar(routes,routes_raw,name):
    tar = []
    for i in range(0, len(routes)):
        # imp=0
        # temp2=[]
        d = defaultdict(int)
        for j in range(0, len(routes_raw)):

            if (len(set(tar).intersection(routes_raw[j])) == 0):  # if the route is still not blocked
                # temp2.append(routes_raw[j])
                for rr in routes_raw[j]:
                    d[rr] += 1
        r = np.zeros((len(d), 2))
        r[:, 0] = np.array(list(d.keys()))
        r[:, 1] = np.array(list(d.values()))
        # imp=r[np.argsort(-1*r[:,1]),0][0]
        print(i)
        try:
            # tar.append(dfd)
            tar.append(r[np.argsort(-1 * r[:, 1]), 0][0])
        except:
            break

    np.savetxt('tar'+name, np.array(tar))


def removal_perc(routes,routes_raw,trips,name):
    c = np.zeros([len(routes), len(routes_raw)])

    tar = []
    for i in range(0, len(routes)):
        # imp=0
        # temp2=[]
        d = defaultdict(int)
        for j in range(0, len(routes_raw)):

            if (len(set(routes[i:i + 1, 0]).intersection(routes_raw[j])) != 0):  # if route is blocked

                # if(np.in1d(routes[:i,0],routes_raw[j]).any()==True): #if route is blocked
                c[i, j] = 1  # might need to do a cumsum over this...

        print(i)

    #return (c)

    c_sum = np.cumsum(c, axis=0)
    c_sum[c_sum >= 1] = 1

    c_sum_trips = c_sum * trips
    c_sum_trips_frac = np.sum(c_sum_trips, axis=1) / np.sum(trips)
    np.savetxt('c_sum_trips_frac'+name+'.txt', c_sum_trips_frac)

def perc(nodes_dis,G,OD_in,name):

#nodes_dis=routes[np.argsort(-1*routes[:,1]),0]
#nodes_dis_r=nodes_dis.copy()
    p=np.zeros(len(nodes_dis))
    G2=G.copy()
    for i in range(0, len(nodes_dis)):
        G2=G.copy()
        #random.shuffle(nodes_dis_r)
        G2.remove_nodes_from(list(nodes_dis[0:i]))
        OD_in_s=OD_in.sample(n=1000,weights=OD_in['trips'])
        OD_in_s=OD_in_s.reset_index(drop=True)
        OD_in_s.columns
        for j in range(0, len(OD_in_s)):
            if(G2.has_node(OD_in_s['ID_osm_start'][j]) & G2.has_node(OD_in_s['ID_osm_end'][j])):
                #is there still a path after removing nodes?
                p[i]+=nx.has_path(G2,OD_in_s['ID_osm_start'][j],OD_in_s['ID_osm_end'][j])*1
        print(i,p[i])
    np.savetxt('p_tt_sub1000'+name+'.txt',p)


