{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 217,
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "import pandas as pd\n",
    "import os\n",
    "import sys"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 265,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_date(message):\n",
    "    \"\"\" This function is to get the date ONLY, doesn't include the time.\n",
    "    \n",
    "        Explanation:\n",
    "        pattern1: [dd/MM/YY HH.MM.SS] Sender: Messages\n",
    "                  [dd/MM/YY HH.MM.SS AM/PM] Sender: Messages\n",
    "        pattern2: dd/MM/YY, HH:MM - Sender: Messages\n",
    "                  dd/MM/YY, HH:MM AM/PM - Sender: Messages\n",
    "        pattern3: dd/MM/YY HH.MM - Sender: Messages\n",
    "        pattern4: dd/MM/YYYY HH.MM - Sender: Messages\n",
    "    \"\"\"\n",
    "    pattern1 = r'\\[(\\d{1,2})\\/(\\d{1,2})\\/(\\d{1,2}) (\\d{1,2})\\.(\\d{1,2})\\.(\\d{1,2})?( AM|PM)?\\]'\n",
    "    pattern2 = r'(\\d{1,2})\\/(\\d{1,2})\\/(\\d{0,2})\\, (\\d{0,2}):(\\d{1,2})( AM|PM)? -'\n",
    "    pattern3 = r'(\\d{1,2})\\/(\\d{1,2})\\/(\\d{1,2}) (\\d{1,2})\\.(\\d{1,2})'\n",
    "    pattern4 = r'(\\d{1,2})\\/(\\d{1,2})\\/(\\d{1,4}) (\\d{1,2})\\.(\\d{1,2})'\n",
    "    \n",
    "    result1 = re.findall(pattern1, message)\n",
    "    result2 = re.findall(pattern2, message)\n",
    "    result3 = re.findall(pattern3, message)\n",
    "    result4 = re.findall(pattern4, message)\n",
    "    \n",
    "    date = []\n",
    "    if result1:\n",
    "        for result in result1:\n",
    "            date.append(result[0]+'/'+result[1]+'/'+result[2])\n",
    "    elif result2:\n",
    "        for result in result2:\n",
    "            date.append(result[1]+'/'+result[0]+'/'+result[2])\n",
    "    elif result3:\n",
    "        for result in result3:\n",
    "            date.append(result[0]+'/'+result[1]+'/'+result[2])\n",
    "    elif result4:\n",
    "        for result in result4:\n",
    "            date.append(result[0]+'/'+result[1]+'/'+result[2])\n",
    "    else:\n",
    "        print(\"No pattern detected.\")\n",
    "    return date"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 221,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_sender(message):\n",
    "    \"\"\" This function is to get the sender from messages.\n",
    "    \n",
    "        patternNo where the sender is a phone number (contact hasn't been saved)\n",
    "        patternNa where the sender is a name\n",
    "    \"\"\"\n",
    "    patternNo = r'(\\+[\\d+\\-\\s].*):'\n",
    "    patternNa = r'[\\]|\\-] ?([\\w\\.].*):'\n",
    "\n",
    "    resultNo = re.findall(patternNo, message)\n",
    "    resultNa = re.findall(patternNa, message)\n",
    "    \n",
    "    if resultNo:\n",
    "        return resultNo\n",
    "    elif resultNa:\n",
    "        return resultNa"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 222,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_messages(message):\n",
    "    \"\"\" This function is to get the messages! \"\"\"\n",
    "    \n",
    "    pattern = r': ([\\d\\w\\s\\W][^\\[\\]]+)' # messages pattern\n",
    "    RE_EMOJI = re.compile(\"([\"\n",
    "                          \"\\U0001F1E0-\\U0001F1FF\"  # flags (iOS)\n",
    "                          \"\\U0001F300-\\U0001F5FF\"  # symbols & pictographs\n",
    "                          \"\\U0001F600-\\U0001F64F\"  # emoticons\n",
    "                          \"\\U0001F680-\\U0001F6FF\"  # transport & map symbols\n",
    "                          \"\\U0001F700-\\U0001F77F\"  # alchemical symbols\n",
    "                          \"\\U0001F780-\\U0001F7FF\"  # Geometric Shapes Extended\n",
    "                          \"\\U0001F800-\\U0001F8FF\"  # Supplemental Arrows-C\n",
    "                          \"\\U0001F900-\\U0001F9FF\"  # Supplemental Symbols and Pictographs\n",
    "                          \"\\U0001FA00-\\U0001FA6F\"  # Chess Symbols\n",
    "                          \"\\U0001FA70-\\U0001FAFF\"  # Symbols and Pictographs Extended-A\n",
    "                          \"\\U00002702-\\U000027B0\"  # Dingbats\n",
    "                          \"])\")\n",
    "\n",
    "    message = RE_EMOJI.sub(r'', message)\n",
    "    message = \" \".join(message.split()) # remove excess line\n",
    "    message = \" \".join(message.split('\\u200e')) # remove idk what this is xixi\n",
    "    messages = re.findall(pattern, message)\n",
    "    return messages"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 227,
   "metadata": {},
   "outputs": [],
   "source": [
    "def convert_to_csv(dataframe, messages):\n",
    "    \"\"\" This function is to convert .txt files to .csv files.\n",
    "        All files stored in dataset_csv/\n",
    "    \"\"\"\n",
    "    path = 'dataset_csv/'\n",
    "    \n",
    "    if not os.path.exists(path):\n",
    "        os.mkdir(path)\n",
    "    \n",
    "    file = 'dataset_csv/' + messages.replace('.txt', '.csv')\n",
    "    dataframe.to_csv(file, index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 228,
   "metadata": {},
   "outputs": [],
   "source": [
    "def create_df(message):\n",
    "    \"\"\" Aggregate date, sender, and messages then create a Data Frame \"\"\"\n",
    "    date = get_date(message)\n",
    "    sender = get_sender(message)\n",
    "    messages = get_messages(message)\n",
    "    df = pd.DataFrame(\n",
    "            list(zip(date, sender, messages)),\n",
    "            columns=['timestamp', 'sender', 'messages']\n",
    "        )\n",
    "    return df[1:]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 230,
   "metadata": {},
   "outputs": [],
   "source": [
    "def main():\n",
    "    files = os.listdir(os.getcwd()+'/dataset')\n",
    "    messages_list = [file for file in files if file.endswith('.txt')]\n",
    "    \n",
    "    for messages in messages_list: \n",
    "        with open('dataset/' + messages, encoding='utf-8') as file:\n",
    "            message = file.read()\n",
    "            \n",
    "            df = create_df(message)\n",
    "            \n",
    "            convert_to_csv(df, messages)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 232,
   "metadata": {},
   "outputs": [],
   "source": [
    "main()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
