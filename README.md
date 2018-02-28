# Invoice distributer
This is a script made for sending the correct attachment to the correct email adress.

This is achieved by taking each email adress in a `.CSV` and map that one to one file in the attachment folder provided. The first email will be sent the first file, second email the second file and so on.
#### IMPORTANT
- Attachment files should be named a number, eg. `5.txt`.
- If the attachment files have any other extension that `.txt` this will have to be changed in the code. Only one type of attachments can be sent in this implementation.
- Email and app specific password for less secure apps need to be entered into the code.
- The subject and message of the mail also needs to be assigned the `subject` and `body` variables respectively.
