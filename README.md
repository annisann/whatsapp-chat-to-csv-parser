## WhatsApp Chat Parser
Converts .txt file to .csv file

***IMPORTANT NOTE***
Due to some limitations, please check the code before you start parsing. All limitations and patterns used are listed below.

#### Patterns List
This is patterns I've known. Stil, I don't have pattern 4 on my dataset.
pattern 1 [DD/MM/YY HH.MM.SS] Sender: Messages
          [DD/MM/YY HH.MM.SS AM/PM] Sender: Messages
pattern 2 MM/DD/YY, HH:MM - Sender: Messages
          MM/DD/YY, HH:MM AM/PM - Sender: Messages
pattern 3 DD/MM/YY HH.MM - Sender: Messages
pattern 4 DD/MM/YYYY HH.MM - Sender: Messages

#### Limitations
- Tried on iOS file with pattern 1 without AM/PM.
- Tried on Android file with pattern 2 with AM/PM.
- Tried on Android file with pattern 3.
- Need to remove the first line of .txt file for Android since it doesn't have a sender.
- Could only works if the senders is whether a name only, or phone numbers only.
- Couldn't parse if the sender is a phone number (a.k.a not saved as contacts) and a name.
- If the messages have colons, then it will match as the sender. So I've deleted all colons except in sender field. Thus, won't show https://.
