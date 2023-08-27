# real-time-notifications-via-websocket

## endpoint for websocket:- ws://127.0.0.1:8000/trigger_event
## message payload allowed for each categories:- 
 * MESSAGE:  {"title":"New Message Received","category":"MESSAGE","description":"testing"}
 * SUBSCRIPTION_EXPIRY: {"title":"Subscription Expiring Soon","category":"SUBSCRIPTION_EXPIRY","description":"2023-11-01"}
 * PROFILE_SETUP: {"title":"Profile Setup Complete","category":"PROFILE_SETUP"}