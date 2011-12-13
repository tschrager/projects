import glob
import numpy
import matplotlib
matplotlib.use('Agg')
import pylab
from os.path import basename,splitext

wiki_dir='../../projects.wiki/'

bins=numpy.arange(-2048,2048,1)

wikifile = open(wiki_dir+'plots.mediawiki','w')

for file in glob.glob('data/*.npy'):
	currenthist=numpy.load(file)
	pylab.clf()
	pylab.plot(bins,currenthist,marker='.',linestyle='None')
	rms = numpy.sqrt(1/numpy.sum(currenthist) * numpy.sum(numpy.square(bins)*currenthist) )
	pylab.savefig(wiki_dir + '/images/' + splitext(basename(file))[0] + '.png',format='png')
	alttext = splitext(basename(file))[0] + ' rms: ' + `rms` + ' samples: ' + `numpy.sum(currenthist)`

	wikifile.write('[[images/' + splitext(basename(file))[0] + '.png | frame | alt=' + alttext + ']]\n')

	#display a log plot
	pylab.clf()
	pylab.plot(bins,currenthist,marker='.',linestyle='None')
	pylab.yscale('log')
	pylab.savefig(wiki_dir + 'images/' + splitext(basename(file))[0] + '_log.png',format='png')
	wikifile.write('[[images/' + splitext(basename(file))[0] + '_log.png | frame | alt=' + splitext(basename(file))[0] + ' log plot]]\n')

wikifile.close()






