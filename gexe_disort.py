#!/bin/python
#***********************************************************************
# Written By Gagan Sharma :
# 16th Jan, 2014, Department of Radiology, The University of Melbourne
# Australia
#
# Write a complete sorter and deidentfier in Python.....
# 
#***********************************************************************

usage = """
Usage:
python gexe_sort.py inputdicom_dir ouput_dir
OR.....
python gexe_sort.py inputdicomfile.dcm outputdicomfile.dicom
"""

# Rigrous testing required.....

def _create_dic_from_translation_table():
	 #Read the text file of translation table
	 #First element of each row is Deidenfied variable for particular
	 #PatientID..Chronologically...given...
	 global dic
	 transt_file = open('/home/gsharma/Programming/Python/gexe_sort/stoptranstable.txt','r')
	 #Create an empty dictionary....
	 dic={}
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

# Rigrous testing Required.....	 
def _anonmyize(filename,remove_private_tags=True):
	# filename: Source which needs to be anonymized.
	# newloc: Where should this file should be stored.
	# newname: New name for this file.
	# remove private tags is the flag to remove these private tags.

	 # This is pydicom beauty... Once call back and recursively I can 
	 # access all the tags which have PN as VR....
	 global dic
	 foldername='/home/gsharma/Programming/Python/gexe_sort/DICOM/'
	 def PN_callback(ds, data_element):
	 	if data_element.VR == "PN":
	 		data_element.value = de_name

	 try:
		ds = dicom.read_file(filename,force=True)
	 except:
		print "Not a dicom file...."
	 
	 if dic.has_key(ds.PatientID):
	 	de_name=dic[ds.PatientID]
	 else:
	 	print "Dictionary does not has the key......"
	 	sys.exit()

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

	 foldername=foldername+'/'+de_name+'/'+str(ds.StudyDate)+'T'+str(ds.StudyTime)+'/'+str(ds.SeriesNumber)+'_'+str(ds.SeriesDescription).replace(" ","_")
	 fname=de_name+'_'+str(ds.Modality)+'_'+str(ds.StudyDate)+'T'+str(ds.StudyTime)+'_'+str(ds.SeriesNumber)+'_'+str(ds.SeriesInstanceUID)+'_'+str(ds.InstanceNumber)
	 print fname
	 if not os.path.exists(foldername):
	 	os.makedirs(foldername)
         
	 if not os.path.isfile(foldername+'/'+fname):
		ds.save_as(foldername+'/'+fname)
	 else:
		print "Duplicate......"


if __name__ == '__main__':
	
	try:
		#Pydicom library developed by MIT..Very Intitutive...
		import dicom
		import os
		import sys
	except Exception:
		print "Cannot import required libraries.Please Check...."
		exit()
	
	_create_dic_from_translation_table()

	
	# Lets read the directory or a file....
	if len(sys.argv) != 2:
		print (usage)
		sys.exit()
    
    #
	if os.path.isdir(sys.argv[1]):
		dname=os.path.basename(sys.argv[1])
		for root,dir,files in os.walk(sys.argv[1]):
			for each in files:
				_anonmyize(os.path.join(root,each))
