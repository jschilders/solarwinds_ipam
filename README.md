API access from Python for Solarwinds IP Address Manager (IPAM)

First release, incomplete (nonexistent) documentation.

It works, but could do with a lot more testing and some cleanup.


    For safety reasons, I choose not to load credentials from config files.
    Instead, I import them from the environment.

    Quick start:
        - Create a file called ".env" in the root of this project
        - put ".env" in your ".gitignore" file
        - Put something like this in there:
            SERVER = 'my-solarwinds-server.my-domain.com'
            USERNAME = 'my_api_user'
            PASSWORD = 'supersecretpassword'
        - test scripts will read these variables with "load_dotenv()" 
          and use them for authentication

The test scripts are your only form of documentation at the moment. 
