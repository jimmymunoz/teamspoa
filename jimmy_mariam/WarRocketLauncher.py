DEFENSE_RANDOM_HEADING = 5
DISTANCE_TO_GARDE_OUR_BASE = 60
DISTANCE_TO_HELP_OUR_BASE = 500

from math import *
#Globals



#Jimmy: Method to calculate the enemy base angle.
def getEnemyBaseAngle(explorerAngle, explorerDistance, baseAngle, baseDistance):
	newAngle = 0
	if (explorerDistance > baseDistance):
		hypoteneuse =  explorerDistance; #hypoténuse
		ca = baseDistance
	else:
		hypoteneuse =  baseDistance; #hypoténuse
		ca = explorerDistance

	angle = baseAngle - explorerAngle;
	# triangle 1
	# co1 = h1 * COS(angle) 
	# ca1 = h1 * SEN(angle) 
	# difAngle1 = (180 - 90 - baseAngle)
	# test -> ca^2 + co^2 =  h1^2

	# triangle 2
	# co2 = abs(explorerAngle - ca1)
	# ca2 = co1
	# difAngle2 = tang = co2/ca2

	# triangle 3
	# angleRocket = difAngle1 + difAngle2

	return newAngle


class searchEnemyBase(object):
	@staticmethod
	def execute():
		
		if( WarRocketLauncher.GroupName == "Defense" ):
			WarRocketLauncher.nextState = surveillerBase
			WarRocketLauncher.currentState = WarRocketLauncher.nextState
			return idle()
		else:
			messages = getMessages();
			for message in messages:
				if(message.getMessage() == "EnemyBaseFound"): #Pending to calculate base enemy position
					arrContent = message.getContent()
					WarRocketLauncher.enemyBaseAngle = message.getAngle();
					baseDistance = float(message.getDistance());

					debugStr = "AttackEnemyBase BA( " + str(message.getAngle()) + " ) BD: (" + str(message.getDistance()) + ") ";
					setDebugString(debugStr);

					setHeading(message.getAngle())
					return move();
				if(message.getMessage() == "RocketLaunchersAttack" and False): #Pending to calculate base enemi position
					WarRocketLauncher.enemyBaseAngle = message.getAngle();
					arrContent = message.getContent()
					explorerAngle = float(arrContent[0]);
					explorerDistance = float(arrContent[1]);
					baseAngle = float(message.getAngle());
					baseDistance = float(message.getDistance());

					#newAngle = 360 - (WarRocketLauncher.enemyBaseAngle + explorerAngle)  ;##pendiente problema con angulos superiores a 180
					newAngle = getEnemyBaseAngle(explorerAngle, explorerDistance, baseAngle, baseDistance)
					##newAngle = 360 - (WarRocketLauncher.enemyBaseAngle + explorerAngle);##pendiente problema con angulos superiores a 180
					#newAngle = 10
					debugStr = "AttackEnemyBase EA(" + str(arrContent[0]) + ") BA( " + str(message.getAngle()) + " )" + " ED: (" + str(arrContent[1]) + ")" + " BD: (" + str(message.getDistance()) + ") ";
					setDebugString(debugStr);
					#setHeading(newAngle)
					return move();
			return move()

class surveillerBase(object):
	@staticmethod
	def execute():
		WarRocketLauncher.nextState = surveillerBase
		broadcastMessageToAgentType(WarAgentType.WarBase, "whereAreYou", "");
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "OurBaseIsHere"):
				if(message.getDistance() < DISTANCE_TO_GARDE_OUR_BASE):
					setDebugString("je surveille la base")			
					#setHeading(message.getAngle())
					#setRandomHeading()
					return move()
				else:
					setHeading(message.getAngle())
					return move()
		
		setRandomHeading(DEFENSE_RANDOM_HEADING);
		return move()

def validateMainMessages():
	messages = getMessages()
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			sendMessage(message.getSenderID(), "responseIdentify", ("WarRocketLauncher") ); #reply to Base
		elif(message.getMessage() == "yourGroupIs"):
			content = message.getContent()
			WarRocketLauncher.GroupName = content[0]; #Jimmy: setGroupName
			setDebugString("Group: " + content[0])
			if( WarRocketLauncher.GroupName == "Attack" ):
				requestRole ("defenceurs", "attaque")
			
			elif( WarRocketLauncher.GroupName == "Defense" ):
				requestRole ("defenceurs", "defend")
		
		elif(message.getMessage() == "ThereAreEnemiesInOurBase"): 
			WarRocketLauncher.ourBaseAngle = message.getAngle();
			baseDistance = message.getDistance();
			if( WarRocketLauncher.GroupName == "Defense" ):
				setHeading(message.getAngle())
			else:
				if( baseDistance <= DISTANCE_TO_HELP_OUR_BASE ):
					setHeading(message.getAngle())
					#setDebugString("goToDefendOurBase: " + str(baseDistance));
					WarRocketLauncher.nextState = defendOurBase
					WarRocketLauncher.GroupName == "Defense"
				else:
					#setDebugString("NotEarly: " + str(baseDistance));
					WarRocketLauncher.GroupName = "Attack"
			#return move();

	return None

def reflexes():
	percepts = getPerceptsEnemies()
	enemyFound = None
	for percept in percepts:
		if( percept.getType() == WarAgentType.WarBase ):
			infoBase = ( str(percept.getAngle()), str(percept.getDistance()), str(getHeading()) )
			broadcastMessageToAll("EnemyBaseFound",  infoBase )
			enemyFound = percept
			break
		if( WarRocketLauncher.GroupName == "Defense" ):#Only Defense
			if( percept.getType() == WarAgentType.WarRocketLauncher ):
				enemyFound = percept
				break
			if( percept.getType() == WarAgentType.WarExplorer ):
				enemyFound = percept
				break
			if( percept.getType() == WarAgentType.WarKamikaze ):
				enemyFound = percept
				break
			if( percept.getType() == WarAgentType.WarEngineer and False ):#Disabled
				enemyFound = percept
				break
			if( percept.getType() == WarAgentType.WarTurret and False ):#Disabled
				enemyFound = percept
				break

	if (enemyFound):
		setHeading(enemyFound.getAngle())
		if (isReloaded()):
			return fire()
		else :
			return reloadWeapon()

	if isBlocked():
		if( WarRocketLauncher.GroupName == "Defense" ):
			setRandomHeading(30)
		else:
			RandomHeading()
		return None

class defendOurBase(object):
	@staticmethod
	def execute():
		#setHeading(message.getAngle())
		#setDebugString("goToDefendOurBase")
		ThereAreEnemiesInOurBase = False
		messages = getMessages();
		for message in messages:

			if(message.getMessage() == "ThereAreEnemiesInOurBase"):
				ThereAreEnemiesInOurBase = True
				WarRocketLauncher.nextState = searchEnemyBase
				WarRocketLauncher.ourBaseAngle = message.getAngle();
				if( WarRocketLauncher.GroupName == "Defense" ):
					setHeading(message.getAngle())
				break
			elif(message.getMessage() == "BaseState" and message.getContent() == "BaseOk"):
				ThereAreEnemiesInOurBase = True
				WarRocketLauncher.nextState = defendOurBase
				break

		if( WarRocketLauncher.GroupName != "Defense" ):
			if(not ThereAreEnemiesInOurBase ): #JImmy: if there are not enemies in the base he continues
				WarRocketLauncher.nextState = searchEnemyBase

		return move();



class WiggleState(object):
	@staticmethod
	def execute():
		setDebugString("WiggleState")
		return move();

def actionWarRocketLauncher():
	validateMainMessages()
	result = reflexes() # Reflexes
	if result:
		return result

	# FSM - Changement d'Ã©tat
	WarRocketLauncher.currentState = WarRocketLauncher.nextState
	WarRocketLauncher.nextState = None

	if( WarRocketLauncher.GroupName == "Defense" ):
		WarRocketLauncher.nextState = surveillerBase

	if WarRocketLauncher.currentState:
		#setDebugString("My Group Is: " + WarRocketLauncher.GroupName )
		return WarRocketLauncher.currentState.execute()
	else:
		result = searchEnemyBase.execute()
		WarRocketLauncher.nextState = searchEnemyBase
		#setDebugString("My Group Is: " + WarRocketLauncher.GroupName )
		return result;

# Initialisation des variables
WarRocketLauncher.nextState = searchEnemyBase
WarRocketLauncher.currentState = None
WarRocketLauncher.ourBaseAngle = 0
WarRocketLauncher.enemyBaseAngle = 0
WarRocketLauncher.GroupName = "Attack"
#WarRocketLauncher.lastHealth = 10
