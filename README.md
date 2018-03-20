# MULTIROOM CHAT MS

keywords : chat, rooms, websockets, channels, django

Multiroom chat developed in Django 2.0.2
The app use [Channels 2.0](https://channels.readthedocs.io/en/latest/) with [channel-layer](https://channels.readthedocs.io/en/latest/topics/channel_layers.html) django-redis

## Socket Events
* Connection
  ```
  connect()
  ```
  Event triggered when a new Socket connects to the server. When it triggers it does the following sequence of events:
  * Get info sent in the connection URL
  * Add channel_name to GROUP_CHAT-{id}
  

* Disconnect
  ```
  disconnect()
  ```
  Event triggered when a socket disconnects from the server. When it triggers it does the following sequence of events:
  * Remove channel_name from GROUP_CHAT-{id}
  
  
* Receive
  ```
  receive_json
  ```
  Event triggered when a socket disconnects from the server. When it triggers it does the following sequence of events:
  * ask the category message.
  * send event to GROUP_CHAT-{id} 
  * if category == 'NEW-MESSAGE': Execute chat_message method.
  * if category == 'JOIN-ROOM': Execute chat_join method.
  
