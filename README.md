# CINS465-Shelley-Wong
This is a private repo for CINS465 created for Shelley Wong

Primary Project Deliverables:
* Chat Forum with real time updates
* Face/Name Match Game - list of students shown in random order, with 4 multiple
  choice options (including the correct option), and results (score, correct and
  incorrect answers) - different randomization each time
* User Profiles (extension of Django User) with profile pictures, "about" section,
  and image description options).

Additional Project Deliverables:
* User Profile components are required, but all components of Student Profile are
  optional to add during registration and may be added later (option to edit in
  student's personal profile)
* User Profile includes option to join non-admin group if the name of the group
  is known (currently have 2 groups set up: cins465students (non-admin) and
  professors (admin)) - only cins465students are in the name/face match game and
  team roster
* Team Roster allows users to view other user profiles (but they cannot edit
  other user profiles or see the groups that they are in)
* Message Board was created separate from chat room to so important posts about
  assignments, projects, announcements, etc can be viewed and commented on.
  Separate chat room is available for users to chat about whatever they want.
  Message Board includes a search bar, which currently has the ability to search
  Post and Comment subjects and details

Helpful Details:
* Groups:
  - 'professors' (admin, have permissions: active, staff status, superuser status)
  - 'cins465students' (non-admin)
* Users - username & password (a sample to allow you to see how everything works):
    Username      Password
  - shelleywong   csuchico (admin)
  - daria         janelane
  - morty         ricksanchez
  - porkchop      killertofu

References utilized in multiple locations: (additional references can be found
  near the adapted code associated with each reference)
1. https://www.youtube.com/watch?v=JmaxoPBvp1M , https://www.youtube.com/watch?v=D9Xd6jribFU
  * Used for Editing Profile code in these files:
    * edit_profile.html
    * views.py
    * urls.py

2. https://channels.readthedocs.io/en/latest/tutorial/index.html
  * Django Channels/Websockets tutorial for building a simple chatroom, referenced
    for the following:
    * chat/chatroom.html
    * js/chat.js
    * consumers.py
    * routing.py
    * urls.py
    * views.py

3. https://www.ploggingdev.com/2017/11/building-a-chat-room-using-django-channels/
  * Plogging Dev: Building a Chat Room Using Django Channels - creating a model to  correspond with chat room messages
    * models.py (Chat_Model)
    * consumers.py
