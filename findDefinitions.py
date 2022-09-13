# input options: "-p" pdf input or "-t" txt input. Either of the formats can be used to find abbreviations from text.
# must: "-jo" name of the abbreviaton file to be created
# optional: "-ji" if this args is given, recently createad abbreviations file will be merged into this file (in case of having the same abbreviation, keeps the one in this file)
# example commands: 
# python3 findDefinitions.py -p pdfs/ssb.pdf -jo abbreviations.json
# python3 findDefinitions.py -p pdfs/ssb_Text.txt -jo abbreviations.json -ji abbreviationsList.json

# Include standard modules
from abbreviations import schwartz_hearst
import argparse
import re
import fitz
import itertools
import json
from pprint import pprint
from jsonmerge import merge
import os

#helper function for mergeTwoJSON function
#@param: jsonFile, filepath to a json file
def openJSON(jsonFile):
    with open(jsonFile) as f:
        j1 = json.load(f)
    return j1

#@param: json1 and json2, filepaths to json files
# merge() function priotizes second input and keeps its value when there are same keys
def mergeTwoJSONFiles( json1, json2):
    j1 = openJSON(json1)
    j2 = openJSON(json2)
    return merge(j1, j2)

#@param: @param: json1 filepath to json file, json2 dictionary
def mergeJSONFileAndDict( json1, json2):
    j1 = openJSON(json1)
    j2 = json2
    return merge(j1, j2)

# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--text", "-t", help="set text input directory")
parser.add_argument("--pdf", "-p", help="set pdf input directory")
parser.add_argument("--jsonOutput", "-jo", help="set output json filename, must be .json")
parser.add_argument("--jsonInput", "-ji", help="set JSON filename to append, must be .json")

# Read arguments from the command line
args = parser.parse_args()

# Check for --text
if args.text:
    print("Text directory set to %s" % args.text)
if args.pdf:
    print("PDF directory set to %s" % args.pdf) 
if args.jsonOutput:
    print("Output JSON filename set to %s" % args.jsonOutput)
if args.jsonInput:
    print("Input JSON filename set to %s" % args.jsonInput)
    
fileReceived = False

if args.pdf:
    fileDirectory = args.pdf #user can define as input
    outputTextNameBody = ((args.pdf).rstrip(".pdf")) #user can define as input
    outputTextName = outputTextNameBody + "_Text.txt"
    doc = fitz.open(fileDirectory)  #open document
    out = open( outputTextName, "wb")  #open text output
    for page in doc:  #iterate the document pages
        text = page.get_text().encode("utf8")  #get plain text (is in UTF-8)
        out.write(text)  #write text of page
        out.write(bytes((12,)))  #write page delimiter (form feed 0x0C)
    out.close()
    
    with open(outputTextName, "r") as file: 
        rawDataStr = file.read()
    dataStr = re.sub('(\n[A-ZÜŞİÖÇ0-9])(\n)', r'\1', rawDataStr) #merge large font capital letters of paragraphs with body
    
    f = open(outputTextName, "w")
    f.write(dataStr)
    f.close()
    
    print("PDF to Text Conversion Completed!\nSaved with filename: " + outputTextName)
    fileReceived = True
    
elif args.text:
    with open(args.text, "r") as file: 
        rawDataStr = file.read()
    dataStr = re.sub('(\n[A-ZÜŞİÖÇ0-9])(\n)', r'\1', rawDataStr) #merge large font capital letters of paragraphs with body
    fileReceived = True   
    
if( fileReceived):
    
    
    pattern = re.compile(r"\(([^(^)]+)\)") #find all statements between parantheses, ( ) should not include "(" ")"
    dataParanthesesStr = ""
    dataParanthesesList = []
    for match in pattern.finditer(dataStr):
        #eng = translator.translate(match.group(), dest='en')
        dataParanthesesList.append(match.group())
        dataParanthesesStr += str(match.group())
        
    #translator.translate(match.group(), dest='en')
    
    dataParanthesesList = [ x for x in dataParanthesesList if "(312)" not in x ]
    dataParanthesesList = [ x for x in dataParanthesesList if "(+90)" not in x ]
    dataParanthesesList = [ x for x in dataParanthesesList if "(4x4)" not in x ]
    #dataParanthesesList = [ x for x in dataParanthesesList if "ML8" not in x ]
    
    dataDeleteNewlineList = []
    dataDeleteNewlineStr = ""
    for sub in dataParanthesesList:
        dataDeleteNewlineList.append(sub.replace("\n", "")) #delete all newlines between parantheses
    for i in range (len(dataDeleteNewlineList)):
        dataDeleteNewlineStr +=  str(i) + "---" + dataDeleteNewlineList[i] + "\n"
    print("Number of parantheses found: " + str(len(dataDeleteNewlineList)))
    #for i in dataDeleteNewlineList:
        #print(i)

    dataList = dataStr.split()
    #print(dataList)
    definitions = ""
    notFoundTexts = ""
    found = 0
    defList = list(0 for i in range(0,len(dataDeleteNewlineList)))
    notFoundList = list(1 for i in range(0,len(dataDeleteNewlineList)))

    spanVar = [-1, 2, 5]
    j = len(spanVar)
    checkDefList = ""
    for j in range(len(spanVar)):
        for k in range(len(dataDeleteNewlineList)):
            index = len(tuple(itertools.takewhile(lambda x: (dataDeleteNewlineList[k]) not in x, dataList))) #when dataStr is splitted, it doesn't work with expressions that have space
            length = len(dataDeleteNewlineList[k]) - 2
            span = length + spanVar[j]
            if (span <= min(length*2, length+5)):
                i = span
                definition = ""
                while ( i > 0):
                    try:
                        dataList[index-i].replace("\n", " ")
                    except:
                        print("noNewline")  
                    definition += " " + dataList[index-i]
                    i-=1
                
            
            #definitions += str(k)+definition+uniqueList[k]+"\n"
            checkDef = definition + " " + dataDeleteNewlineList[k]
            
            lower_map = {
                ord(u'İ'): u'i',
            }
            
            #checkDef.replace(r"\İ(?=[^()]*\))", "i");
            
            checkDef = checkDef.translate(lower_map)
            checkDefList += checkDef + "\n"
    
        checkDefListTxt = "passToSchwartz" + str(spanVar[j]) + ".txt"
        f = open(checkDefListTxt, "w")
        f.write(checkDefList)
        f.close()
        checkDefList = ""
        chcekDef = ""

        pairs = schwartz_hearst.extract_abbreviation_definition_pairs(file_path=checkDefListTxt)     
        print( "Number of acronym-definition pairs: " + str(len(pairs)) )
        jsonOutName = 'tmp_pairs' + str(spanVar[j]) + '.json'
        with open(jsonOutName, 'w', encoding ='utf8') as json_file:
            json.dump(pairs, json_file, ensure_ascii = False)
        print("JSON File Created: " + jsonOutName)
    
    mergedNew = {}
    for m in range(len(spanVar)):
        jsonFilesToBeDeleted = 'tmp_pairs' + str(spanVar[m]) + '.json' #deleting the intermediate json files 
        mergedNew = mergeJSONFileAndDict(jsonFilesToBeDeleted, mergedNew)
        file_path = jsonFilesToBeDeleted
        if os.path.isfile(file_path):
            os.remove(file_path)
        print("Deleted temporary JSON files.")
    print("No of abbreviations found: ", len(mergedNew))
    
    mergedNew = {k.replace('i', 'İ'): mergedNew.pop(k) for k in list(mergedNew.keys())}
        
    with open(args.jsonOutput, 'w', encoding ='utf8') as json_file:
        json.dump(mergedNew, json_file, ensure_ascii = False)
    print("JSON File Created: " + args.jsonOutput)
    
        
    if args.jsonInput:
        print("Appending recent abbreviations to " + args.jsonInput)
        mergedLast = mergeTwoJSONFiles( args.jsonOutput, args.jsonInput)
        
        with open(args.jsonInput, 'w', encoding ='utf8') as json_file:
            json.dump(mergedLast, json_file, ensure_ascii = False)
        print("Appended to " + args.jsonInput)

    
#else file not received
    else:
        print("File not received.")    



