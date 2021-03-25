import pandas as pd
import looker_sdk
from looker_sdk import models40

sdk = looker_sdk.init40("/your/ini/file/path/Looker.ini")

query = """select Name, Email From Fake_Users"""
 
create = sdk.create_sql_query(body=models40.SqlQueryCreate(connection_name="your_connection", sql=query)).slug
result = sdk.run_sql_query(slug=create, result_format="json")

df = pd.read_json(result)
df.head()

for i, row in df.iterrows():
    plan = models40.WriteScheduledPlan(name="Test Schedule: " + str(f"{row[0]}"), 
                                        run_as_recipient=False, 
                                        filters_string='?Employee+Name='+str(f"{row[0]}"), 
                                        dashboard_id=1, 
                                        crontab="0 5 * * *", 
                                        scheduled_plan_destination = [models40.ScheduledPlanDestination(format="csv_zip", 
                                                                                                        address=str(f"{row[1]}"), 
                                                                                                        type = "email")])
    schedule = sdk.create_scheduled_plan(body=plan)
     
