from optparse import OptionParser

parser = OptionParser()
parser.add_option("-tb", "--table", dest="tablename",help="translation table", metavar="FILE")
parser.add_option("-s", "--source", dest="source",help="source data")
parser.add_option("-td", "--target", dest="target",help="target destination")
