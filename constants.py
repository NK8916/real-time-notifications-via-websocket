from enum import Enum

class NotificationCategory(Enum):
    MESSAGE="MESSAGE"
    SUBSCRIPTION_EXPIRY="SUBSCRIPTION_EXPIRY"
    PROFILE_SETUP="PROFILE_SETUP"

class NotificationTitle(Enum):
    NEW_MESSAGE_RECEIVED="New Message Received"
    SUBSCRIPTION_EXPIRING_SOON="Subscription Expiring Soon"
    PROFILE_SETUP_COMPLETE="Profile Setup Complete"