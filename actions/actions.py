# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re


class ValidateNewsletterForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_newsletter_form"
    
    def validate_email(
      self,
      slot_value: Any,
      dispatcher: CollectingDispatcher,
      tracker: Tracker,
      domain: DomainDict,
)   -> Dict[Text, Any]:
      """Validate the email address."""

      # You can use a simple regular expression to check if the email address has a valid format
      email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
      if re.match(email_pattern, slot_value):
          return {"email": slot_value}
      else:
          dispatcher.utter_message(text="The email address is not valid. Please enter a valid email address.")
          return {"email": None}

   
    
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        email = tracker.get_slot("email")

        # Save the data to a file (e.g., CSV)
        with open('newsletter_user_data.csv', 'a') as file:
            file.write(f"{email}\n")

        # Display a message to the user
        dispatcher.utter_message(response="utter_subscribed")

        # Reset slot email to None after successful form submission
        return [SlotSet("email", None)]




class ValidateContactUsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_contact_us_form"
    

    def validate_name(
          self,
          slot_value: Any,
          dispatcher: CollectingDispatcher,
          tracker: Tracker,
          domain: DomainDict,
    )   -> Dict[Text, Any]:
          """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
          print(f"name given = {slot_value} length = {len(slot_value)}")
          if len(slot_value) <= 2:
              dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
              return {"name": None}
          else:
              return {"name": slot_value}

        #   name_entity = tracker.latest_message.get("entities", [])
    
        #   if not name_entity:
        #     dispatcher.utter_message(text="Please provide a valid name.")
        #     return {"name": None}

        #   # Extract the name entity value
        #   name_value = name_entity["value"]

        #   # provide some examples of valid names to help the model learn
        #   valid_names = ["John Smith", "Jane Doe", "Alex Kim"]
        #   if name_value.lower() not in [name.lower() for name in valid_names]:
        #       dispatcher.utter_message(text="We don't recognize this name. Please provide a valid name.")
        #       return {"name": None}

        #   return {"name": name_value}
    
    

    def validate_message(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validate `message` slot value."""
        
        if not slot_value:
            dispatcher.utter_message(response="utter_ask_message")
            return {"message": None}
        return {"message": slot_value}
    

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        message = tracker.get_slot("message")

        # Save the data to a file (e.g., CSV)
        with open('contact_us_user_data.csv', 'a') as file:
            file.write(f"{name}, {email}, {message} \n")

        # Display a message to the user
        dispatcher.utter_message(f"Thank you, {name}! We have received your message. We will get back to you at {email} as soon as possible.")

      
        return []
    


#
# class SubmitNewsletterForm(Action):
#     def name(self) -> Text:
#         return "action_submit_newsletter"
    
#     def submit(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict]:

#         # name = tracker.get_slot("name")
#         email = tracker.get_slot("email")

#         # Save the data to a file (e.g., CSV)
#         with open('user_data.csv', 'a') as file:
#             file.write(f"{email}\n")

#         # Display a message to the user
#         dispatcher.utter_message(response="utter_subscribed")

#         # Reset slots to None after successful form submission
#         return []
#         # return [SlotSet("name", None), SlotSet("email", None)]