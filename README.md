# WhatsApp Chat Parser
Converts .txt file to .csv file

This is an on-going, so the code is not final **YET!**

Constraints:
- Only tried on iOS file with a pattern without AM/PM
- Couldn't parse if the sender is a phone number (a.k.a not saved as contacts) and a name.
- Could only works if the senders is whether a name only, or phone numbers only.
- If the messages have semicolons, then it will match as the sender. So I've deleted all semicolons except in sender field.
