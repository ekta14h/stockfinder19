
This project is on creating a cherrypy web app. It displays top 10 stocks from the BSE link 
and also it has option to search for a stock by its name and get its corresponding details.

used Heroku to deploy my app. Few problems faced while deploying the code
  1) dyno scaling
  2) Redis server connection error
  3) was using quickstart(classname) in my equity_index.py so UI was not getting displayed(it was running on local server) so to rectify the problem used config file in the py and changed my ip to 0.0.0.0 and port 5000 and specified it in 
  quickstart(classname,'/', config)

What more I could have done:
  1) could have implemented sorting column wise to improve search
  2) could have applied partial search option in the Searchbox
