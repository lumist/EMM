# -*- coding: utf-8 -*-
from numpy import *
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import xlrd
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
kgdp = [10666,12487,14368,16738,20505,24121,26222,30876,36403,40007,43852,47203,50251] #个人GDP
#自然增长拟合 2次曲线效果不好 无法抑制之后的生长率
def nbirthfit():
	nnbirth = nbirth
	nnbirth.append(5.86)
	nyear = arange(2003,2017)
	coffient = polyfit(nyear,nnbirth,2)
	line = polyval(coffient,arange(2003,2030))
	plot(nyear,nnbirth,color='red',linestyle='-')
	plot(arange(2003,2030),line,color='blue',linestyle='--')
	show()

#出生生存模型
def B(t):
	return 1.06
	#return 1+exp(-(t-100)**2/2500)
def l(t,a):
	par = a*(1-0.3/(1+20*exp(-0.05*t)))
	#print(par)
	if par>=70:
		return 0
	else:
		return exp(6/245-120/((70-par)**2))
def POP():
	T = arange(0,30,0.1) #2003-2203年
	A = arange(0,100,0.1) #0-100岁
	Z = []
	
	for a in A:
		Z.append([])
		for t in T:
			Z[-1].append(B(t-a)*l(t-a,a))
	T, A = meshgrid(T, A)
	fig = figure()
	ax = fig.gca(projection='3d')
	surf = ax.plot_surface(T, A, Z)
	show()

def Solow():
	#好TM长全是算L(t)
	fn = ['男年龄.xls','女年龄.xls']
	P_male = zeros((7,100))#03-09 7年 100个年龄
	P_famale =zeros((7,100))
	P_mt = arange(7)
	P_ft = arange(7)
	for fname in fn:
		bk = xlrd.open_workbook(fname)
		for name in bk.sheet_names():
			cbk = bk.sheet_by_name(name)
			row = cbk.nrows
			col = cbk.ncols
			col = 7+1#03-09 7年的数据
			for i in range(2,row):
				for j in range(1,col):
					if fname == fn[0]:
						for k in range(5):
							P_famale[j-1][(i-2)*5+k] = cbk.cell_value(i,j)/5  #i-2 这是自训练数据
					else:
						for k in range(5):
							P_male[j-1][(i-2)*5+k] = cbk.cell_value(i,j)/5  #i-2 这是自训练数据
	#print(P_male)
	#print(P_famale)
	for i in range(7):
		P_mt[i] = sum(P_male[i])
		P_ft[i] = sum(P_famale[i])
	for i in range(7):
		for j in range(100):
			P_male[i][j] /= P_mt[i] #i-2 这是自训练数据
			P_male[i][j] *= male[i]
			P_famale[i][j] /= P_ft[i]  #i-2 这是自训练数据
			P_famale[i][j] *= famale[i]
	
	#估计参数
	KE = []
	lE = []
	PE = []
	r = 0.35/100#折现
	s = 0.52#储蓄
	sE = [0.339397,0.337943376,0.353834038,0.371697853,0.392448724,0.399383547,0.403843769]
	for i in range(7):
		PE.append( pop[i] )
		KE.append( kgdp[i] )
		lE.append( (sum(P_famale[i][16:60])+sum(P_male[i][16:55]))/pop[i] )#l=L/P
	print(PE)
	C3 = lE[0]/lE[5]
	C1 = (KE[1]*PE[1]/PE[0]-(1-r)*KE[0])/(KE[6]*PE[6]/PE[5]-(1-r)*KE[5])/C3
	C2 = KE[0]/KE[5]/C3
	alpha = log(C1)/log(C2)
	print(alpha)
	A = ( KE[1]*PE[1]/PE[0]-(1-r)*KE[0] ) / ( s*(KE[0]**alpha)*(lE[0]**(1-alpha)) )
	print(A)
	
	#预测GDP
	K = []
	L = []
	L.append(lE[0])
	K.append(kgdp[0])
	print()
	for i in range(1,7):
		L.append( (sum(P_famale[i][16:60])+sum(P_male[i][16:55]))/pop[i] )#l=L/P
		K.append( s*A*(K[i-1]**alpha)*(L[i-1]**(1-alpha))+(1-r)*K[i-1] )
	
	#plot
	figure(figsize=(12,8))
	grid()
	title(u'年末人均国内生产总值预测对比')
	ylabel(u'年末人均国内生产总值(亿元)')
	xlabel(u'自然年')	
	plot(range(0,7),kgdp[0:7], color="red" , marker="o" , linestyle="-", label="Reality")
	plot(range(0,7),K, color="blue" , marker="." , linestyle="--", label="Solow")
	legend(loc="upper left")
	show()
	
#拟合2030
def logistic(x0,start,end,s2,e2,s3,e3):	
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
	print("\nLogistic_1:\n",pop2)
	
	#二胎预测
	x0=138271
	r = 0.0237
	N = 183582
	pop3 = []
	for y in range(s2,e2):
		pop3.append( N/(1+(N/x0-1)*exp(-r*(y-s2)))  )
	print("\nLogistic_2:\n",pop3)
	
	#不开放二胎lisbel
	pop4 = [138015.0156,138449.7074,138759.286,138942.0692,139000.5561,138934.3908,138760.9317,138488.8593,138128.6298,137691.6977,137182.4257,136622.1204,136019.4663,135382.5638,134718.823,134027.604,133324.6183,132616.7533,131916.9572,131243.3975,130609.9731,130039.3426,129539.4512,129110.5028,128745.7129,128429.5092,128152.0617,127897.2617,127649.9913,127397.3134,127123.6116,126829.4967,126510.4057,126164.597,125792.7149]
	
	'''#以lisbel数据估计
	pop5= pop[0:-1]
	year5 = arange(start,e3)#2003-2050
	for i in pop4:
		pop5.append(i)
	len_y = int(len(year5)/2) #3 interval x0 x1 x2
	x = [pop5[0],pop5[len_y],pop5[2*len_y]]
	print("\nNew Estimation\npop5 is",x)
	r = log((1/x[0]-1/x[1])/(1/x[1]-1/x[2]))/len_y
	print("r=%f"%r)
	N = (1-exp(-r*len_y))/(1/x[1]-exp(-r*len_y)/x[0])
	print("N=%f"%N)
	pop6 = []
	for y in year5:
		pop6.append( N/(1+(N/x[0]-1)*exp(-r*(y-year[0])))  )
	print("\nLogistic_3:\n",pop6)'''
	
	
	
	plot(year,pop, color="red" , marker="o" , linestyle="-", label="Reality")
	plot(range(start,end),pop2, color="blue" , marker="." , linestyle="--", label="Logistic")
	plot(range(s2,e2),pop3, color="pink" , marker="x" , linestyle="--", label="Logistic2")
	plot(range(s3,e3),pop4, color="purple" , marker="x" , linestyle="--", label="leslie")
	#plot(range(start,e3),pop6,color="green" , marker="x" , linestyle="--", label="Logistic3")
	legend(loc="upper left")
	#plot(year,pop)
	#plot(year,pop2)
	show()	


#logistic(pop[0],year[0],2051,2016,2051,2015,2050)
Solow()
#nbirthfit()