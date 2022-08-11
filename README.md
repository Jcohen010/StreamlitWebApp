# StreamlitWebApp
Web Application for Final Inspection Data Collectiom

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

Initially, I searched for third party applications that had use cases similar to ours. We had one particular requirment that needed to be met, the ability to loop through a section of the form an arbitrary number of times and produce a dataframe in which the header information for the inpection was repeated for each iteration of the looped section. 

*Example below:*

|jobID|itemID|customerID|datefound |inspectshift|inspectgluer|caseqty|defectcode|defectivesamples|totalsamples|
|-----|------|----------|----------|------------|------------|-------|----------|----------------|------------|
|4200 |CPC000|Titleist  |2022-08-10|1st Shift   |Gluer 12    |1200   |P1        |12              |32          |
|4200 |CPC000|Titleist  |2022-08-10|1st Shift   |Gluer 12    |1200   |D4        |1               |32          |
|4200 |CPC000|Titleist  |2022-08-10|1st Shift   |Gluer 12    |1200   |G11       |2               |32          |

99% of form building applications I found were too basic to allow for this feature, except for an application called GoCanvas, a fully managed cloud form builder. It had everything we needed: a pleasant GUI on the form building side, cloud storage for collected data, integration capablities, built in analytics of submission activity and app usage; it even had the capability to generate templated pdf's upon form submission. When the price tag was revealed, I could sense my manager was doubtful that upper management would agree to the investment. 

I started developing a solution myself. Using Streamlit, a web app development environment based in python, I built an app that could be run on the final inspectors' samsung tablets out on the production floor. Each submission routes captured data in the digital form directly to the company's **[data warehouse](https://github.com/Jcohen010/CompanyDW) staging area. 

## Resources

Tools
* Streamlit
* Visual Studio Code
* Postgresql
* Jupyter Notebooks

Languages
* Python
* SQL

## App Preview
![App Preview](App Preview.mp4)