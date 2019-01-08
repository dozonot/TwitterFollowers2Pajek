#!/usr/bin/env python
user_dict = {}
arcs_dict = {}

with open("friendships.net", mode='r') as r:
    with open("friendships-arc.txt", mode='w') as w:
        r.readline() # *Vertics行を読み飛ばす
        while True:
            l = r.readline()
            if '*Arcs' in l:
                break
            else:
                vertex = l.split(' ')
                user_dict[vertex[0]] = vertex[1][1:-2]
        index = 1
        while True:
            l = r.readline()
            if not l:
                break
            else:
                arc = l.split(' ')
                src  = user_dict.get(arc[0])
                dst = user_dict.get(arc[1][0:-1])
                w.write("index={}, arc, src={}, dst={}\n".format( index, src, dst ))
                index += 1
print("friendships-arc.txt file created")
