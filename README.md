# Develop a Telegram / WhatsApp Bot that can:

1. Save audio messages from dialogues to a database (DBMS or disk) by user IDs.
   Audio should be converted to wav format with a sampling rate of 16kHz. Recording format: uid -> [audio_message_0, audio_message_1, ..., audio_message_N].
2. Determines whether there is a face in the photos being sent or not, saves only those where it is
