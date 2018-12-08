#!/usr/bin/python
# -*- coding:utf8 -*-

import getopt
import sys

__author__="xiazhanfeng"

'''
针对有序网络进行递归获得整个网络结构并输出成文件，也可查询任意节点所在网络集合
'''


def usage():
	print("Usage:%s -i 输入关系网络文件(netfile) -o 输出网络code和对应连线(output) -c 任意一个节点包含的网络路径(code) -h 帮助说明" %(sys.argv[0]))


if len(sys.argv)<2:
	usage()
	sys.exit()

opts, args = getopt.getopt(sys.argv[1:], "i:o:h")
input_file = ""
output_file = ""
for op, value in opts:
	if op == "-i":
		input_file = value
	elif op == "-o":
		output_file = value
	elif op == "-c":
		code = value
	elif op in ("-h","-help"):
		usage()
		sys.exit()


class net_analysis():
	
	def __init__(self):
		#值初始化
		self.init_dict={}
		#首先确认是否有根，有方向肯定有根
		self.root=set()
		self.association=set()
		self.code_dict={}
		
		
	def read_net(self,infile):
		#确定起始根点
		#存取初始化字典
		#A1 B1
		#A2 B2
		#A1 C1
		#B2 D2
		with open(infile,"r") as net_in:
			#for net_line in 
			info=net_in.readlines()
			for net_liner in info:
				net_liner=net_liner.strip("\n")
				net_liners=net_liner.split(sep="\t")
				self.root.add(net_liners[0])
			for net_line in info:
				net_line=net_line.strip("\n")
				net_lines=net_line.split(sep="\t")
				if net_lines[1] in self.root:
					self.root.remove(net_lines[1])
				if self.init_dict.get(net_lines[0]):
					self.init_dict[net_lines[0]].add(net_lines[1])
				else:
					self.init_dict[net_lines[0]]=set()
					self.init_dict[net_lines[0]].add(net_lines[1])
					
					
	def recursion_net(self):
		#进行递归循环遍历得到线路图
		#for k,v in self.net_dict.items():
		for r in self.root:
			string=""
			f=set()
			f.add(r)
			self.node=r
			#self.node="R-BTA-8953854"
			#f.add("R-BTA-8953854")
			#self.association[self.node]=""
			recur_dict=self.recursion(f)
			#for i1,t1 in recur_dict.items():
			#	print(i1+"###")
			#	for i2,t2 in t1.items():
			#		print(i2+"&&")
			#		if t2!=1:
			#			for i3,t3 in t2.items():
			#				print(i3+"**")
			self.read_recursion(recur_dict,string)
			#for i in self.association:
			#	print(i+"%%%")
			#sys.exit()
			#self.association[r]=strings

			
	def read_recursion(self,circle_dict,string):
		#association=set()
		for i,k in circle_dict.items():
			index=string
			h=i
			n=k
			if n==1:
				self.association.add(index+"\t"+i)
			else:
				index=index+"\t"+h
				self.read_recursion(n,index)
		#return association

		
	def recursion(self,node):
		dicts={}
		for k in node:
			if self.init_dict.get(k):
				#self.association[self.node]=self.association[self.node]+"\t"+k
				dicts[k]=self.recursion(self.init_dict[k])
			else:
				dicts[k]=1
		return dicts

	
	def save_dict(self):
		for ele in self.association:
			ele=ele.strip("\t")
			ele=ele.strip("\n")
			eles=ele.split(sep="\t")
			for element in eles:
				if self.code_dict.get(element):
					self.code_dict[element].add(ele)
				else:
					self.code_dict[element]=set()
					self.code_dict[element].add(ele)
				
	
	def net_ouput(self,outfile):
		with open(outfile,"w") as out:
			for i in self.association:
				out.write(i+"\n")

if __name__ == "__main__" :
	net=net_analysis()
	net.read_net(input_file)
	net.recursion_net()
	#for i,l in net.association.items():
	#	print(i+"\t"+l
	net.net_ouput(output_file)
	net.save_dict()
	if code:
		for k,v in net.code_dict.items():
			if k==code:
				for e in v:
					print(e)

	
