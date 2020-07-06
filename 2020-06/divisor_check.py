#from sympy.ntheory import divisor_sigma # too slow for this purpose
import pandas as pd

def divisor_sum_factor(p, r):
    dsum = 0
    for i in range(0, r+1):
        dsum += p**i
    return dsum

def divisor_sigma_special(factor_string, number):
    ds = 1
    parts = factor_string.split('|')
    for part in parts:
        ps = part.split('^')
        p  = int(ps[0])
        r  = int(ps[1])
        ds *= divisor_sum_factor(p, r)
    return ds-number

dist = 10**100
df = pd.read_csv('merged.txt')
print('data read')
counter = 0
too_high = 0
too_low = 0
th = {i:0 for i in range(1,20)}
tl = {i:0 for i in range(1,20)}
for index, row in df.iterrows():
    counter += 1
    ds = divisor_sigma_special(row['factors'], int(row['number']))
    # check 1
    difference = abs(12142680281284711468101282998309016699980172-ds)
    if abs(12142680281284711468101282998309016699980172-ds) < dist:
        dist = difference
        print(row['number'])
        print(ds)
        print('dsdiff: '+str(difference))
    if 12142680281284711468101282998309016699980172-ds < 0:
        too_high+=1
        for i in range(1,20):
            if '|2^'+str(i)+'|' in row['factors']:
                th[i] += 1
    else:
        too_low+=1
        for i in range(1,20):
            if '|2^'+str(i)+'|' in row['factors']:
                tl[i] += 1
    # check 2
    # if int(row['number'])%12 == 0 and ds%12 != 0:
    #     print(str(row['number'])+' exception! ')
    # if int(row['number'])%12 != 0 and ds%12 == 0:
    #     print(str(row['number'])+' exception! ')
    # if counter%10000==0:
    #     print(str(counter)+' numbers tested')
print(too_high)
print(too_low)
print(th)
print(tl)