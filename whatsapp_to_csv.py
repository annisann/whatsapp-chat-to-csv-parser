import re
import pandas as pd
import os
import sys

def get_date(message):
    """ This function is to get the date ONLY, doesn't include the time.
    
        Explanation:
        pattern1: [dd/MM/YY HH.MM.SS] Sender: Messages
                  [dd/MM/YY HH.MM.SS AM/PM] Sender: Messages
        pattern2: MM/dd/YY, HH:MM - Sender: Messages
                  MM/dd/YY, HH:MM AM/PM - Sender: Messages
        pattern3: dd/MM/YY HH.MM - Sender: Messages
        pattern4: dd/MM/YYYY HH.MM - Sender: Messages            # haven't met this pattern
    """
    pattern1 = r'\[(\d{1,2})\/(\d{1,2})\/(\d{1,2}) (\d{1,2})\.(\d{1,2})\.(\d{1,2})?( AM|PM)?\]'
    pattern2 = r'(\d{1,2})\/(\d{1,2})\/(\d{0,2})\, (\d{0,2}):(\d{1,2})( [A|P]M)? -'
    pattern3 = r'(\d{1,2})\/(\d{1,2})\/(\d{1,2}) (\d{1,2})\.(\d{1,2})'
    pattern4 = r'(\d{1,2})\/(\d{1,2})\/(\d{1,4}) (\d{1,2})\.(\d{1,2})'
    
    result1 = re.findall(pattern1, message)
    result2 = re.findall(pattern2, message)
    result3 = re.findall(pattern3, message)
    result4 = re.findall(pattern4, message)
    
    date = []
    if result1:
        for result in result1:
            date.append(result[0]+'/'+result[1]+'/'+result[2])
    elif result2:
        for result in result2:
            date.append(result[1]+'/'+result[0]+'/'+result[2])
    elif result3:
        for result in result3:
            date.append(result[0]+'/'+result[1]+'/'+result[2])
    elif result4:
        for result in result4:
            date.append(result[0]+'/'+result[1]+'/'+result[2])
    else:
        print("No pattern detected.")
    return date
    
def get_sender(message):
    """ This function is to get the sender from messages.
    
        patternNo where the sender is a phone number (contact hasn't been saved)
        patternNa where the sender is a name
    """
    patternNo = r'(\+[\d+\-\s].*):'
    patternNa = r'[\]|\-] ?([\w\.].*):'

    resultNo = re.findall(patternNo, message)
    resultNa = re.findall(patternNa, message)
    
    if resultNo:
        return resultNo
    elif resultNa:
        return resultNa

def get_messages(message):
    """ This function is to get the messages!
        iOS and Android type is different.
    
    """
    pattern = r': ([\d\w\s\W][^\[\]]+)' # messages pattern for iOS
    
    RE_EMOJI = re.compile("(["
                          "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          "\U0001F300-\U0001F5FF"  # symbols & pictographs
                          "\U0001F600-\U0001F64F"  # emoticons
                          "\U0001F680-\U0001F6FF"  # transport & map symbols
                          "\U0001F700-\U0001F77F"  # alchemical symbols
                          "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                          "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                          "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                          "\U0001FA00-\U0001FA6F"  # Chess Symbols
                          "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                          "\U00002702-\U000027B0"  # Dingbats
                          "])")
    
    message = RE_EMOJI.sub(r'', message)
    
    # iOS
    if message.startswith('['):
        message = " ".join(message.split()) # remove excess line
        message = " ".join(message.split('\u200e')) # remove idk what this is xixi
        message = re.findall(pattern, message)
    
    # Android
    else:
        message = message.replace('\n', '')
        message = "".join(re.split('\\n?\d{1,2}\/\d{1,2}\/\d{1,2}, ', message))
        message = re.split(r'\d{1,2}:\d{1,2} [A|P]M - [\w\s]+: ', message)
        if '' in message:
            message.remove('') 
    return message
    
def create_df(message):
    """ Aggregate date, sender, and messages then create a Data Frame """
    date = get_date(message)
    sender = get_sender(message)
    messages = get_messages(message)
    df = pd.DataFrame(
            list(zip(date, sender, messages)),
            columns=['timestamp', 'sender', 'messages']
        )
    return df
 
def convert_to_csv(dataframe, messages):
    """ This function is to convert .txt files to .csv files.
        All files stored in dataset_csv/
    """
    path = 'dataset_csv/'
    
    if not os.path.exists(path):
        os.mkdir(path)
    
    file = 'dataset_csv/' + messages.replace('.txt', '.csv')
    dataframe.to_csv(file, index=False)
 
def main():
    files = os.listdir(os.getcwd()+'/dataset')
    messages_list = [file for file in files if file.endswith('.txt')]
    
    for messages in messages_list: 
        with open('dataset/' + messages, encoding='utf-8') as file:
            message = file.read()
            
            df = create_df(message)
            convert_to_csv(df, messages)

main()    
