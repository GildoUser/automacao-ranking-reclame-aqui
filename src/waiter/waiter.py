from src.waiter.waiterDefs import WaiterSecDefs
import os

#is_regular = False
class Waiter:
    def __init__(self,data,web_hunter):
        self.is_regular = False
        self.waiter_sec = WaiterSecDefs(data,web_hunter,self.is_regular)

    def setInternTopicList(self,data):
        self.waiter_sec.setTopicList(data)

    def startService(self):
        self.waiter_sec.sayHello()
        while True:
            self.offerRegularOptions()                

    def offerRegularOptions(self):
        #ask question and expect a input as choice
        user_choice = self.waiter_sec.OfferMessage() #is regular = true
        topic_id = self.waiter_sec.serviceByDemand(user_choice)
        self.waiter_sec.listTopic(topic_id)

   # try:
           # with open("./")
    
