### Run the following code in Google Colab to download the resumes of the students in a zip file.

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from google.colab import auth
# from oauth2client.client import GoogleCredentials
import pandas as pd
# from google.colab import files
# import progressbar
import os
import urllib.request
import shutil
"""
  For GUI Interface to Select files
"""
from getFilePath import App 
"""
  For Progress bar effect
"""
from tqdm import tqdm
from time import sleep

# def installLibs():
#   !pip install -U -q PyDrive

def createFolder(ResumeFolder):
  path=os.getcwd()+"\\" + ResumeFolder
  if(os.path.isdir(path)):
    print('\n[INFO] Folder with same name Found. Cleaning old files!')
    # Remove already existing files in folder if folder exist
    for f in os.listdir(path):
      os.remove(os.path.join(path, f))
    print('[INFO] Cleaning Done! Old Files removed from the Resume Folder.')
  else:
      # Create the folder
      os.mkdir(path)
      print('[INFO] Resume Folder Created')

def createNameListEnum(columns, nameList):
  nameListEnum = []
  for name in nameList:
    try:
      nameListEnum.append(columns.index(name))
    except Exception as e:
      print(name + " is not a valid column name")
  # print(nameListEnum)
  return nameListEnum

def createRollNumberEnum(columns, rollNumberColumn):
  rollListEnum = 0
  try:
    rollListEnum=columns.index(rollNumberColumn)
  except Exception as e:
    print(name + " is not a valid column name for roll number")
  # print(rollListEnum)
  return rollListEnum

def createResumeColumnEnum(columns, resumeColumn):
  resumeColumnEnum = 0
  try:
    resumeColumnEnum = columns.index(resumeColumn)
  except Exception as e:
    print(resumeColumn + " is not a valid column name")
  return resumeColumnEnum

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

def fetchDriveData(file_id, fileName, ResumeFolder):
  print(file_id)
  try:
      downloaded = drive.CreateFile({'id': file_id})
      downloaded.GetContentFile(ResumeFolder + "/" + fileName + ".pdf")
      return ""
  except Exception as e: 
    return fileName

def fetchURLData(url, fileName, ResumeFolder):
  try:
    urllib.request.urlretrieve(url, ResumeFolder + "/" + fileName + '.pdf')
    return ""
  except Exception as e: 
    return fileName

def downloadResumes(ResumeFolder):
  shutil.make_archive(ResumeFolder, 'zip', ResumeFolder)
  files.download(ResumeFolder + ".zip")

def ResumeZIPGenerator(applicationList, nameList, rollNumberColumn, resumeColumn, isDrive, ResumeFolder):
  '''
    applicationList: string
    Path containing the applications file (.csv)
    nameList: list of strings
    An ordered list of the column names which are to be included in the Resume name
    resumeColumn: string
    Column name containing the resume links of the students
    isDrive: boolean
    True if the content is to be fetched from a drive else false
    ResumeFolder: string
    Directory to store all the resumes
    Downloads all the resumes in the chosen naming convention in a zip file.
  '''

#   if isDrive == True:
#     installLibs()

  try: 
    createFolder(ResumeFolder)
  except Exception as e:
    print("[INFO] Folder already created")

  df = pd.read_csv(applicationList,encoding='Latin-1')
  print("[INFO] File Path is correct")
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

  # widgets = [' [', progressbar.Timer(format= 'elapsed time: %(elapsed)s'), '] ', progressbar.Bar('='),' (', progressbar.ETA(), ') ',]
  # bar = progressbar.ProgressBar(max_value=n, widgets=widgets).start()

  exception = []
  print('[INFO] Extracting Resumes from Links.')
  with tqdm(total=noOfRows) as pbar:
    for i in range(noOfRows):

      fileName = getFileName(X[i], nameListEnum,rollListEnum)

      if isDrive == True:
        file_id = X[i][resumeColumnEnum].split("id=")[1]
        tmp = fetchDriveData(file_id, fileName, ResumeFolder)
        if len(tmp) > 0: exception.append(tmp)

      else:
        url = X[i][resumeColumnEnum]
        # print(url)
        tmp = fetchURLData(url, fileName, ResumeFolder)
        if len(tmp) > 0: exception.append(tmp)
      pbar.update(1)

  print("[INFO] Resume Downloaded: ("+(noOfRows-len(exception))+") out of ("+ (noOfRows)+")")
  if len(exception) > 0:
    print("[WARNING] The Resumes couldn't be fetched for the following students:")
    for e in exception:
      print(e)
  print('[INFO] Extraction complete. Downloading the resume folder')
#   downloadResumes(ResumeFolder)

if __name__ == '__main__':

  # Add csv file path to the applicationList. GUI panel appears
  nap=App()
  applicationList=nap.getPath()

  # applicationList='Uber Internship 2024 (1).csv'
  nameList = ['name', 'branch']
  resumeColumn = "resume"
  rollNumberColumn = "rollno"
  isDrive = False
  # Take resume folder name from the CSV File
  JobProfileName=(applicationList.split('/')[-1]).split('.')[0]
  JobProfileName=JobProfileName.replace(' ','_')
  ResumeFolder = "DTU_"+JobProfileName +"_Resumes"
  ResumeZIPGenerator(applicationList, nameList, rollNumberColumn, resumeColumn, isDrive, ResumeFolder)