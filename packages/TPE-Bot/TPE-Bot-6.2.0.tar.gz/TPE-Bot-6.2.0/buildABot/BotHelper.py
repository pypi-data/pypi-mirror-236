import logging
from buildABot.Bot.BotManager import BotManager
import os
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv('./.env')

class BotHelper:
    def main():
        chatbot = BotManager(#qaFile = os.getenv('qaFile'),
                        #slFile = os.getenv('slFile'),
                        #studentFile = os.getenv('studentFile'),
                        inputFile = os.getenv('inputFile'),
                        resultFile = os.getenv('resultFile'),
                        keyFile = os.getenv('keyFile'))
    
    
        logger = logging.getLogger()
        print("\n\nWelcome to TPEduBot Package! What would you like to do today?")
        print("===========================================================")

        print("< Learn & Explore Chatbot >")
        print("\t 1) Create/Re-build Chatbot")
        print("\t 2) Update Intents")
        print("\t 3) Update Worksheets / Hot Topics")
        print("\t 4) Transform to Recommended Menu with Assessment Rubrics & Results")
        print("\t 5) Change of Student Access")
        print("\t 6) Retrieve Telebot Info and Create Dashboard from Logs")

        print()

        print("< Learn & Explore with Recommended Menu Chatbot >")
        print("\t 7) Create/Re-build Chatbot")
        print("\t 8) Update Intents")
        print("\t 9) Update Worksheets / Hot Topics")
        print("\t 10) Add Latest Results")
        print("\t 11) Change of Student Access")
        print("\t 12) Retrieve Telebot Info and Create Dashboard from Logs")

        while True:
            try:
                option = int(input("Enter Option: "))
                print()

                if(option == 1):
                    try:
                        chatbot.createLearnChatbot()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif(option ==2):
                    try:
                        chatbot.updateLearnIntents()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif (option == 3) :
                    try:
                        chatbot.updateLearnLatestWorksheets()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif (option == 4 or option == 10):
                    try:
                        chatbot.addNewResults()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif (option == 5):
                    try:
                        chatbot.updateLearnEntities()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif (option == 6 or option == 12):
                    try:
                        chatbot.createAnalytics()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif(option ==7):
                    try:
                        chatbot.createLearnAndRecoChatbot()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))
                
                elif(option ==8):
                    try:
                        chatbot.updateRecoIntents()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif (option == 9) :
                    try:
                        chatbot.updateRecoLatestWorksheets()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif (option == 11):
                    try:
                        chatbot.updateRecoEntities()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                else:
                    print("Invalid Input, please try again...")
                    continue
                

            except ValueError:
                print("Sorry, I didn't understand that.")
                continue
            
            else:
                break

    if __name__ == "__main__":
        main()
            
        
    




