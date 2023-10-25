Our application is a simple interface that retrieves specific wine data from different store websites with webscraping technology.
For the Dashboard in which the user navigates and sees the results, we used streamlit framework.
We coded in Python to search and get the data and we've made use of a MySQL Database to store it and to redirect it to our Dashboard.

# team-9
## How to start!

First we need to go to the folder webscraping

    cd webscraping

and execute the command

    bash install_dependencies.sh

Then execute the script with this command

    python3 main.py

Go to the folder hack_dashboard

    cd ../hack_dashboard

Then execute streamlit with the Front End

    streamlit run hack_dashboard.py
