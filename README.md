This is not a production project. It is just my final project for the Full Stack Foundations course from Udacity.
https://www.udacity.com/course/full-stack-foundations--ud088

There is no authentication, error handling or UX customization (so far...).

Instead of Vagrant I choose Github, Virtualenv and Pip, so if you want to try it out, follow these steps to setup the project on your machine:

1 - Clone the project to your local machine "git clone https://github.com/vmenezes/udacity-FullStackFoundations-finalProj.git"
2 - Move inside your new project folder and create a virtual environment "cd udacity-FullStackFoundations-finalProj; virtualenv env"
3 - Activate you just created virtual environment "source env/bin/activate"
4 - Install the the system requirements (flask and sqlalchemy) "pip install -r requirements.txt"
5 - Start the server on port 5000 "python src/finalProject.py"
6 - Open http://localhost:5000 on your web brownser and enjoy!

Victor Menezes

menezes.victor@gmail.com