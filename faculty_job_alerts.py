# faculty_job_alerts.py

"""This is the entry point for the project"""
import os
import getpass
import time
import datetime
import Faculty_Jobs.scrape_site as spr
import Faculty_Jobs.manipulate_dataset as md
import Faculty_Jobs.send_alerts as alert


# Logging on to server
sender_email = input("Enter User Id:")
sender_pass = getpass.getpass(prompt="Enter Password:")
recp_name = input("Type Receiver Name:")
recp_email = input("Type Receiver Mail Id:")

mail_obj = alert.Email(user_id=sender_email,
                       password=sender_pass,
                       recipient_address=recp_email,
                       recipient_name=recp_name
                       )
while True:
    status = mail_obj.login_server()
    if status:
        # Scrapping site
        page = spr.url_builder("jobs-by-location", "tamilnadu")
        spr.create_dataset(page, "jobs_by_loc.tsv")
        time.sleep(3)
        page = spr.url_builder("arts-and-science")
        spr.create_dataset(page, "jobs_by_category.tsv")

        # creating dataset
        dataset = md.read_datasets()
        result = md.find_intersection(dataset)
        os.remove("jobs_by_loc.tsv")
        os.remove("jobs_by_category.tsv")

        if not result.empty:
            res_count = len(result.index)
            df1 = result.assign(Result=list(range(1, res_count+1)))
            text_1 = df1.to_string(columns=["Result", "Page Link"], index=False)
            html_1 = df1.to_html(columns=["Result", "Page Link"], index=False, justify="center")

            # Composing email
            subject = "Job Alert!"
            mail_obj.subject = subject

            # sending mail
            mail_obj.mail_props()
            mail_obj.compose_email(res_count, text_1, html_1)
            mail_obj.send_email()
            mail_obj.close_server()
            print(f"{res_count} results found. Mail sent on {datetime.date.today()}")

        else:
            print(f"zero results found. Mail not sent on {datetime.date.today()}")

        time.sleep(24*60*60-3)

    else:
        print("Invalid UserName/Password")
        break
