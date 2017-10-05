# Part 2: The Bad and the Ugly

## Pre-requisite

* Use Firefox
* Use a text editor (*not* a text processor)
* Open a terminal
* Have Python3 installed  
  Steps suggested if Python3 is not installed on your computer, in a terminal:
	- Type `xcode-select --install` to install command line tools (basic development tools on Mac OS, such as a C compiler)
	- Then type `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"` to install [homebrew](https://brew.sh/), a package manager
	- And finally type `brew install python3` to install Python3 using this package manager

## References 

### On standard Unix tools

* http://swcarpentry.github.io/shell-novice/
* http://matt.might.net/articles/sculpting-text/
* https://en.wikibooks.org/wiki/An_Awk_Primer
* http://swcarpentry.github.io/make-novice/

### On Python programming

* http://swcarpentry.github.io/python-novice-inflammation/
* https://www.crummy.com/software/BeautifulSoup

### On writting / understanding html documents

* https://openclassrooms.com/courses/build-your-website-with-html5-and-css3
* https://www.w3schools.com/html/

## Google scholar: extract number of citations from an author page

Go to your google scholar (or someone else's) profile (eg https://scholar.google.ch/citations?user=vlAoH8AAAAAJ&hl=en). If it is your profile, you can download a csv with a list of publications (select some articles and an "export" button will appear).  

Good... but the number of citations of each article is not present in the csv while it is displayed on the webpage.  

What can we do?

Firefox (or any browser) is *rendering* a website. We need to see the source (html code)! For this you can:
* Save the webpage with Firefox (CMD + s) and open it with a text editor
* Use the "view source" option in Firefox (CMD + u)
* Download the webpage with wget or curl and open it with a text editor
* If doing this within a program, use built-in libraries, eg urllib for Python
* For exploring and understanding the struture, the best is Firefox developper tools (CMD + ALT + c): permit to view the source and the rendered page at the same time

The structure is easy to understand. Basic knowledge of html helps but is not strictly required. Usefull ressources on html are listed in the "References" section.

How can we parse Google Scholar html code and extract the relevant information (number of citations for each article)?

Beautiful Soup is a python library to parse html files. It can be installed with a command like `pip3 install bs4` or `pip3 install --user bs4`.

Let's launch Python in a terminal and start experimenting! Let's also open a text editor to write a full Python script.

* First attempt: `./gs0.py "https://scholar.google.ch/citations?user=YILsNPMAAAAJ&hl=en"`

  Only get the first 20 citations, why?  
  Look in webinspector and find the &pagesize parameter (in Network, after clicking "show more"). Add &pagesize=xxx to the URL, trying manually a few different values -> we can get more citations!

* Second attempt: `./gs1.py "https://scholar.google.ch/citations?user=YILsNPMAAAAJ&hl=en"`

  Now gets all citations! But does it work with a longer profile?  
  No! `./gs1.py "https://scholar.google.ch/citations?user=L_JGehAAAAAJ&hl=en"` does only grab the first 100 citations even with "pagesize=200"  
  Go back to webinspector and find the &cstart parameter: the only way to have the full webpage is to request several pages with "cstart=0", "cstart=100", "cstrat=200"... (and always "pagesize=100")  

* Third attempt: `./gs2.py "https://scholar.google.ch/citations?user=L_JGehAAAAAJ&hl=en"`

  Works as expected! Now how to analyze this stuff? The script is slightly modify to produce a csv file if second argument is "csv".
  It is good practice to save the results into a local file so we don't query the server each time! Something like `./gs2.py "https://scholar.google.ch/citations?user=L_JGehAAAAAJ&hl=en" csv > sebastian.csv`

* Now let's analyse the output to do something "usefull"! For example, let's compute h-index:  

  ```
  cat sebastian.csv |cut -d ';' -f 2 |sort -nr |uniq -c |awk '{cumsum += $1; if (cumsum <= $2) print cumsum,$2 }' |tail -n 1 |cut -d ' ' -f 1
  ```

  Add a very basic management of errors to test more complex profiles:  
	
  ```
  ./gs3.py "https://scholar.google.com/citations?user=0A_lO2UAAAAJ" csv > derrida.csv
  cat derrida.csv |cut -d ';' -f 2 |sort -nr |uniq -c |awk '{cumsum += $1; if (cumsum <= $2) print cumsum,$2 }' |tail -n 1 |cut -d ' ' -f 1
  ````


## EcoliTox: submit stuff to a server (with useless authentification)

EcoliTox, available on https://absynth.issb.genopole.fr/Bioinformatics/, is an implementation of an algorithm predicting toxicity for E. coli of a biological compound based on its molecular structure.  

Log in EcoliTox: you can create an account or just use mine (``bebopalula@caramail.com`` with password ``PizzaWinePasta``). From the home page of the absynth server, choose EcoliTox (3rd item of the retrosynthesis line). Paste the content of a [Molfile](https://en.wikipedia.org/wiki/Chemical_table_file#Molfile), which is a standard file format to describe a chemical structure, in the input window. For example use [this one](http://www.genome.jp/dbget-bin/www_bget?-f+m+compound+C00022), or search for another Mol file on [KEGG](http://www.genome.jp/kegg/kegg2.html) (search any compound by name). Press submit. After a few seconds we get a webpage with numerical result, IC50 in g/l. How can we automate the submission of many Molfiles to this webserver? 

We can first inspect the source of the submission web page (and not the results web page) in Firefox web developper tools (CMD + ALT + c). We see that everything happens in another included webpage, https://absynth.issb.genopole.fr/Bioinformatics/tools/EcoliTox/EcoliTox.php. Let's open this address. From there, the relevant information in the source is action="process.php". To understand how it works, we can paste a Molfile and press submit again, with the developper tools open. Then go to the "Network" tab, click on the line related to "process.php" and observe the "Params" and "Cookies" sub-tabs. We now have all the informations needed to write a Python script sending the exact same request to the server!

`./et.py C00022` sends the content of the file C00022 the same way than if we copy/paste its content and press submit. It returns a webpage (html document) that contains the information we are interested in (IC50). We could parse the webpage with BeautifulSoup again to extract this information, but the structure of the webpage is so simple that we don't need this! The relevant information is between `<pre>` and `</pre>` tags, so "sed" (standard unix tool) is sufficient:

```
./et.py C00022 |sed 's/.*<pre>\(.*\)\\n<\/pre>.*/\1/g'
```

Note: we did not use the autentification Cookie. This is because the Login system is very poorly implemented. The Python script et.py contains commented lines showing how we would have dealt with a correctly implemented Login system.

## Getting PDF files for all articles published by Nature in 2016

Let's try to find all the articles (research articles and letters) published by Nature in 2016! If we are within ETH network (or [using a VPN](https://www.ethz.ch/services/en/it-services/catalogue/networks-connections/remote.html)), we can download all the PDF files. Otherwise we can still do interesting parsing (such as extracting titles, authors, doi, ...).

We need to parse the page http://www.nature.com/nature/archive/index.html?year=2016, follow the links to each issue, and parse the page behind all of these links!

`./nature.py` will do this, finding the link toward the page of each research article or letter, and download the matching PDF file.

We use the same technique and tools than in the google scholar example, however the parsing is more complex: we must first parse the webpage listing all 2016 issues, and then parse the webpage of each issue separatly. 

