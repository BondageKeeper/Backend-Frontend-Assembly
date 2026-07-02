#Docker is simply necessary to put into container(combine) all libraries and classes(Fastapi , SQLAlchemy) and so on
#we might presume that not all computers have python with all needed libraries and desired classes it means that if
#we try out our site using another computer without python and all tools we used it is logical that it won't work
#because there are no required tools on this device
#so docker unites all our tools into and puts them into isolated-container which will open on any device , on any server
#METHODS:
#Dockerfile - this is an instruction for another device like 'install python , copy main.py or crud.py etc..)
#Image(it is binary) - it is prepared closed box which was assembled according to Dockerfile(instruction)
#Container - this is a working pattern(box) - used when we open RAM
#MOST IMPORTANT COMMANDS:
#1)docker build: it translates our Dockerfile into binary Image
#docker build -t pcbang_app . (-t is a flag tag(to create name) and pcbang_app is this name btw)
#. IS COMPULSORY(mean: look for in dockerfile right in the current folder(otherwise it docker won't search in our current folder)
#2)docker run  -  it takes our pcbang_app and launches it inside FastAPI
#how to write it : docker run -p 8080:8080 --name my_club_container pcbang_app
#-p ties up port of our computer(8080) with port of built container(it is btw also 8080) - here we turn our image into a container
#3)docker ps - prints out on the screen the list of all containers which work right now in RAM of the computer(or laptop)
#ps by the way means process status it will show some configs of container : id , name
#if we add -a(all)(docker ps -a)  it will show all containers
