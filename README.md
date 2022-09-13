# definition-acronym-extraction
This code allows users to extract definition-acronym pairs.\
Input can be a text or pdf file.\
Output is a json file including pairs.\
Optional operation is merging with a larger json file containin pairs.

# args
Choose between -t and -p, -jo is required, -ji is optional
```
("--text", "-t", help="set text input directory")
("--pdf", "-p", help="set pdf input directory")
("--jsonOutput", "-jo", help="set output json filename, must be .json")
("--jsonInput", "-ji", help="set JSON filename to append, must be .json")
```


# Example commands to run
```
python3 findDefinitions.py -p pdfs/doc.pdf -jo abbreviations.json
python3 findDefinitions.py -t pdfs/doc_Text.txt -jo abbreviations.json -ji abbreviationsList.json
```

# Outputs
If pdf is being processed, txt file with \_Text suffix is generated. 

# Things to be improved
Doesn't catch turkish definitions with english acronyms. Translate possible definitions to english 

