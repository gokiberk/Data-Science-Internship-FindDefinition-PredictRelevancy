# definition-acronym-extraction
This code allows users to extract acronym-definition pairs.\
Input can be a text or pdf file.\
Output is a json file including pairs.\
Optional operation is merging with a larger json file containing acronym-definition pairs. This will modify the input json file and recently encountered pairs will be merged with input file. In case of having the same acronym in input file, it is kept instead of adding new pair.

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
- If pdf is being processed, txt file with \_Text suffix is generated.\
e.g. doc_Text.txt
- passToSchwartz text files are generated within the span depending on acronyms' length.\
e.g. passToSchwartz3.txt
- Json file including recently encountered acronym-definition pairs.\
e.g. abbreviations.json
- Modified json input file that new pairs are appended to. \
e.g. myAbbreviationsList.json


# Things to be improved
Doesn't catch turkish definitions with english acronyms. Translate possible definitions to english then pass to schwartz algorithm again

