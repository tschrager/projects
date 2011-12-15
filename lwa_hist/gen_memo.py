#!/opt/local/bin/python

import glob
import numpy
import matplotlib
matplotlib.use('Agg')
import pylab
from os.path import basename,splitext

bins=numpy.arange(-2048,2048,1)

texfile = open('plots.tex','w')
figuretext = '\\begin{figure}[ht] \
				\\subfloat{\\includegraphics[width=0.5\\textwidth]{%s}} \
				\\subfloat{\\includegraphics[width=0.5\\textwidth]{%s}} \
				\\caption{%s} \
				\\end{figure} \n\n'
				
figurecaption = 'Data from %s. RMS is %f Samples used : %d. If the RMS is unchanged %f percent of the samples will lie within [-128,128). \
 				 With an RMS of 20 %f percent of the samples will lie within [-128,128).'

for file in glob.glob('data/*.npy'):
	currenthist=numpy.load(file)
	
	figurename = 'plots/' + splitext(basename(file))[0] + '.png'
	logfigurename = 'plots/' + splitext(basename(file))[0] + '_log.png'
	
	pylab.clf()
	
	# pylab.plot(bins,currenthist/numpy.sum(currenthist),marker='.',linestyle='None')
	# pylab.xlabel('Power level')
	# pylab.ylabel('Frequency')
	# pylab.savefig(figurename,format='png')
	# #display a log plot
	# pylab.yscale('log')
	# pylab.savefig(logfigurename,format='png')
	
	
	rms = numpy.sqrt(1/numpy.sum(currenthist) * numpy.sum(numpy.square(bins)*currenthist) )
	percentunchwithin8bits = numpy.sum(currenthist[2048-128:2048+128])/numpy.sum(currenthist)*100
	percentrms20withing8bits = numpy.sum(currenthist[int(2048-128*rms/20)+1:int(2048+128*rms/20)])/numpy.sum(currenthist)*100

	thisfigurecaption = figurecaption % (splitext(basename(file))[0].strip('hist'), rms, numpy.sum(currenthist),percentunchwithin8bits, percentrms20withing8bits)
	
	texfile.write(figuretext % (figurename,logfigurename,thisfigurecaption,) )

texfile.close()








