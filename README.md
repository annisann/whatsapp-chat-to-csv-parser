## WhatsApp Chat Parser
Converts .txt file to .csv file for WhatsApp chat.
<br>
<br>

***IMPORTANT NOTE***\
Due to some limitations, please check the code before you start parsing. All limitations and patterns used are listed below.

### Patterns List
This is all pattern I've known. Still, I don't have pattern 4 on my dataset.

<table>
   <thead>
      <tr>
         <th align='center'>Name</th>
         <th align='center'>Pattern</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td align='center'> pattern 1 </td>
         <td align='left'> [DD/MM/YY hh.mm.ss] Sender: Messages <br>
                           [DD/MM/YY hh.mm.ss AM/PM] Sender: Messages </td>
      </tr>
      <tr>
         <td align='center'> pattern 2 </td>
         <td align='left'> MM/DD/YY, hh.mm - Sender: Messages <br>
                           MM/DD/YY, hh:mm AM/PM - Sender: Messages </td>
      </tr>
      <tr>
         <td align='center'> pattern 3 </td>
         <td align='left'> DD/MM/YY hh.mm - Sender: Messages </td>
      </tr>
           <tr>
         <td align='center'> pattern 4 </td>
         <td align='left'> DD/MM/YYYY hh.mm - Sender: Messages </td>
      </tr>
   </tbody>
</table>

### Limitations
- Tried on iOS file with pattern 1 without AM/PM.
- Tried on Android file with pattern 2 with AM/PM.
- Tried on Android file with pattern 3.
- Need to remove the first line of .txt file for Android since it doesn't have a sender.
- Could only works if the senders is whether a name only, or phone numbers only.
- Couldn't parse if the sender is a phone number (a.k.a not saved as contacts) and a name.
- If the messages have colons, then it will match as the sender. So I've deleted all colons except in sender field. Thus, won't show https://.
