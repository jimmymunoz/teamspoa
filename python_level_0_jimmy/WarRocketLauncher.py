
def actionWarRocketLauncher():

	percepts = getPercepts();
	for percept in percepts:
		if (percept.getType().equals(WarAgentType.WarBase)):
			if (isEnemy(percept)):
				setDebugString("Mode hunter")
				setHeading(percept.getAngle())

				if (isReloaded()):
					#return fire()
					return move()
				else :
					#return reloadWeapon()
					return move()
			#else:
				#setDebugString("No cible")
		#else:
			#setDebugString("No cible")

	#if (len(percepts) == 0):
		#setDebugString("No cible")

	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "RocketLaunchersAttack" and False): #Pending to finish
			baseAngle = message.getAngle();
			arrContent = message.getContent()
			explorerAngle = float(arrContent[0]);
			setHeading(baseAngle)
			newAngle = 180 - (baseAngle + explorerAngle);##pendiente problema con angulos superiores a 180
			newAngle = 360 - (baseAngle + explorerAngle);##pendiente problema con angulos superiores a 180
			#newAngle = 10
			debugStr = "AttackEnemyBase Explorer Angle(" + str(explorerAngle) + ") Base Angle ( " + str(message.getAngle()) + " )" + " newAngle: (" + str(newAngle) + ")" ;
			setDebugString(debugStr);
			setHeading(newAngle)
			return move();
		if(message.getMessage() == "ThereAreEnemies"): 
			baseAngle = message.getAngle();
			setHeading(baseAngle)
			return move();
			

	if(isBlocked()):
		RandomHeading()


	return move();
