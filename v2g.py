import re
import networkx as nx
import matplotlib.pyplot as plt
import math
import easygui

verilog_file_name=easygui.fileopenbox()

f = open(verilog_file_name, "r")
en=False
variables=[]
variables2=[]
matches = ["input", "output","wire","reg"]
body=[]
modules=[]

for line in f:
    if "module" in line:
        if "endmodule" not in line:
            modules.append((line.split(" "))[1])

reply   = easygui.choicebox("Select the Module", "Select", modules)

f = open(verilog_file_name, "r")

module_name="module "+reply

for x in f:
    if x[0:1]!="//":
        if module_name in x:
            en=True
        if en:
            if any(y in x for y in matches):
                temp=(x.split("//")[0]).split( )
                if '];'in x:
                    strt=x.split("[")[-2]
                    ptr=strt.index("]")
                    strt=strt[ptr+1:].replace(" ", '')
                    # print(strt)
                    variables.append(strt)
                else: variables.append(str([re.split(',',(a.split(";")[0])) for a in temp if ";" in a])[2:-2])
            else: body.append(x)
            if "endmodule" in x:
                break
for m in variables:
    variables2.extend((m.replace("'", '')).split(","))
print((variables2))
variables2 = [i for i in variables2 if i] 

edges_set=[]

# for x in variables2:
#     for y in body:
#         if x in y:
#             if "assign" in y:
#                 temp1=y.replace("assign", '')
#                 edges_set.append(set(temp1.split("=")))
#                 print(temp1.split("="))
#             elif "<=" in y:
#                 temp2=y.split(";")[0]
#                 edges_set.append(set(temp2.split("<=")))
#                 print(temp2.split("<="))
#             elif "==" in y:
#                 pass
#             elif "." in y:
#                 temp3=y.replace(".", '')
#                 temp3=temp3.replace(" ", '')
#                 temp3=temp3.replace(")", '')
#                 if ":" in temp3:
#                     temp3=temp3.split("[")[0]
#                 else: temp3=temp3.split(";")[0]
#                 # temp3=temp3.replace("", '')
#                 edges_set.append(set(temp3.split("(")))
#                 print(temp3.split("("))
#             # edges_set.append(set([x,y]))
#             # print (y)
for x in variables2:
    for y in variables2:
        if (x!=y):
            for m in body:
                if x in m:
                    if y in m:
                        print(x,y)
                        edges_set.append(set([x,y]))


# print (edges_set)

G=nx.Graph()
G.add_nodes_from(variables2)
G.add_edges_from(edges_set)

pos=nx.spring_layout(G,0.6)
print(G.degree())
print(G.nodes())
print(G.edges())

# print(type(G.nodes()))
# print(type(G.edges()))

nx.draw(G,pos,with_labels=True)
# plt.savefig("graphs/"+verilog_module_name+".png") # save as png
plt.show()
