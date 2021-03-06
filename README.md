# 2019-kam-proj2-multi-search
Second project for Knowledge Analysis &amp; Management (2019)

### Documentation
 
For the general documentation run:

    python3 multi_search.py

For details about each command and instruction on "how to run", run:

    python3 multi_search.py <command> -h/--help
    
### Generated files
All the files generated by the software can be found in folder `res` (in project root).

### Arguments
By default the extraction of the data make use of project tensorflow (e.g in the `lib` folder) although since this folder is not uploaded to github you should provide your own path. Alternatively you can use this method without 
arguments by first creating the `lib` folder (in the project root) and move there the project to analyse.

### Examples usage:
The following are some example of commands:
1. **Data Extraction**
    - ```$ python3 multi_search.py extract_data --path <path>/tensorflow``` (The methods 1,2 search for file `res/data.csv` so you should run this command before)
2. **Train and run query**
    - ```$ python3 multi_search.py search_data --query "Some query" ```
3. **Evaluation and Visualization**
    - ```$ python3 multi_search.py prec_recall --ground_truth <path>/gt.txt```
