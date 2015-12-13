from math import *

#Globals
distanceToHelpBase = 400


class searchEnemyBase(object):
	@staticmethod
	def execute():
		WarRocketLauncher.nextState = searchEnemyBase
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "RocketLaunchersAttack" and False): #Pending to calculate base enemi position
				WarRocketLauncher.enemyBaseAngle = message.getAngle();
				arrContent = message.getContent()
				explorerAngle = float(arrContent[0]);
				explorerDistance = float(arrContent[1]);

				RLH = str( WarRocketLauncher.getHeading() );
				newAngle = 360 - (WarRocketLauncher.enemyBaseAngle + explorerAngle)  ;##pendiente problema con angulos superiores a 180
				##newAngle = 360 - (WarRocketLauncher.enemyBaseAngle + explorerAngle);##pendiente problema con angulos superiores a 180
				#newAngle = 10
				debugStr = "AttackEnemyBase EA(" + str(explorerAngle) + ") BA( " + str(message.getAngle()) + " )" + " ED: (" + str(explorerDistance) + ")" + " BD: (" + str(message.getDistance()) + ") RLH: " + RLH;
				setDebugString(debugStr);
				setHeading(newAngle)
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

def reflexes():
	#PerceptsEnemiesWarBase = getPerceptsEnemiesWarBase();
	#if PerceptsEnemiesWarBase:
	#	broadcastMessageToAll("EnemyBase","")
	#	return idle() #• Idle : l’agent ne bougera plus et ne fera aucune action. 
	#	for percept in PerceptsEnemiesWarBase:
	#		setHeading(percept.getAngle())
	#		if (isReloaded()):
	#			return fire()
	#			#return move()
	#		else :
	#			return reloadWeapon()
	#			#return move()
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
			if(message.getMessage() == "BaseState" and message.getContent() == "BaseOk"):
				ThereAreEnemiesInOurBase = True
				break


		if(not ThereAreEnemiesInOurBase ):#JImmy: if there are not enemies in the base he continues
			WarRocketLauncher.nextState = searchEnemyBase
		return move();

class WiggleState(object):
	@staticmethod
	def execute():
		setDebugString("WiggleState")
		return move();

def actionWarRocketLauncher():
	result = reflexes() # Reflexes
	if result:
		return result

	# FSM - Changement d'Ã©tat
	WarRocketLauncher.currentState = WarRocketLauncher.nextState
	WarRocketLauncher.nextState = None

	if WarRocketLauncher.currentState:
		return WarRocketLauncher.currentState.execute()
	else:
		result = searchEnemyBase.execute()
		WarRocketLauncher.nextState = searchEnemyBase
		return result;

# Initialisation des variables
WarRocketLauncher.nextState = searchEnemyBase
WarRocketLauncher.currentState = None

WarRocketLauncher.ourBaseAngle = 0
WarRocketLauncher.enemyBaseAngle = 0
#WarRocketLauncher.lastHealth = 10
