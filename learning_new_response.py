from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client['chatterbot-database']
products_colletcion = database.products

# Uncomment the following line to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        }
    ],

)

bot.set_trainer(ChatterBotCorpusTrainer)

bot.train("chatterbot.corpus.english")

CONVERSATION_ID = bot.storage.create_conversation()


unnecessary_words = ['to', 'i', "i'm", 'you', 'me', 'yours', 'they', 'be', 'can', 'should',
                     'are', 'is', 'in', 'the', 'of']


def get_feedback():
    from chatterbot.utils import input_function

    text = input_function()

    if 'yes' in text.lower():
        return False
    elif 'no' in text.lower():
        return True
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()

def getProductsOnSale():
    product = products_colletcion.find({"onSale": True},{"product":1,"_id":0}).limit(5).sort('qty',-1)
    for item in getProductsOnSale():
        print(item['product'])

print("Hi")
print("How can i help you ?")

# The following loop will execute each time the user enters input
while True:
    try:
        input_statement = bot.input.process_input_statement()
        statement, response = bot.generate_response(input_statement, CONVERSATION_ID)

        if response.confidence > 0.6:
            if(response == "There are some products on sale"):
                bot.output.process_response(response)
                getProductsOnSale()
            else:
                bot.output.process_response(response)
        else:

            print("Sorry, I'm too young to understand this ...")
            var = int(input("Press 1 to products on sale\nPress 2 to products in stock\nPress 3 to product location\n"))

            if(var==1):
                bot.set_trainer(ListTrainer)

                bot.train([
                    str(statement),
                    'There are some products on sale',
                ])

                bot.set_trainer(ChatterBotCorpusTrainer)

                print("There are some products on sale")
                getProductsOnSale()

            elif(var==2):
                print()

            elif(var==3):
                print()

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

