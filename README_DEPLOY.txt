COFFEE SALES STREAMLIT DASHBOARD (SQLite edition)

Files to upload to the root of your GitHub repository:
- app.py
- coffee_sales.db
- requirements.txt

Streamlit Community Cloud setup:
1. Push these three files to your GitHub repository.
2. In Streamlit Community Cloud, choose the repository and branch.
3. Set the Main file path to app.py and deploy.

Database note:
This version uses the included SQLite file. View/Add/Update/Delete operate on
that file while the app process is running. Streamlit Community Cloud does not
provide durable writable local disk for this use case: edits may disappear when
the app restarts, sleeps, or is redeployed. Do not treat this as permanent
production storage. For durable online CRUD, connect a persistent hosted
database or storage service.

The database was created from the supplied MySQL dump. Tables imported:
raw_sales and sales_transactions; category_summary view recreated in SQLite.
