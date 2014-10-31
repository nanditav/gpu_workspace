#!/usr/bin/python

import re
import subprocess
import argparse

def get_avg_power(f_str,f_str2): #encoding: -8
	match1 = re.findall('gpu_sim_cycle\s*=\s*(\d*)',f_str)
	if not match1:
		return("X");
	match2 = re.findall(encode["DRAM Avg Power"],f_str2)
	if not match2:
		return("X");
	sum1 = 0.0;
	sum2 = 0.0;
	for each in range(len(match1)):
		if match2[each] == "-":
			continue
		sum1 += float(match1[each])*float(match2[each])
		sum2 += float(match1[each])
	return(sum1/sum2)

def get_stat_last(stat,f_str): #encoding: 0 
	match = re.findall(encode[stat],f_str)
	if not match:
		return("X");
	else:
		return(float(match[-1]))


def get_shader_data_stall_rate(f_str): #encoding: -1
	match = re.findall('W0_Scoreboard:(\d*)',f_str)
	if not match:
		return("X")
	else:
		match2 = re.findall('Number of Issue cycles:(\d*)',f_str)
		if not match2:
			return("X")
		else:
			return(float(match[-1])/float(match2[-1]))

def get_shader_pipeline_stall_rate(f_str): #encoding: -2
	match = re.findall('W0_Scoreboard:(\d*)',f_str)
	if not match:
		return("X")
	else:
		match2 = re.findall('Number of Issue cycles:(\d*)',f_str)
		if not match2:
			return("X")
		else:
			match3 = re.findall('Stall:(\d*)',f_str)
			if not match3:
				return("X")
			else:
				return((+float(match3[-1]))/float(match2[-1]))

def get_shader_idle_rate(f_str): #encoding: -3
	match = re.findall('W0_Scoreboard:(\d*)',f_str)
	if not match:
		return("X")
	else:
		match2 = re.findall('Number of Issue cycles:(\d*)',f_str)
		if not match2:
			return("X")
		else:
			match3 = re.findall('W0_Idle:(\d*)',f_str)
			if not match3:
				return("X")
			else:
				return((float(match3[-1]))/float(match2[-1]))

def get_rbl(f_str): #encoding: -4
	match = re.findall("average row locality = (\d*)/(\d*)",f_str)
	if not match:
		return("X");
	else:
		return((float(match[-1][0]) - float(match[-1][1]))/float(match[-1][0]))

def get_comp_ratio(f_str): #encoding: -5
	match = re.findall("nbytes_uncomp=(\d*) nbytes_comp=(\d*)",f_str)
	if not match:
		return("X");
	else:
		sum1 = 0
		sum2 = 0
		for each in match[-6:]:
			sum1 += int(each[0])
			sum2 += int(each[1])
		return(float(sum1)/float(sum2))

def get_power(stat, f_str): #encoding: -6
	match = re.findall(encode[stat],f_str)
	if not match:
		return("X");
	else:
		return(float(match[-1]))

def get_num_decomp(f_str): #encoding: -7
	match = re.findall("my_stat_l2_read_hit\s*=\s*(\d*)",f_str)
	if not match:
		return("X");
	match2 = re.findall("gpgpu_n_mem_read_global\s*=\s*(\d*)",f_str)
	if not match2:
		return("X");
	return(float(match[-1]) + float(match2[-1])) 


# --- standard stat lists ---------- 
stat_list_map = {}
stat_list_map["power"] = [("Cycles",0),("GPU Avg Power",-6),("DRAM Avg Power",-8),("Num Compressions",0),("Num Decompressions",-7)]
stat_list_map["ipc"] = [("IPC",0),("Insts",0)]
stat_list_map["shader_stalls"] = [("Shader Data Stall Rate",-1),("Shader Pipeline Stall Rate",-2),("Shader Idle Rate",-3),("Memory Pipeline Stalls",0),("ALU Pipeline Stalls",0),("ALU SFU Pipeline Stalls",0)]
stat_list_map["rbl"] = [("Row Buffer Locality",-4)]
stat_list_map["comp_ratio"] = [("Compression Ratio",-5),("IPC",0)]

# ----stat encodings --------
encode = {}
encode["IPC"] = "gpu_tot_ipc\s*=\s*(\d*.\d*)"
encode["Cycles"] = "gpu_tot_sim_cycle\s*=\s*(\d*)"
encode["Insts"] = "gpu_tot_sim_insn\s*=\s*(\d*.\d*)"
encode["ALU Pipeline Stalls"] = "Number of alu pipeline stall cycles:(\d*)"
encode["ALU SFU Pipeline Stalls"] = "Number of alu_sfu pipeline stall cycles:(\d*)"
encode["Memory Pipeline Stalls"] = "Number of memory pipeline stall cycles:(\d*)"
encode["GPU Avg Power"] = "gpu_tot_avg_power\s*=\s*(\d*.\d*)"
encode["Num Compressions"] = "gpgpu_n_mem_write_global\s*=\s*(\d*)"
encode["DRAM Avg Power"] = "gpu_avg_DRAMP,\s*=\s*(\d*.\d*)"

parser = argparse.ArgumentParser(description="Gets gpgpusim statistics");
parser.add_argument('-result_dir',dest='result_dir',required=True);
parser.add_argument('-f_out',dest='file_out',required=True);
parser.add_argument('-merge',dest='merge',required=False,type=int,default=0);
args = parser.parse_args()
cmd = subprocess.Popen('ls ' + args.result_dir + '/',shell=True, stdout=subprocess.PIPE)
config_list = []
suite_list = []
stats = []



stats = stat_list_map["power"]
for each in cmd.stdout.readlines():
	match = re.search('(.*?)\n',each)
	if match:
		config_list += [ match.group(1)]
	else:
		config_list += [each]	

cmd = subprocess.Popen('ls ' + args.result_dir + '/' + config_list[0],shell=True, stdout=subprocess.PIPE)
for each in cmd.stdout.readlines():
	match = re.search('(.*?)\n',each)
	if match:
		suite_list += [ match.group(1)]
	else:
		suite_list += [each]		

#f = open(file_list[0],'rU')
#print(f.read())
fout = open(args.file_out,'w')
title = "Stats,"
for stat in stats:
	title += stat[0] + "," 
title += '\n\n\n'
fout.write(title)

config_map = {}

for config in config_list:
	stat_map = {}
	fout.write("\n\nConfig: " + config + '\n\n')
	suite_benchmark_map = {}
	for suite in suite_list:
		suite_map = {} 
		fout.write(suite + '\n')
		benchmarks = []
		cmd = subprocess.Popen('ls ' + args.result_dir + '/' + config + '/' + suite, shell=True, stdout=subprocess.PIPE)
		for each1 in cmd.stdout.readlines():
			match = re.search('(.*?)\n',each1)
			if match:
				benchmarks += [match.group(1)]
			else:
				benchmarks += [each1]
		for benchmark in benchmarks:
			data_str = benchmark + ","
			cmd = subprocess.Popen('ls ' + args.result_dir + '/' + config + '/' + suite + '/' + benchmark + '/output_*', shell=True,stdout=subprocess.PIPE)
			temp =  cmd.stdout.readlines()[0]
			file_name = re.search('(.*?)\n',temp).group(1)
			print file_name;
			f = open(file_name,'rU')
			f_str = f.read()
			for stat in stats:
				if(stat[1] == 0):
					data = get_stat_last(stat[0],f_str)
				if(stat[1] == -1):
					data = get_shader_data_stall_rate(f_str)
				if(stat[1] == -2):
					data = get_shader_pipeline_stall_rate(f_str)
				if(stat[1] == -3):
					data = get_shader_idle_rate(f_str)
				if(stat[1] == -4):
					data = get_rbl(f_str)
				if(stat[1] == -5):
					data = get_comp_ratio(f_str)
				if(stat[1] == -6):
					cmd = subprocess.Popen('ls ' + args.result_dir + '/' + config + '/' + suite + '/' + benchmark + '/gpgpusim_power_report_*', shell=True,stdout=subprocess.PIPE)
					file_name = re.search('(.*?)\n',cmd.stdout.readlines()[0]).group(1)
					f2 = open(file_name,'rU')
					f_str2 = f2.read()
					f2.close()
					data = get_power(stat[0],f_str2)
				if(stat[1] == -7):
					data = get_num_decomp(f_str)
				if(stat[1] == -8):
					cmd = subprocess.Popen('ls ' + args.result_dir + '/' + config + '/' + suite + '/' + benchmark + '/gpgpusim_power_report_*', shell=True,stdout=subprocess.PIPE)
					file_name = re.search('(.*?)\n',cmd.stdout.readlines()[0]).group(1)
					f2 = open(file_name,'rU')
					f_str2 = f2.read()
					f2.close()
					data = get_avg_power(f_str,f_str2)
				data_str += str(data) + ","
			data_str += "\n"
			fout.write(data_str)
			f.close()
			suite_map[benchmark] = data_str.split(',')[1:]
		stat_map[suite] = suite_map;
		suite_benchmark_map[suite] = benchmarks
	config_map[config] = stat_map;
fout.close()
if(args.merge):
	fout = open(args.file_out,'r')
	stat_strings = fout.readlines()
	stat_string = fout.read()
	fout.close()
	match_statlist = re.search('Stats,',stat_strings[0])
	if(match_statlist):
		stat_list = stat_strings[0].split(',')[1:-1]
	else:
		print "Couldn't find stat list"
	title_str = ","
	for config in config_list:
		title_str += config + ","
	title_str += "\n"
	fout = open(args.file_out,'w')
	index = 0
	for stat in stat_list:
		fout.write("\n\n\n" + stat + '\n\n')
		fout.write(title_str)
		for suite in suite_list:
			fout.write(suite + '\n')
			for benchmark in suite_benchmark_map[suite]:
				data_str = benchmark + ","
				for config in config_list:
					data_str += config_map[config][suite][benchmark][index] + ","
				data_str += "\n"
				fout.write(data_str)
		index = index + 1
	fout.write("\n\n\n\n")
	fout.write(stat_string)
	fout.close()
		
		
