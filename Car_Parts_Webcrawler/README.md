Car part webcrawler. 
This is the Hollander module. This has been upgraded and slimmed down by removing classes that did not accomplish the functions for the hollander module.
This webcrawler has 3 primary goals. 
Goal 1) scrape information from all car parts websites
Goal 2) Match that information to all parts to a car based upon year, make, and model
Goal 3) Create a map that shows where all the parts are geographically located
Goal 4) Color code the parts based upon their function. E.g. Yellow for electrical components, 
    Red for cosmetic, blue for fluid management, etc.

Note: in the future to reduce amount of retries it will be wise to write the html to a text file and 
then read from that page for experimentation

URL Example:hollanderparts.com/used-auto-parts/Year/Make/Model/Category /Part Type      /Fitment
https://www.hollanderparts.com/used-auto-parts/2007/honda/crv/electrical/601-alternator/601-50108-get-parts