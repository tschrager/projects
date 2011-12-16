#!/opt/local/bin/python

import glob
import numpy
import matplotlib
matplotlib.use('Agg')
import pylab
from os.path import basename,splitext
import sympy.galgebra.latex_ex as tex

bins=numpy.arange(-2048,2048,1)

imagefile = open('plots.tex','w')
tablefile = open('table.tex','w')
figuretext = '\\begin{figure}[ht] \
				\\subfloat{\\includegraphics[width=0.5\\textwidth]{%s}} \
				\\subfloat{\\includegraphics[width=0.5\\textwidth]{%s}} \
				\\caption{%s} \
				\\end{figure} \n\n'
				
figurecaption = 'Data from %s. RMS is %.4f Samples used : %d. If the RMS is unchanged %.4f percent of the samples will lie within [-128,128). \
 				 With an RMS of 20 %.4f percent of the samples will lie within [-128,128).'
 				 
resultsarray = numpy.array(['\\text{Stand}','\\text{RMS}','\\text{samples }\in [-128,128)','\\text{samples }\in [-128,128)\\text{ with RMS}=20'])

for file in glob.glob('data/*.npy'):
    currenthist=numpy.load(file)

    figurename = 'plots/' + splitext(basename(file))[0] + '.png'
    logfigurename = 'plots/' + splitext(basename(file))[0] + '_log.png'

    rms = numpy.sqrt(1/numpy.sum(currenthist) * numpy.sum(numpy.square(bins)*currenthist) )
    percentunchwithin8bits = numpy.sum(currenthist[2048-128:2048+128])/numpy.sum(currenthist)*100
    percentrms20withing8bits = numpy.sum(currenthist[int(2048-128*rms/20)+1:int(2048+128*rms/20)])/numpy.sum(currenthist)*100

    thisfigurecaption = figurecaption % (splitext(basename(file))[0].strip('hist'), rms, numpy.sum(currenthist),percentunchwithin8bits, percentrms20withing8bits)

    imagefile.write(figuretext % (figurename,logfigurename,thisfigurecaption,) )

    resultsarray = numpy.vstack([resultsarray,(splitext(basename(file))[0].strip('hist'),rms, '%.4f\\%%'%percentunchwithin8bits, '%.4f\\%%'%percentrms20withing8bits )])

    pylab.clf()

    pylab.plot(bins,currenthist/numpy.sum(currenthist),marker='.',linestyle='None')
    pylab.xlabel('Power level')
    pylab.ylabel('Frequency')
    pylab.axvspan(-128,128,facecolor='blue', alpha=0.25)
    pylab.axvspan(-128*rms/20,-128,facecolor='y', alpha=0.25)
    pylab.axvspan(128,128*rms/20,facecolor='y',alpha=0.25)
    pylab.savefig(figurename,format='png')
    #display a log plot
    pylab.yscale('log')
    pylab.ylabel('Frequency (log scale)')
    pylab.savefig(logfigurename,format='png')


tablefile.write(tex.LaTeX(resultsarray,inline=True).replace('#','').replace('cccc','c||c|c|c').replace('\\left [','').replace('\\right ]',''))

imagefile.close()
tablefile.close()








