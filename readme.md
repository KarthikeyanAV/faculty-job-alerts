# Faculty Job Alerts

### About the project:
    - Checks jobs posted in FacultyPlus website under Arts and Science category every 24 hours.
    - Filters these jobs based on location - Tamilnadu, India
    - Sends e-mail to recipient if new jobs posted pass through the filter.

### Language - Python 3
### Libraries used:
    1. Requests
    2. BeautifulSoup 4
    3. smtplib
    4. Pandas
    5. os
    6. getpass
    7. email
    8. SSL
    9. time
    10. datetime

### How to use:
* Install necessary dependencies listed in *requirements.txt* file. 
* Open command prompt and type `python faculty_job_alerts.py`
* Enter gmail id  from which you want the alerts to be sent when asked for userid(I suggest you to not use your personal account). 
* Enter password when asked for - your typed password will not be shown on screen. 
* Enter recipient mail id.

### Output Snippings
![Mail Structure]("images/Mail_snipping.PNG" "Alert Mail Format")

Note:- The project is intended for educational purposes not for commercial use.