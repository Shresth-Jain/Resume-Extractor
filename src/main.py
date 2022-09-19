"""
  Resume Extractor App:

  This application can be used to extract the resumes from a csv file and store the same in a zip file
  Please note that the following conditions must hold:
  1) The program can only read csv file.
  2) The csv file must have all the resume links under a column header : "resume".

"""

# 
# import subprocess

# # Install dependencies
# bashCommand = "pip install -r requirements.txt"
# process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()

"""
  Imports
"""

# To interact with csv file
import pandas as pd
import os
# To fetch URL data
import urllib.request

# For GUI Interface to get files path (Select csv file)
from getFilePath import App 

# For Progress bar effect
from tqdm import tqdm
from time import sleep

# For Zipping Files
import shutil

# For logging
import logging

# for opening the log file at the end
import webbrowser

"""Global Variables"""
logFilePath=""

""" Create the Folder to store Extracted resumes """
def createFolder(ResumeFolder):
  path= ResumeFolder
  if(os.path.isdir(path)):
    print('\n[INFO] Folder with same name Found. Cleaning old files!')
    # Remove already existing files in folder if folder exist
    for f in os.listdir(path):
      os.remove(os.path.join(path, f))
    print('[INFO] Cleaning Done! Old Files removed from the Resume Folder.')
  else:
      # Create the folder
      os.makedirs(path,exist_ok=True)
      print('[INFO] Resume Folder Created')

""" Get column number of the Name of student """
def createNameListEnum(columns, nameList):
  nameListEnum = []
  for name in nameList:
    try:
      nameListEnum.append(columns.index(name))
    except Exception as e:
      print(name + " is not a valid column name")
  return nameListEnum

""" Get column number of the Roll Number of student """
def createRollNumberEnum(columns, rollNumberColumn):
  rollListEnum = 0
  try:
    rollListEnum=columns.index(rollNumberColumn)
  except Exception as e:
    print(rollNumberColumn + " is not a valid column name for roll number")
  return rollListEnum

""" Get column number of the Resume Links of student """
def createResumeColumnEnum(columns, resumeColumn):
  resumeColumnEnum = 0
  try:
    resumeColumnEnum = columns.index(resumeColumn)
  except Exception as e:
    print(resumeColumn + " is not a valid column name")
  return resumeColumnEnum

""" 
  Make File name of each resume.pdf
  Current Format: NAME_BRANCH_ROLL_NUMBER.pdf
"""
def getFileName(row, nameListEnum, rollListEnum):
  fileNames = []
  for nameIndex in nameListEnum:
    name = "_".join(str(row[nameIndex]).upper().split(" "))
    fileNames.append(name)
  # Insert Roll Number 
  rollNo="_".join(str(row[rollListEnum]).upper().split("/"))
  fileNames.append(rollNo)
  # Create fileName from name and roll number seperated by _
  fileName = "_".join(fileNames)
  # fileName = fileName + "_Delhi_Technological_University_2022";
  return fileName

""" Fetch Resume from the URL """
def fetchURLData(url, fileName, ResumeFolder):
  try:
    urllib.request.urlretrieve(url, ResumeFolder + "/" + fileName + '.pdf')
    return ""
  except Exception as e: 
    return fileName

def ResumeZIPGenerator(applicationList, nameList, rollNumberColumn, resumeColumn, ResumeFolder,parentFolder):
  '''
    applicationList: string -> Path containing the applications file (.csv)
    nameList: list of strings-> An ordered list of the column names which are to be included in the Resume name
    resumeColumn: string -> Column name containing the resume links of the students
    ResumeFolder: string -> Directory to store all the resumes
    Downloads all the resumes in the chosen naming convention in a zip file.
  '''
  
  try: 
    createFolder(ResumeFolder)
  except Exception as e:
    logging.info("Folder already created")


  logging.basicConfig(filename=logFilePath, filemode='w', 
      level=logging.DEBUG,
      # %(asctime)s.%(msecs)03d 
    format='%(levelname)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
  
  df = pd.read_csv(applicationList,encoding='Latin-1')
  print("File Path is correct")
  X = df.values
  n = len(X)
  noOfRows = len(df)
  columns = list(df.columns)
  # To prevent Error, Convert all strings to lowerCase for comparison
  for i in range(len(columns)):
    columns[i] = columns[i].lower()
  
  nameListEnum = createNameListEnum(columns,  nameList)
  rollListEnum = createRollNumberEnum(columns,  rollNumberColumn)
  resumeColumnEnum = createResumeColumnEnum(columns, resumeColumn)

  exception = []
  print('Extracting Resumes from Links.')
  with tqdm(total=noOfRows) as pbar:
    for i in range(noOfRows):
      fileName = getFileName(X[i], nameListEnum,rollListEnum)
      url = X[i][resumeColumnEnum]

      tmp = fetchURLData(url, fileName, ResumeFolder)
      if len(tmp) > 0: 
        errStatement="Name/RollNumber:" + tmp + " || Resume Link:"+ url
        exception.append(errStatement)

      pbar.update(1)
  programStatus=""
  if len(exception)==0:
    programStatus="Successful"
  else:
    programStatus="Partial"

  logging.info("Resume fetching completed.")
  logging.info("Status till now: " + programStatus)

  logging.info("Resume Downloaded: ("+str(noOfRows-len(exception))+") out of ("+ str(noOfRows)+")")
  if len(exception) > 0:
    print("The Resumes couldn't be fetched for the following students: CHECK LOG file ")
    logging.critical("The Resumes couldn't be fetched for the following students: ")
    for e in exception:
      # Print exceptions to the log file
      print(e)
      logging.critical(e)

  print('[INFO] Extraction complete. Zipping the resume folder')
  # logging.info("Extraction complete. Zipping the resume folder")
  shutil.make_archive(ResumeFolder, 'zip', ResumeFolder)

  # Open the final report document

  print('Opening the parent Folder and Log file in explorer in 2 sec.')
  print("===========================================================")
  os.system('start '+ parentFolder+"\\"+JobProfileName)

  webbrowser.open(logFilePath)


if __name__ == '__main__':
  

  # Add csv file path to the applicationList. GUI panel appears
  nap=App()
  applicationList=nap.getFilePath()
  nameList = ['name']
  resumeColumn = "resume"
  rollNumberColumn = "rollno"
  # isDrive = False
  # Take resume folder name from the CSV File
  JobProfileName=(applicationList.split('/')[-1]).split('.')[0]
  JobProfileName=JobProfileName.replace(' ','_')
  parentFolder=nap.getDirectoryPath()
  logFilePath=parentFolder+"\\"+JobProfileName+"\\"+JobProfileName+'.log'

  ResumeFolder=parentFolder+"\\"+JobProfileName+"\\DTU_"+JobProfileName +"_Resumes"
  ResumeZIPGenerator(applicationList, nameList, rollNumberColumn, resumeColumn, ResumeFolder,parentFolder)