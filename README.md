# cposts-postcard-generator
An Application that convert .cpost files into .html and .png post card

# Dependencies

To work this application need "wkhtmltoimage".  
You can find it [here](https://wkhtmltopdf.org/downloads.html)

# How To Use ?

* Create an env.py file
* Write the variable : htmltoimage = "path/to/your/wkhtmltoimage/bin"
* Edit the template.cpost file (or make a new one and copy the template.cpost file format)  
* Run transpileur.py file
* Select your .cpost file
* Choose where to save your .html and .png files (./posts by default)
* Generate your card
