#Globals
distanceToHelpBase = 500
from math import *

class searchEnemyBase(object):
	@staticmethod
	def execute():
		WarRocketLauncher.nextState = searchEnemyBase
		
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "RocketLaunchersAttack" and False): #Pending to finish
				WarRocketLauncher.enemyBaseAngle = message.getAngle();
				arrContent = message.getContent()
				explorerAngle = float(arrContent[0]);
				explorerDistance = float(arrContent[1]);
				setHeading(WarRocketLauncher.enemyBaseAngle)
				#newAngle = 180 - (WarRocketLauncher.enemyBaseAngle + explorerAngle);##pendiente problema con angulos superiores a 180
				#newAngle = 360 - (WarRocketLauncher.enemyBaseAngle + explorerAngle);##pendiente problema con angulos superiores a 180
				#newAngle = 10
				newAngle = tan(message.getDistance()/explorerDistance)
				debugStr = "AttackEnemyBase EA(" + str(explorerAngle) + ") BA ( " + str(message.getAngle()) + " )" + " ED: (" + str(explorerDistance) + ")" + " BD: (" + str(message.getDistance()) + ")" ;
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
			if(message.getMessage() == "Base ennemie"): 
				arrContent = message.getContent()
				explorerAngl = float(arrContent[0]);
				setDebugString("attaqueeeee ")
				broadcastMessage("defenceurs", "attaque","attaqueeee",(str(explorerAngl)))
			if(message.getMessage() == "attaqueeee" and message.getMessage() == "Base ennemie"):
				arrConte = message.getContent()
				Angl = float(arrConte[0]);
				setHeading(Angl)
				setDebugString("goToAttack: " + str(Angl));
			if(message.getMessage() == "ThereAreEnemiesLauncher"):
				setDebugString("on defend")
				broadcastMessage("defenceurs", "defend","defendezz",(str(message.getAngle())))
			if(message.getMessage() == "defendezz" and message.getMessage() == "ThereAreEnemiesLauncher"):
				Contenu = message.getContent()
				angle = float(arrConte[0]);
				setHeading(angle + 180)
				setDebugString("goToDefend: " + str(angle));	
			#	PerceptsEnemiesWarBase = getPerceptsEnemiesWarBase();
	        #    if PerceptsEnemiesWarBase:
			#	   WarRocketLauncher.currentState = Attack;
		return move()
#class Attack(object):
#	@staticmethod
#	def execute():
#		PerceptsEnemiesWarBase = getPerceptsEnemiesWarBase();
#		if PerceptsEnemiesWarBase:
#			for percept in PerceptsEnemiesWarBase:
#				setHeading(percept.getAngle())
#				if (isReloaded()):
#					return fire()
#				    #return move()
#				else :
#					return reloadWeapon()
				    #return move()
#		if isBlocked():
#			RandomHeading()
#			return None
def reflexes():
	PerceptsEnemiesWarBase = getPerceptsEnemiesWarBase();
	PerceptsEnemiesWarluncher = getPerceptsEnemiesWarRocketLauncher();
	if PerceptsEnemiesWarBase:
		broadcastMessageToAll("EnemyBase","")
		for percept in PerceptsEnemiesWarBase:
			setHeading(percept.getAngle())
			if (isReloaded()):
				return fire()
				#return move()
			else :
				return reloadWeapon()
				#return move()
	if PerceptsEnemiesWarluncher:
		for percept in PerceptsEnemiesWarluncher:
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

		if(not ThereAreEnemiesInOurBase ):#JImmy: if there are not enemies in the base he continues
			WarRocketLauncher.nextState = searchEnemyBase
		return move();

class etatInitial(object):
	@staticmethod
	def execute():
		setDebugString("etat  initial")
		broadcastMessageToAgentType(WarAgentType.WarBase, "whereAreYou", "");
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "OurBaseIsHere"):
				if(message.getDistance() <= 75):
					requestRole ("defenceurs", "defend")
					setDebugString("je surveille la base")
					setHeading(message.getAngle())
					return move()
					WarRocketLauncher.nextState = surveillerBase
				else:
					requestRole ("defenceurs", "attaque")
					setDebugString("je vais attaquer")
					WarRocketLauncher.nextState = searchEnemyBase
		return move()
			
class surveillerBase(object):
	@staticmethod
	def execute():
		broadcastMessageToAgentType(WarAgentType.WarBase, "whereAreYo", "");
		messages = getMessages();
		for message in messages:
			if(message.getMessage() == "OurBaseIsHere"):
				if(message.getDistance() <= 100):
					setDebugString("maaaaaaaBase")			
					setHeading(message.getAngle()+20)
					return move()
				else:
					setHeading(message.getAngle()+20 )
					return move()
		return move()
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
		result = etatInitial.execute()
		WarRocketLauncher.nextState = etatInitial
		return result;

# Initialisation des variables
WarRocketLauncher.nextState = etatInitial
WarRocketLauncher.currentState = None

WarRocketLauncher.ourBaseAngle = 0
WarRocketLauncher.enemyBaseAngle = 0
