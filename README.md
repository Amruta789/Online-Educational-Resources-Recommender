# Online-Educational-Resources-Recommender
Based on keywords from course outline, lecturers can receive recommendations for web resources to be added to their course page.
There is also a specifically programmed search engine that gives only educational resources from Google based on keyword entered.

Installation Instructions:
1. Create a virtual environment in python (https://docs.python.org/3/library/venv.html) and install all modules using `pip install -r requirements.txt`
2. Elasticsearch must be installed within the system (https://www.elastic.co/downloads/elasticsearch) and follow the instructions to start elasticsearch. Elasticsearch is used for the search courses in navbar feature.
3. Create a directory called 'instance' in the root directory with another folder 'uploads' in it. The databases will also be stored in instance folder.
4. Create a .env file in the root directory with the following variables, `FLASK_APP=TeachAid`, `FLASK_ENV=development`, `ELASTICSEARCH_URL=http://localhost:9200` or any elasticsearch URL you have configured.
5. For the reset password email system to work, the following environmental variables need to be configured:
    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD
    If you want to send the reset password link via a real email address use MAIL_SERVER=smtp.googlemail.com, MAIL_PORT=587, MAIL_USE_TLS=1, MAIL_USERNAME=your_email, MAIL_PASSWORD=your_password. Otherwise, configure only these two variables as:
    MAIL_SERVER=localhost, MAIL_PORT=8025. Then open another terminal in your virtual environment, type the command: 
    `python -m smtpd -n -c DebuggingServer localhost:8025`
    When you enter your email and request password reset, the message with the link will be displayed in the above terminal.
6. And most importantly, your Google API key, possibly from https://console.cloud.google.com/home/dashboard, must be stored in `GOOGLE_YOUTUBE_API_KEY` environment variable. This API key is necessary for displaying content recommendations and surfing for educational content. This API key lets you use Youtube Data API, and Custom Search Engine JSON API provided by Google. The Google API key is freely provided as long as you have a Google account.
7. Run the following commands:
    `flask db upgrade` to make the database migrations
    `flask run` to start the development server

Now you can login, create courses, modify courses, and learn courses. Login as multiple users and test the interface.
Here is the YouTube video where I made a short demo of some features: https://youtu.be/FgGLR-VEBYA

