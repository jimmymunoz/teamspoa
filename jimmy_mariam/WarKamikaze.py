
def actionWarKamikaze():
	setDebugString("WarKamikaze");
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			sendMessage(message.getSenderID(), "responseIdentify", ("WarKamikaze") );
			break;

	return move();