# Payment network data: AID and fake PAN numbers
import random

from StringUtily import EntryMode


TestCard = [
    {
        "Network": "VISA",
        "AID": "A0000000031010",
        "PAN": "4761739001010119",  # User-specified Visa number
        "AppName": "VISA Credit",
       
    },
    {
        "Network": "MC",
        "AID": "A0000000041010",
        "PAN": "5419330089604111",  # 16 digits, starts with 5
        "AppName": "MasterCard Credit",
       
    },
    {
        "Network": "DISCOVER",
        "AID": "A0000001523010",
        "PAN": "6011601160116611",  # 16 digits, starts with 6011
        "AppName": "Discover",
       
    },
    {
        "Network": "JCB",
        "AID": "A0000000651010",
        "PAN": "3569990010095841",  # 16 digits, starts with 35
        "AppName": "JCB",
        
    },
    {
        "Network": "AMEX",
        "AID": "A00000002501",
        "PAN": "373953189371007",  # 15 digits, starts with 34 or 37
        "AppName": "American Express",
    }
    
]

# Randomly select a card from the list
def get_random_card():
    return random.choice(TestCard)

# Get mask PAN number
def get_masked_pan(card):
    return f"{'*' * 12}{card['PAN'][-4:]}"

# Get card type
def get_card_type(card):
    return card['Network']

# Get AID number
def get_aid_number(card):
    return card['AID']
    
# Get application name
def get_app_name(card):
    return card['AppName']

# main function
if __name__ == "__main__":
    card = get_random_card()
    print(f"Network: {card['Network']}")
    print(f"AID: {card['AID']}")
    print(f"PAN: {card['PAN']}")