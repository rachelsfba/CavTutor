JMeter Test Suite for CavTutor
==============

Usage:
--------------
1. Install Apache Jmeter
2. Load *.jmx test plan into Jmeter
3. Start test plan
4. Results stored in jmeter.log and results.log
5. Graphs obtained from Jmeter->Jmeter *_TEST->Graph Results
6. Summary obtained from Jmeter->Test Plan->Summary Report

Outline:
-------------
The test suite consists of three modules (Jmeter Thread groups) which step through some of the distinct functionalities of CavTutor. Each module represents a collection of user stories and so this also doubles as a crude from of end to end testing. Each scenario can be simulated concurrently a variable number of times (think multiple users doing the same thing at the same time) each offset a certain time period computed from a "ramp-up period" so as to not overload the server all at once. It is in this way that the scalability of our system is tested. Each modules and all its users (threads) are completed before the next module is started. This is important because the listing and search functionality should be tested after models have been saved to the db so the test isn't operating on fixture data alone (more realistic to have large db). The digitalocean_plan.jmx and localhost_plan.jmx were both tested using Jmeter and the results stored in two folders named similarly.

Modules & Protocol:
----------------
1. User Functionality (10 threads x 15 seconds ramp up) - this module aims to simulate a user registering, logging in, and then listing themselves as a tutor for a random course.


2. Listing Functionality (10 threads x 30 seconds ramp up) - this module tries to measure how well the web service responds to the listings of various models such as Users, Courses, Tutors and Tutees.

3. Search Functionality (10 threads x 40 seconds ramp up) - this final module aims to test the performance of our search implementation by querying the service four times; twice on a random string (which should not give any results), once on a fixed string "CS" known to produce results, and a final string equal to the first word of one of the courses (should give results but is randomly chosen for each thread, to test the robustness of the search).


Analysis:
-------------------
A comparison of the summary's reveals that localhost has marginally better throughput at 2.7 vs 2.6 requests per second both weighing in around 5.5 kb/sec. The average time for a requests was much high for digitalocean and so was the std. dev. which implies the prescence of slow outliers. It was confirming to see that the std. dev. for the randomly chosen course keyword was much higher than that of the determined "CS" keyword. Digital ocean had a min-max resp. time of (81,921) while localhost was bounded between (35,719). While the data seems to suggest that digitalocean ensues some performance hinderances this might not always be the case. When performing more strenuous load testing (not illustrated here but you can try on your own by decreasing the "ramp-up time", or increasing the number of threads), digitalocean seemed to handle requests smoother with smaller std. dev.



