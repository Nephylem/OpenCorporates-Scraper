I already fixed those confusing logs. Here's what this script do when you execute run.py file: 

1.) It will initialize the drivers and at the same time sign in the account. Each driver will represent 1 thread and 1 account. For this script, we have 10 accounts so meaning there will be 10 threads/workers. You can adjust the maximum workers in config.py file by adding an account or removing an existing account by commenting the lines. (I set the proxy global for all of the accounts you will see it in config.py file)


2.) Run search for all the terms given in terms.txt file. For example, you added a 100 terms and 10 threads to work with the search. What it does is it splits the terms into 10 parts so that each thread will have 20 terms running search in the background. 

3.) Save the output to csv format. (Notice: It may have multiple output but what you need will be the last one written)