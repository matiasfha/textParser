# encoding: utf-8
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

class PDF2Txt:
	def __init__(self,pdffile,outfile,output_type='text'):
		PDFDocument.debug = 0
		PDFParser.debug = 0
		CMapDB.debug = 0
		PDFResourceManager.debug = 0
		PDFPageInterpreter.debug = 0
		PDFDevice.debug = 0
		self.rsrcmgr = PDFResourceManager(caching=True)
		self.outtype = output_type
		self.outfile = outfile
		self.pdffile = pdffile

	def convert(self):
		outfp = file(self.outfile,'w')
		if self.outtype == 'text':
			self.device = TextConverter(self.rsrcmgr,outfp,codec='utf-8',laparams=LAParams(),imagewriter=None)
		elif self.outtype == 'xml':
			self.device = XMLConverter(self.rsrcmgr, outfp, codec='utf-8', laparams=LAParams(),
							  imagewriter=None)
		elif self.outtype == 'html':
			self.device = HTMLConverter(self.rsrcmgr, outfp, codec='utf-8', scale=1,
							   layoutmode='normal', laparams=LAParams(),
							   imagewriter=None)
		else:
			print 'Formato de salida no soportado'
			sys.exit(-1)
		fp = file(self.pdffile,'rb')
		interpreter = PDFPageInterpreter(self.rsrcmgr,self.device)
		pagenos = set()
		for page in PDFPage.get_pages(fp,pagenos,caching=True,check_extractable=True):
			page.rotate = (page.rotate) % 360
			interpreter.process_page(page)
		fp.close()
		self.device.close()
		outfp.close()
		print "Archivo %s creado en base a %s" % (self.outfile,self.pdffile)

if __name__ == '__main__':
	if len(sys.argv) == 3:
		pdf2txt = PDF2Txt(sys.argv[1],sys.argv[2])
		pdf2txt.convert()
	elif len(sys.argv) == 4:
		pdf2txt = PDF2Txt(sys.argv[1],sys.argv[2],sys.argv[3])
		pdf2txt.convert()
	else:
		print 'Argumentos invalidos uso: pdfscrap.py pdffile outfile [output_type]'