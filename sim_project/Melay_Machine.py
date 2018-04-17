#!/usr/bin/env python
machine = [None for i in xrange(11)]#hard-code of the Mealy Machine
machine[0] = [0,0,0],[1,2,5]
machine[1] = [0,0,0],[2,3,6]
machine[2] = [0,0,0],[3,4,7]
machine[3] = [0,0,0],[4,5,8]
machine[4] = [0,0,0],[5,6,9]
machine[5] = [0,0,0],[6,7,10]
machine[6] = [0,0,1],[7,8,10]
machine[7] = [0,0,2],[8,9,10]
machine[8] = [0,0,3],[9,10,10]
machine[9] = [0,1,4],[10,10,10]
machine[10] = [1,2,5],[10,10,10]
print 'Enter the string: '
string = raw_input()
state = 0
output = 0
foo = 0
for i in string:
    print 'State:',state,'\t',
    print 'Input:',i,'\t',
    foo = int(i)
    if foo == 1:
        output = machine[state][0][0]
        state = machine[state][1][0]
    elif foo == 2:
        output = machine[state][0][1]
        state = machine[state][1][1]
    elif foo == 5:
        output = machine[state][0][2]
        state = machine[state][1][2]
    else:
        state = -1
        print '\nMachine Hanged! Aborting...'
        break
    print 'Output:',output
print 'Last state:',state
