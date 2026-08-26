# Cards-Hub
## Introduction:
This site is the most successful project ,because I practiced frontend-part a lot and came to conclusion that I should learn more about JavaScrpt and HTML. 
Also, I integrated API(Artificial Intelligence) and this skill is very important nowadays because lots of modern websites integrate a lot of API's. 
And in my opinion I made pretty cool interface with four main tabs, moreover I added `https` domain finally for security reasons.
In summary I really enjoyed doing this project and final view of the project makes me happy.

## Here are all screens of tabs:

### 📷 Registration window:
<img width="1919" height="925" alt="Registration_window(sign-up)" src="https://github.com/user-attachments/assets/87ae3f34-ba84-4e68-82d8-45c78a52dcc5" />
Here user can create a completely new account or can sign in the "old" account or if user can't recall password - he or she can easily restore it by 
writing only their email where they get a new recovery-password.These all things related to Registration window in my project.

### 📷 Request window:
<img width="1919" height="917" alt="request_window" src="https://github.com/user-attachments/assets/ca687970-47f9-4a70-b721-6feca01b34cb" />
In this `textarea` user writes a topic,question,problem,etc and presses button 'generate' which immediately launches a request to AI API(I used Google).
After API gave us a response which is divided into steps - these steps go to 'Dashboard' . User can easily clean text in 'textarea' by pressing 'clean' .
Also, user can choose amount of steps from 2 to 5 and this amount of steps will turn into amount of unique cards in 'Dashboard' panel.

### 📷 Dashboard window:
<img width="1919" height="905" alt="dashboard_window" src="https://github.com/user-attachments/assets/d8898c9a-3e2b-4fa0-89a3-d050e7108edd" />
Here user get those cards and can drag them from one table to another if he completed(or didn't complete) tasks in the cards,it's possible to drag them
in any sequence. If user wants to keep these cards in database - he or she just should press 'Save' button and every card will be saved successfully.
If user wants to delete these cards - he or she just should press 'Delete' button and any data of these cards will be deleted from screen and database.

### 📷 Settings window:
<img width="1919" height="887" alt="security_window" src="https://github.com/user-attachments/assets/a6d52ef0-0230-4b58-9a92-e934267d0dc5" />
This window seems pretty empty but there are all important things like email and nickname that were registered. As you can see user can effortlessly
change old password or recovery-password in 'textarea' and log out any time he or she wants or needs.

## 📷 Here is a short video-review of my website:
<img width="1920" height="910" alt="main_record" src="https://github.com/user-attachments/assets/e139138c-1230-4099-b8c8-1f65a409a48c" />

## 🛠️ Used tools(crucial libraries) - I should definitely point it out:
* **FastAPI**
* **Pydantic**
* **SQLAlchemy**
* **CORSMiddleware**
* **Regex(re)**
* **Bcrypt** -> to hash the password of user for security reasons
* **Faker** -> to create a recovery-password due to method `fake.bothify(text='')`
* **Smtplib** -> to connect with the server of Google or Yandex
 
## ⚡ Key Features:
* **Password Recovery**
* **Password Hashing**
* **Password Estimation**
* **Draggable Cards**
* **Modern Interface**
* **Chosen Cards Amount**

## 🎯 Conclusion:
I think this project can be in some way useful because user can immediately get a plan how to cook,repair,study,understand,make particular things,
moreover this plan divided into cards and by dragging this cards user can monitor his or her progress which is kind of convenient. I hope this project 
will attract some attention and make my github better.

## 🌐 Website domain:
`https://cards-hub.website` -> it can run some days or not because I don't pay in advance a lot, so sometimes it can be off.



