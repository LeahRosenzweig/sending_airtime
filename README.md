# Sending airtime to survey respondents in Kenya and Nigeria
This repository provides instructions and code for sending an SMS and airtime to people using the [Africa's Talking](https://africastalking.com/) API. The sample provided sends an SMS and airtime to survey respondents in Kenya and Nigeria, but could easily be adapted for any other country in which Africa's Talking operates.


Steps to follow:
1. Register for an Africa's Talking account [here](https://account.africastalking.com/auth/register/) and create an app for whatever country in which you want to send people an SMS/airtime. *Note:* In some countries you will need to register and pay for a sender ID to send messages (we needed to do this for Kenya -- see more information [here](https://help.africastalking.com/en/articles/407085-how-do-i-set-up-my-sender-id-in-kenya-or-uganda)). 
2. Editing the files. The .env file is a sample. You will need to edit this document to include your own API keys and sender ID from Africa's Talking. Currently the file is running a sandbox environment (testing - see [here](https://help.africastalking.com/en/articles/2189460-what-are-the-sandbox-and-the-live-environments)) but to run for production (actually send SMS/airtime) you can follow these instructions [here](https://developers.africastalking.com/docs/authentication).  In addition to the files provided here you will also need to create and save locally a serviceAccount.json that has your google permissions and provides access to your google sheet where the respondents phone numbers are stored. See more information about how to do this [here](https://python.plainenglish.io/master-google-sheets-api-in-python-cheat-sheet-3535e86fbe17).
3. Finally, to automate payment you can host the code provided on [heroku](https://www.heroku.com/) and set up scheduler that runs daily. The python code provided pays respondents who completed the survey the previous calendar day. See instructions for how to do that [here](https://dev.to/towernter/hosting-a-python-script-on-heroku-using-github-khj).

Helpful links:
- https://github.com/AfricasTalkingLtd/africastalking-python
- https://developers.africastalking.com/
