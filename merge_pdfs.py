from PyPDF2 import PdfMerger, PdfReader
import glob
 
mergedObject = PdfMerger()
filenames = glob.glob("white_papers/*.pdf")

for file in filenames:
    mergedObject.append(PdfReader(file, 'rb'))
 
mergedObject.write("All Decadal White Papers.pdf")