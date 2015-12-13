class SearchFoodState(object):
	@staticmethod
	def execute():
		setDebugString("SearchFoodState")
		if isBagFull():
			actionWarExplorer.nextState = GoHomeState
			return idle()

		actionWarExplorer.nextState = SearchFoodState
		percepts = getPerceptsFood()
		if percepts:
			#broadcastMessageToAgentType(WarAgentType.WarExplorer,"FoodHere","")
			if percepts[0].getDistance() < getMaxDistanceTakeFood():
				return take()
			else:
				followTarget(percepts[0])
				return move()
		else:
			for message in getMessages():
				if message.getMessage() == "FoodHere":
					followTarget(message)
		return move()

class GoHomeState(object):
	@staticmethod
	def execute():
		setDebugString("GoHomeState")
		if getNbElementsInBag() == 0:
			# Transition vers l'Ã©tat SearchFood
			actionWarExplorer.nextState = SearchFoodState
			return idle()
		# Maintien de l'Ã©tat
		actionWarExplorer.nextState = GoHomeState
		percepts = getPerceptsAlliesWarBase()
		# Cherche une base dans son champs de vision
		if percepts:
			if percepts[0].getDistance() < maxDistanceGive():
				giveToTarget(percepts[0])
				return give()
			else:
				followTarget(percepts[0])
				return move()
		# Cherche une base par les messages
		broadcastMessageToAgentType(WarAgentType.WarBase,"whereAreYouBase","")
		for mess in getMessages():
			if isMessageOfWarBase(mess):
				followTarget(mess)
				return move()
		return move()


class WiggleState(object):
	@staticmethod
	def execute():
		setDebugString("WiggleState")
		if (isBlocked()) :
			RandomHeading()
		return move();


def validateMainMessages():
	messages = getMessages();
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			sendMessage(message.getSenderID(), "responseIdentify", (str("WarExplorer") ) );


def reflexes():
	PerceptsEnemiesWarBase = getPerceptsEnemiesWarBase();
	if PerceptsEnemiesWarBase:
		percetEnemyBase = PerceptsEnemiesWarBase[0]
		#actionWarExplorer.idBaseFound = percetEnemyBase.getId()
		#broadcastMessageToAll("EnemyBase",  infoBase )
		infoBase = ( str(percetEnemyBase.getAngle()), str(percetEnemyBase.getDistance()), str(getHeading()) )
		broadcastMessageToAll("EnemyBaseFound",  infoBase )
		setHeading( percetEnemyBase.getAngle() )
		if( percetEnemyBase.getDistance() > 5 ):
			actionWarExplorer.currentTask = "goToEnamyBase";
		else:
			actionWarExplorer.currentTask = "waitingRocket";
	
	if isBlocked(): 
		RandomHeading()

	return None


def actionWarExplorer():
	validateMainMessages()
	result = reflexes() # Reflexes
	if result:
		return result



	if( actionWarExplorer.currentTask == "goToEnamyBase" ):
		setDebugString("goToEnemyBase" + " Id: ")
		return move()
	if( actionWarExplorer.currentTask == "waitingRocket" ):
		setDebugString("waitingRocketLauchersResponse" + " Id: ")
		return idle() #• Idle : l’agent ne bougera plus et ne fera aucune action. 

	# FSM - Changement d'Ã©tat
	actionWarExplorer.currentState = actionWarExplorer.nextState
	actionWarExplorer.nextState = None

	if actionWarExplorer.currentState:
		return actionWarExplorer.currentState.execute()
	else:
		result = WiggleState.execute()
		actionWarExplorer.nextState = WiggleState
		return result

# Initialisation des variables
actionWarExplorer.nextState = SearchFoodState
actionWarExplorer.currentState = None
actionWarExplorer.currentTask = ""
actionWarExplorer.idBaseFound = 0
