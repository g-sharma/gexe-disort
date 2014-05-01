#!/bin/python
#***********************************************************************
# Written By Gagan Sharma :
# 16th Jan, 2014, Department of Radiology, The University of Melbourne
# Australia
# 
# To Do:
# 1.Create a comprehensive report if there is some issues in the trasition table.
# 2.Create a readable log
#   Which this patient is
#   When was sorted and which series 
#   
# Write a complete sorter and deidentfier in Python.....
#
# 
#***********************************************************************

# Rigorous testing required.....

def _create_dic_from_translation_table(table):
	 #Read the text file of translation table
	 #First element of each row is Deidenfied variable for particular
	 #PatientID..Chronologically...given...
	 global dic
	 transt_file = open(table,'r')
	 # Looping through each line.....
	 for line in transt_file:
		# What the below line is doing
  		# Well, it split each line based on comma and then covert the line in to tuple/list
 		# For example: Patient0001,256897,9996385 will become ['Patient0001','256897','9996385']
	 	tup=line.strip('\n').strip(',').split(',')
	 	#Creating every id as the key and having our deidentfied 
	 	#value......
		#Below code will run upto N-1 values
		#First value is Patient0001(our deidentified mapping value, will be given to all the ID's of that patient
		#Every Key(PatientID) will have its own mapping Deidentified value given by user for example 256897 will have Patient0001 as its value
	 	for i in xrange(len(tup)-1):
	 		dic[tup[i+1]]=tup[0]	

def _mreplace(text, wordDic):
        """
                take a text and replace words that match a key in a dictionary with
                the associated value, return the changed text
        """
        rc = re.compile('|'.join(map(re.escape, wordDic)))
        def translate(match):
                return wordDic[match.group(0)]
        return rc.sub(translate, text)



# Rigrous testing Required.....	 
def _anonmyize(filename,foldername,remove_private_tags=True):
	# filename: Source which needs to be anonymized.
	# newloc: Where should this file should be stored.
	# newname: New name for this file.
	# remove private tags is the flag to remove these private tags.

	 # This is pydicom beauty... Once call back and recursively I can 
	 # _andrew_trans_table.txt all the tags which have PN as VR....
	 global dic,dupfiles
	 
	 rep_dic={
	 ' ':'_',
         '^':'_',
         '/':'_',
	 '__':'_',
	 '  ':'_'}
	 
	 def PN_callback(ds, data_element):
	 	if data_element.VR == "PN":
	 		data_element.value = de_name

	 try:
		ds = dicom.read_file(filename)
	 except:
		print "Not a dicom file...."
		return
	 
	 if dic.has_key(ds.PatientID):
	 	de_name=dic[ds.PatientID]
	 else:
	 	print "Dictionary does not has the key......"
		return

	 ds.walk(PN_callback)

	 ds.PatientID = de_name
	 
	 for name in ['OtherPatientIDs', 'OtherPatientIDsSequence']:
	 	if name in ds:
	 		delattr(ds, name)

	 for name in ['PatientBirthDate']:
	 	if name in ds:
	 		ds.data_element(name).value = de_name

	 if remove_private_tags:
	 	ds.remove_private_tags()
   
	 try:
		if not "SeriesDescription" in ds:
			ds.SeriesDescription='NA'
	 except:
		pass
        
	 print "Checking....."+filename 
	 
         seriesName=_mreplace(ds.SeriesDescription,rep_dic)
	 foldername=foldername+'/'+de_name+'/'+str(ds.StudyDate)+'T'+str(ds.StudyTime)+'/'+str(ds.SeriesNumber)+'_'+seriesName  #str(ds.SeriesDescription).replace(" ","_")
	 fname=de_name+'_'+str(ds.Modality)+'_'+str(ds.StudyDate)+'T'+str(ds.StudyTime)+'_'+str(ds.SeriesNumber)+'_'+str(ds.SeriesInstanceUID)+'_'+str(ds.InstanceNumber)
	 if not os.path.exists(foldername):
	 	os.makedirs(foldername)
          
	 if not os.path.isfile(foldername+'/'+fname):
		ds.save_as(foldername+'/'+fname)
	 else:
		print "Duplicate......"
		dupfiles.append(filename)



if __name__ == '__main__':
	
	global dupfiles,dic
	dupfiles=[]
	dic={}
	try:
		#Pydicom library developed by MIT..Very Intitutive...
		import dicom
		import os
		import sys
		import re
		from optparse import OptionParser
	except Exception:
		print "Cannot import required libraries.Please Check...."
		exit()
	
	parser = OptionParser()
	parser.add_option("-t", "--table", dest="tablename",help="translation table")
	parser.add_option("-s", "--source", dest="source",help="source data")
	parser.add_option("-d", "--target", dest="target",help="target destination")

	(options,args) = parser.parse_args()

	_create_dic_from_translation_table(options.tablename)

	   
    #
	if os.path.isdir(options.source):
		dname=os.path.basename(options.source)
		for root,dir,files in os.walk(options.source):
			for each in files:
				print options.target
				_anonmyize(os.path.join(root,each),options.target)

        print "Total Number of Duplicate files = "+str(len(dupfiles)) 
