import sys
import re
from datetime import *
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt

Flow = namedtuple( 'Flow', ['start_datetime', 'duration', 'protocol', 'src_ip', 'src_port', 'dst_ip', 'dst_port', 'num_packets', 'num_bytes', 'num_flows'] )

with open(sys.argv[1], 'r') as f:
    flow_lines = f.readlines()

flows = list()
#                          date time       duration   proto    src_ip  src_port         dst_ip dst_port n_pkts n_bytes  n_flows
flow_re = re.compile('([\d-]* [\d:\.]*)\s*([\d\.]*)\s*(\S*)\s*([\d\.]*)\:(\d*)\s*->\s*([\d\.]*)\:(\d*)\s*(\d*)\s*(\d*)\s*(\d*)')

def parse_flow(flow_str):
    match = flow_re.match(flow_str)
    try:
        groups = match.groups()
        #print groups
        return Flow(datetime.strptime(groups[0], '%Y-%m-%d %H:%M:%S.%f'),  # start_datetime
                    timedelta(seconds=float(groups[1])),                   # duration
                    groups[2],                                             # protocol
                    groups[3],                                             # src_ip
                    int(groups[4]),                                        # src_port
                    groups[5],                                             # dst_ip
                    int(groups[6]),                                        # dst_port
                    int(groups[7]),                                        # num_packets
                    int(groups[8]),                                        # num_bytes
                    int(groups[9]) )                                       # num_flows
    except Exception:
        return None

for line in flow_lines:
    parsed = parse_flow(line)
    if parsed:
        flows.append(parsed)

for f in flows[0:10]:
    print f


G = nx.Graph()
i = 0
for f in flows:
  G.add_edge(f[3],f[5])

  print i, "of", len(flows)
  i+=1

position = nx.spring_layout(G)

localnodes =  [n for n in G if ("192.168" in n)]  
remotenodes = [n for n in G if ("192.168" not in n)]

nx.draw_networkx_nodes(G, position, nodelist = localnodes, node_color="g", node_size=10, draw_labels=True)
nx.draw_networkx_nodes(G, position, nodelist = remotenodes, node_color="r", node_size = 8)

nx.draw_networkx_edges(G, position)

plt.show()
