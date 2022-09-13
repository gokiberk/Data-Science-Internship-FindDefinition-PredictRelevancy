# definition-acronym-extraction
This code allows users to extract definition-acronym pairs.\
Input can be a text or pdf file.\
Output is a json file including pairs.\
Optional operation is merging with a larger json file containin pairs.
Example commands to run:\
```
# python3 findDefinitions.py -p pdfs/doc.pdf -jo abbreviations.json
# python3 findDefinitions.py -t pdfs/doc_Text.txt -jo abbreviations.json -ji abbreviationsList.json
```

