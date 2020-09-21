# Selenium Practice Projects
![Selenium](https://imgur.com/2T3JRuf.png)
## Quora Helper ✍️

#### DISCLAIMER: *I am not liable for anything that happens to your account. Using bots of the sort might go against the policies of Quora and can get you banned. These were made purely for educational purposes.*

### Auto-Inviter

How to:<br>
- Provide how many questions to review
- No need to do anything else

Description:<br>
It scrolls the page down enough to load the required number of questions, just as a user would do, then extracts and sorts these questions. Invites the possible daily amonunt
of people to those questions which have less than 3 answers.

### Revenue-Ratio Checker | Keyword Extractor

How to:<br>
- No need to do anything

Description:<br>
It checks the ratio of views and adsense of high-earning questions and if the ratio is 2:1 or better it will extract relevant keywords from those questions. It will save all the info to a .TXT file in the format of:<br>
`question | ratio | [keyword_1, keyword_2, ...]`

## Manic Clicker 🖱

How to:<br>
- Add the full path to your webdriver
- Add the site link you want your clicks on
- Add the ID of the DOM element you want clicked
- Provide your click-count

Description:<br>
It opens a new session, wait a few seconds then starts double clicking the element you provided.
A good site to try it on might be [Cookie Clicker](http://orteil.dashnet.org/cookieclicker/), which is a fun time waster.

## General Requirements 📋

- Python
- IDE

[Python](https://www.python.org/downloads/)<br>

If you are using Sublime Text as your IDE, consider the Terminus package as ST itself is not interactive.

[Terminus](https://packagecontrol.io/packages/Terminus)<br>
[How To Install Sublime Text Packages](https://packagecontrol.io/installation)

You could also create an executable from the python script using either [py2exe](http://www.py2exe.org/) or the [auto-py-to-exe](https://dev.to/eshleron/how-to-convert-py-to-exe-step-by-step-guide-3cfi).

## Misc.

For less hassle, I am using Sublime Text for these.
