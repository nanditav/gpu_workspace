#!/usr/bin/python

import os
import sys
import re
import subprocess
import argparse

home = "/home/nandita/gena_work/gpgpusim_compression_repo/gpgpu-sim/"
#subprocess.call("source /home/nandita/set_env.sh",shell=True)
# BFS 
os.chdir(home + "/benchmarks/CUDA/BFS/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "BFS compiled\n"
os.chdir(home + "/benchmarks/CUDA/JPEG/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "JPEG compiled\n"
os.chdir(home + "/benchmarks/CUDA/LPS/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "LPS compiled\n"
os.chdir(home + "/benchmarks/CUDA/MUM/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "MUM compiled\n"
os.chdir(home + "/benchmarks/CUDA/NN/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "NN compiled\n"
os.chdir(home + "/benchmarks/CUDA/STO/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "STO compiled\n"
os.chdir(home + "/benchmarks/CUDA/SCP/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "SCP compiled\n"
os.chdir(home + "/benchmarks/Mars/sample_apps/PageViewRank/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "PVR compiled\n"
os.chdir(home + "/benchmarks/Mars/sample_apps/PageViewCount/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "PVC compiled\n"
os.chdir(home + "/benchmarks/Mars/sample_apps/SimilarityScore/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "SimilarityScore compiled\n"
os.chdir(home + "/benchmarks/Mars/sample_apps/InvertedIndex/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "InvertedIndex compiled\n"
os.chdir(home + "/benchmarks/rodinia/cuda/backprop/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "backprop compiled\n"
os.chdir(home + "/benchmarks/rodinia/cuda/hotspot/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "hotspot compiled\n"
os.chdir(home + "/benchmarks/rodinia/cuda/streamcluster/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "streamcluster compiled\n"
os.chdir(home + "/benchmarks/lonestar/")
subprocess.call("make clean",shell=True)
subprocess.call("make",shell=True)
print "lonestar compiled\n"
