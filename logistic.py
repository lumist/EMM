# -*- coding: utf-8 -*-
from numpy import *
from pylab import *
import os

mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体

year =arange(2003,2016)
pop = [129227,129988,130756,131448,132129,132802,133450,134091,134735,135404,136072,136782,137462]
famale = [66556,66976,67375,67728,68048,68357,68647,68748,69068,69395,69728,70079,70414]
male = [62671,63012,63381,63720,64081,64445,64803,65343,65667,66009,66344,66703,67048]
city = [52376,54283,56212,58288,60633,62403,64512,66978,69079,71182,73111,74916,77116]
village = [76851,75705,74544,73160,71496,70399,68938,67113,65656,64222,62961,61866,60346]
birth = [12.41,12.29,12.4,12.09,12.1,12.14,11.95,11.9,11.93,12.1,12.08,12.37,12.07]
death = [6.4,6.42,6.51,6.81,6.93,7.06,7.08,7.11,7.14,7.15,7.16,7.16,7.11]
nbirth = [6.01,5.87,5.89,5.28,5.17,5.08,4.87,4.79,4.79,4.95,4.92,5.21,4.96]

#拟合2030
def logistic(x0,start,end,s2,e2):	
	#plot
	figure(figsize=(12,8))
	grid()
	title(u'年末总人口数预测对比')
	ylabel(u'年末总人口(万人)')
	xlabel(u'自然年')
	
	len_y = int(len(year)/2) #3 interval x0 x1 x2
	x = [pop[0],pop[len_y],pop[2*len_y]]
	print("pop is",x)
	r = log((1/x[0]-1/x[1])/(1/x[1]-1/x[2]))/len_y
	print("r=%f"%r)
	N = (1-exp(-r*len_y))/(1/x[1]-exp(-r*len_y)/x[0])
	print("N=%f"%N)
	pop2 = []
	for y in range(start,end):
		pop2.append( N/(1+(N/x[0]-1)*exp(-r*(y-year[0])))  )
		if y == year[0]:
			text( y, pop2[0]+850,
								"0.0000%%",
								size=10,
								ha="center", va="center")
		elif y>year[0] and y<year[-1]:
			text( y, pop2[y-year[0]]+850,
								"%.4f%%"%abs((pop2[y-year[0]]-pop[y-2003])*100/pop[y-2003]),
								size=10,
								ha="center", va="center"
							)
	print(pop2)
	
	#有孩预测
	x0=138271
	r = 0.0237
	N = 183582
	pop3 = []
	for y in range(s2,e2):
		pop3.append( N/(1+(N/x0-1)*exp(-r*(y-s2)))  )
	print(pop3)
	
	plot(year,pop, color="red" , marker="o" , linestyle="-", label="Reality")
	plot(range(start,end),pop2, color="blue" , marker="." , linestyle="--", label="Logistic")
	plot(range(s2,e2),pop3, color="pink" , marker="x" , linestyle="--", label="Logistic2")
	legend(loc="upper left")
	#plot(year,pop)
	#plot(year,pop2)
	show()	

#2016预测2030
def logistic2(start,end):	
	#plot
	figure(figsize=(12,8))
	grid()
	title(u'年末总人口数预测对比')
	ylabel(u'年末总人口(万人)')
	xlabel(u'自然年')
	
	x0=138271
	r = 0.02370521331393650651110279060339
	N = 183582
	pop2 = []
	for y in range(start,end):
		pop2.append( N/(1+(N/x0-1)*exp(-r*(y-start)))  )
	print(pop2)
	plot(range(start,end),pop2, color="red" , marker="x" , linestyle="-", label="Logistic")
	legend(loc="upper left")
	#plot(year,pop)
	#plot(year,pop2)
	show()	

logistic(pop[0],year[0],2031,2016,2031)
