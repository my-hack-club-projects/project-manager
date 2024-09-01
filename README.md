# project-manager
*This project is not completely finished yet. Development-related things, such as an easier deploy script or Dockerization are missing. The application itself is in a good enough MVP state to be usable, though!*

# about
This is a simple TODO app. It consists of two main components - **milestones** and **tasks**. A milestone can have as many tasks as you need. Once all tasks inside it are completed, the milestone is marked as finished and can't be edited anymore.
It is meant to be released and hosted one day, so it supports things such as logging in with a Google account - for that, you'll need to add your API key to the settings.py file, but if you don't need that functionality and just wanna use it for yourself, it is not required.

![image](https://github.com/user-attachments/assets/4ba3cc07-d4d2-4244-9067-9b2929618423)
![image](https://github.com/user-attachments/assets/e01cd13c-e30b-4ba1-8aec-35761a80f27c)
![image](https://github.com/user-attachments/assets/ce36b5e8-30ba-46dd-827d-92173f3b7d08)


# installation, usage
1. Clone this repository
2. Run `pip install -r pip-requirements.txt` in the root of the repository.
3. In the `frontend` directory, run `npm install`.
4. To run the app, run the `deploy.sh` script in the `backend` directory. This is just a very simple bash script that builds the frontend, applies migrations to the DB and then runs the backend. If you can't run the script (for example if you're on Windows for some reason), read it and execute the commands manually.
5. This will run the server on localhost:8000 by default. Navigate there in your web browser and you're done!
