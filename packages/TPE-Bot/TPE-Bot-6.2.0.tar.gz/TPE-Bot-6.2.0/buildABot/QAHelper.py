import logging
from buildABot.QA.QAManager import QAManager
import os

logger = logging.getLogger()

class QAHelper:
    def main():
        qa = QAManager(qaFile = os.getenv('qaFile'), 
                       apiKey = os.getenv('OPENAI_APIKEY'))
        print("\n\nWelcome to TPEBot QA Helper! What would you like to do today?")
        print("===========================================================")

        print("\t 1) Create entire QA for me")
        print("\t 2) Fill in the responses for me")

        while True:
            try:
                option = int(input("Enter Option: "))
                print()

                if(option == 1):
                    try:
                        qa.createQA()
                    except Exception as e:
                        logger.exception("Exception Occured while code Execution: "+ str(e))

                elif(option ==2):
                    try:
                        qa.createResponse()
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
