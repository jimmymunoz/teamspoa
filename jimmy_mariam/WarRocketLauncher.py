from math import *

#Globals
distanceToHelpBase = 100



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
				if(message.getMessage() == "ThereAreEnemiesInOurBase"): 
					WarRocketLauncher.ourBaseAngle = message.getAngle();
					baseDistance = message.getDistance();
					if( baseDistance <= distanceToHelpBase ):
						setHeading(WarRocketLauncher.ourBaseAngle)
						setDebugString("goToDefendOurBase: " + str(baseDistance));
						WarRocketLauncher.nextState = defendOurBase
					else:
						setDebugString("NotEarly: " + str(baseDistance));
						
					return move();
			return move()

def validateMainMessages():
	messages = getMessages()
	for message in messages:
		if(message.getMessage() == "identifyYou"):
			sendMessage(message.getSenderID(), "responseIdentify", ("WarRocketLauncher") ); #reply to Base
		elif(message.getMessage() == "yourGroupIs"):
			content = message.getContent()
			WarRocketLauncher.GroupName = content[0]; #Jimmy: setGroupName
			if( WarRocketLauncher.GroupName == "Attack" ):
				requestRole ("defenceurs", "attaque")
			
			elif( WarRocketLauncher.GroupName == "Defense" ):
				requestRole ("defenceurs", "defend")
			

	return None

class surveillerBase(object):
	@staticmethod
	def execute():
		WarRocketLauncher.nextState = surveillerBase
		broadcastMessageToAgentType(WarAgentType.WarBase, "whereAreYou", "");
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "OurBaseIsHere"):
				if(message.getDistance() < distanceToHelpBase):
					setDebugString("je surveille la base")			
					#setHeading(message.getAngle())
					#setRandomHeading()
					return move()
				else:
					setHeading(message.getAngle())
					return move()
		
		return move()

def reflexes():
	PerceptsEnemiesWarBase = getPerceptsEnemiesWarBase();
	PerceptsEnemiesWarluncher = getPerceptsEnemiesWarRocketLauncher();
	if PerceptsEnemiesWarBase:
		#broadcastMessageToAll("EnemyBase","")
		#infoBase = ( str(percetEnemyBase.getAngle()), str(percetEnemyBase.getDistance()), str(getHeading()) )
		#broadcastMessageToAll("EnemyBaseFound",  infoBase )
		for percept in PerceptsEnemiesWarBase:
			setHeading(percept.getAngle())
			if (isReloaded()):
				return fire()
				#return move()
			else :
				return reloadWeapon()
				#return move()
	if( WarRocketLauncher.GroupName == "Defense" ):#Jimmy: Only for the defense Group
		for percept in getPerceptsEnemies():
			setHeading(percept.getAngle())
			if (isReloaded()):
				return fire()
				#return move()
			else :
				return reloadWeapon()

	if isBlocked():
		RandomHeading()
		return None

class defendOurBase(object):
	@staticmethod
	def execute():
		setHeading(WarRocketLauncher.ourBaseAngle)
		setDebugString("goToDefendOurBase")
		ThereAreEnemiesInOurBase = False
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "ThereAreEnemiesInOurBase"):
				ThereAreEnemiesInOurBase = True
				break
			elif(message.getMessage() == "BaseState" and message.getContent() == "BaseOk"):
				ThereAreEnemiesInOurBase = True
				break

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
