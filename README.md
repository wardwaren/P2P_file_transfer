# P2P Fil transfer application

### Description

This is a simple P2P file transfer application.

It contains server and client versions. 

Server is always on and keeps track of users that connect to it.
When clients connect they send folder with files that they want to share.
Server saves basic information of these files and user who put them.
Then client can search for files shared by other users with server and download them from these users.

Think Torrent but much much simpler.

### Execution:

To run server execute Server.py
To run client execute Client.py

Client is setup in a way that you need to provide it IP and Port of the server. 
Both of them are displayed in the logs of the Server.py (Port is set to 9999 and IP to IP of your device)

After you enter IP and Port you need to select a folder from which Server will look for files.
This is also the folder to which files you find will be downloaded.

Then you press "Connect" and connect to the server. If connection is successful you will be moved to the SEARCH page.
Enter the name of the file you are looking for without extension (e.g .txt) and press search.

If Server will find any files that match your file's name it will display them as a list.
Enter the index of the needed file and press download.

Then you will establish connection with the client who has these files and download from them.


P.S. Server won't find your own files, so to test server you will need at least 2 clients. 
In addition server won't find files of disconnected users so if you want to download file from other user
they must be currently connected to server.

