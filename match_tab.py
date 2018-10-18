#!/usr/bin/python3
# -*- coding:utf8 -*-

__author__="xiazhanfeng"

'''
提取miRNA所有表达量和在相应差异分析结果中的log2Ratio以及分组后的表达量值
'''


import sys
import os
import re

#class

if len(sys.argv)<4:
	print("python"+sys.argv[0]+"merge_tpm<>	DiffExp<>	choose<>	ouput<>")
	sys.exit()


'''
argv第一个参数是程序名
'''
(py,merge,diff,output)=sys.argv
	
'''
存取数据为set格式
'''
def read_inset(*argv):
	miRNA=set()
	with open(argv[0],'r') as f:
		flag=argv[2]
		'''
		tuple不能直接进行赋值，可以进行id转换后再进行赋值判断
		'''
		for line in f.readlines():
			if flag==1:
				continue
				flag=0
			lines=line.split(sep="\t")
			if isinstance(argv[1],int):
				miRNA.append(lines[col])
			else:
				raise ValueError("non int for column")
		return miRNA
'''
col may be a set 不考虑key一致的列进行存储dict，会直接产生覆盖
递归实现多维字典
'''
def trans_key(tup,dicts,value=1):
	#pass
	index=0
	if index<len(tup)-1:
		dd=trans_key(tup,dicts)
		dicts[tup[index]]=dd
	else:
		dicts[tup[index]]=value
'''
存取数据为多维字典,如果两列key一样会进行一个覆盖
'''
def read_indict(*argv,**wkargv):
	miRNA_dict={}
	hh=''
	with open (argv[0],'r') as df:
		flag_dict=argv[3]
		for ll in df.readlines():
			ll=ll.strip('\n')
			if flag_dict==1:
				#print(type(argv[3]))
				flag_dict=0
				hh=ll
				continue
			llines=ll.split(sep="\t")
			if isinstance(argv[1],tuple):
				if argv[2]=='all':
					trans_key(llines[argv[1]-1],miRNA_dict,llines)
				elif isinstance(argv[2],int):
					trans_key(llines[argv[1]-1],miRNA_dict,llines[argv[2]-1])
				elif isinstance(argv[2],tuple):
					trans_key(llines[argv[1]-1],miRNA_dict,[llines[i-1] for i in argv[2]])
			elif isinstance(argv[1],int):
				if argv[2]=='all':
					miRNA_dict[llines[argv[1]-1]]=llines
				elif isinstance(argv[2],int):
					miRNA_dict[llines[argv[1]-1]]=llines[argv[2]-1]
				elif isinstance(argv[2],tuple):
					miRNA_dict[llines[argv[1]-1]]=[llines[i-1] for i in argv[2]]
			else:
				raise ValueError("non int for column")

		return (hh,miRNA_dict)


def read_table(filename,filetype,col,value,header):
	if filetype == 'set':
		return read_inset(filename,col,header)
	elif filetype == 'dict':
		return read_indict(filename,col,header,value)



def add_header(line):
	st=''
	for lines in line:
		lst=lines.split("-vs-")
		lst.append('')
		st+='_Expression\t'.join(lst)
		st+=lines+'_log2Ratio\t'
	st.strip()
	return st

if __name__=='__main__':
	merge_dict={}
	mhead,merge_dict=read_table(merge,'dict',1,1,'all')
	diff_dict={}
	klist=[]
	if os.path.isdir(sys.argv[2]):
		for files in os.listdir(sys.argv[2]):
			dirname=os.path.dirname(sys.argv[2])
			filename=os.path.join(sys.argv[2],files)
			m=re.search(r'(.*?)_DEGseq\.diffexp\.xls',files)
			if m:
				dhead,diff_dict_value=read_table(filename,'dict',1,1,(4,5,6))
				diff_dict[m.groups()[0]]=diff_dict_value
				klist.append(m.groups()[0])
	for l in klist:
		print(l)
	with open(output,'w') as o:
		strs=add_header(klist)
		o.write(mhead+'\t'+strs+"\n")
		for k,v in merge_dict.items():
			o.write('\t'.join(merge_dict[k]))
			for k1 in klist:
				if k in diff_dict[k1]:
					o.write('\t'+'\t'.join(diff_dict[k1][k]))
				else:
					o.write('\tNA\tNA\tNA')
			o.write('\n')
'''
	diff_dict=read_table(diff,'dict',1,6,1,dicts)
if os.path.isfile(sys.argv[3]):
	with open(choose,'r') as c:
		for ls in c.readlines():
			ls=ls.strip()
			lss=ls.split(sep="\t")
			if re.search("sRNA id",ls):
				continue
			else:
				if lss[0] in merge_dict:
					if not lss[0] in diff_dict:
						diff_dict[lss[0]]='NA'
				#with open(output,'w') as o:
					#o.write(merge_dict[lss[0]]+"\t"+diff_dict[lss[0]]+"\n")
					print('%s\t%s' %('\t'.join(merge_dict[lss[0]]),diff_dict[lss[0]]))
'''
