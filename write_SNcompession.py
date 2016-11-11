# Load libraries
import sys, os
import ROOT
from larlite import larlite as fmwk
from ROOT import compress

# Create ana_processor instance
my_proc=fmwk.ana_processor()

# Specify IO mode
my_proc.set_io_mode(fmwk.storage_manager.kBOTH)
#my_proc.set_io_mode(fmwk.storage_manager.kWRITE)
#my_proc.set_io_mode(fmwk.storage_manager.kREAD)

# Set output root file: this is a separate root file in which your
# analysis module can store anything such as histograms, your own TTree, etc.
##################################################
##### TO SET OUTPUT FILE FROM COMMAND LINE #######
##      UNCOMMENT THE FOLLOWING 4 LINES:       ###

for x in xrange(len(sys.argv)-4):
    my_proc.add_input_file(sys.argv[x+1])
    my_proc.set_ana_output_file(sys.argv[-3]) #this is the output_ana root file, third from last entry in command line
    my_proc.set_output_file(sys.argv[-2])   #this is the compressed waveforms root file, second from last entry in command line

#### to run: $ python $LARLITE_USERDEVDIR/SNCompression/Compression/mac/write_SNcompression.py /PATH_TO_output_ana.root /PATH_TO_compressedWFs.root [ADC threshold]
##########################################
## AND COMMENT OUT THE FOLLOWING 4:     ##
##########################################
#for x in xrange(len(sys.argv)-2):
#    my_proc.add_input_file(sys.argv[x+1])
#    my_proc.set_ana_output_file("SNoutput_ana.root") #creates file in working directory
#    my_proc.set_output_file("compressedWFs.root") #creates file in working directory

#########################################
#### to run: $ python $LARLITE_USERDEVDIR/SNCompression/Compression/mac/write_SNcompression.py [ADC threshold]






#my_proc.set_output_rootdir("scanner")
# Create analysis class instance. For this example, ana_base.
# To show how one can run multiple analysis modules at once,
# we make multiple ana_base instance.

compAna=fmwk.ExecuteCompression()
compAna.SetSaveOutput(True)
compAna.SetUseSimch(False)
#add Compression Algorithm
compAlgo = compress.CompressionAlgosncompress()
compAlgo.SetDebug(False)
compAlgo.SetVerbose(False)
compAlgo.SetFillTree(False)
compAlgo.SetBlockSize(64)
compAlgo.SetBaselineThresh(2.0)
compAlgo.SetVarianceThresh(2.0)
thresh = float(sys.argv[-1])
compAlgo.SetCompressThresh(-thresh,thresh,thresh)
compAlgo.SetMaxADC(4095)
compAlgo.SetUVYplaneBuffer(55,18,47,30,20,20)
#compAlgo.SetUVYplaneBuffer(30,55,15,20,15,10);
compAna.SetCompressAlgo(compAlgo)

#add HIT study Algorithm
compStudy = compress.CompressionStudyHits()
compStudy.setThreshold(5.)
compStudy.setConsecutiveTicks(3)

#add IDE study Algorithm
compIDE = compress.CompressionStudyIDEs()
compIDE.SetVerbose(False)

compAna.SetCompressAlgo(compAlgo)
#compAna.SetCompressStudy(compStudy)
#compAna.SetIDEStudy(compIDE)

# Add analysis modules to the processor

my_proc.add_process(compAna)

# Let's run it.

my_proc.run()
#my_proc.run(0,1)

# done!
