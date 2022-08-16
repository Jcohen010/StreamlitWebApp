# StreamlitWebApp
Web Application for Final Inspection Data Collection

![Header Image](https://www.sas.com/en_us/insights/big-data/what-is-big-data/_jcr_content/par/styledcontainer_335204280/image.img.jpg/1457718453446.jpg)

## The Problem
Throughout my time at my current company, I've invested a lot of energy into the transition away from paper forms as a method of internal data collection. The advantages of making the change to digital data capture are numerous:
* Improvement in data accuracy
* No lag time in potential analysis due to lack of need for manual entry
* Environmental friendliness
* Increased productivity due to no time wasted manually entering data
* Decrease in data redundancy
* Removes clutter typically accompanied by storing paper documents

*...and the list goes on*

One form in particular caught my eye as a perfect candidate for kicking off the transition away from paper data collection. It captures vital quality data which is utilized in giving stakeholders on the production team a clear idea of production performance, and also happens to steal much precious time from our quality engineer, who currently manually enters the collected data. 

## The Solution

### Plan A
I initially started searching for a third party form building application with a similar use case. One aspect of the candidate app was vital: the capability to loop a particular section/question an arbitrary amount of times, allowing inspectors to only have to enter header inpection information once, even if there ends up being several cases with defects. Furthermore, the JSON or .csv schema would have to match that of target table in the data warehouse.

*Example below:*

|jobID|itemID|customerID|datefound |inspectshift|inspectgluer|caseqty|defectcode|defsamples|totalsamples|
|-----|------|----------|----------|------------|------------|-------|----------|----------------|------------|
|4200 |7576|Test  |2022-08-10|1st Shift   |Machine 12    |1200   |F1        |12              |32          |
|4200 |7576|Test  |2022-08-10|1st Shift   |Machine 12    |1200   |F4        |1               |32          |
|4200 |7576|tes  |2022-08-10|1st Shift   |Machine 12    |1200   |L11       |2               |32          |


99% of the form building web apps I found were to basic to allow for the specific functionality that we required. Enter GoCanvas. They offered everything we needed: full customizability, pleasant GUI form builder, full integration capabilites, .pdf generation upon form submission; they even accomodated the looping section functionality we were seeking. Only issue: sky high pricing. My manager and I both knew upper management was unlikely to support the investment.

#### Plan B
I decided to build an app myself for the company. Using Streamlit, a web development environment based in python, I developed an app that could be run on the final inspectors' samsung tablets out on the production floor. Each submission routes captured data directly to the company's [data warehouse](https://github.com/Jcohen010/CompanyDW) staging area. 

## Resources

Tools
* Streamlit
* Visual Studio Code
* Postgresql
* Jupyter Notebooks

Languages
* Python
* SQL

## Features
There were a few key features that the Director of Quality and the inspection team were looking:
* Spanish/English Toggle
* Auto-Fill Sample Quantity depending on Case Quantity according to AQL sampling guidelines
* Local Hosting for increased security
* Ensured Accessability for all users


[App Preview](https://user-images.githubusercontent.com/104105293/184428035-28b63ce4-dc52-4d52-aee7-1a61603e2267.webm)
