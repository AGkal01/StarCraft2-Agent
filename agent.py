from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random

#obs is the object that contains all the observactions we need it

class ZergAgent(base_agent.BaseAgent):


  n_attack = 0 
  n_bild = 0
  n_attack2 = 0


  def __init__(self):
    """initialize a variable"""
    super(ZergAgent, self).__init__()  
    self.attack_coordinates = None
    self.safe_coordinates = None
    self.drone_sent_to_work = False
    self.n_attacks = False
    self.S_base = False 


    
  def unit_type_is_selected(self, obs, unit_type):
  
    """utility fuction to simply sintax of unit type 
    selected check"""
    if (len(obs.observation.single_select) > 0 and
            obs.observation.single_select[0].unit_type == unit_type):
        return True
        
    if (len(obs.observation.multi_select) > 0 and 
            obs.observation.multi_select[0].unit_type == unit_type):
        return True
        
    return False

  def get_units_by_type(self, obs, unit_type):
  
    """utility fuction to simply sintax of unit 
    selection by type"""
    return [unit for unit in obs.observation.feature_units
            if unit.unit_type == unit_type]
    
  def can_do(self, obs, action):
  
    """utility fuction to simply sintax of 
    available actions check"""
    return action in obs.observation.available_actions


  def move_camera_S_B(self):
    #you can  see other part of the map in the coordinates of the minimap 
    camaramove = actions.FUNCTIONS.move_camera(self.second_base) 
       
    return camaramove 

  def my_attack1(self, obs):
    #if enough zerglings,send attack

    zerglings = self.get_units_by_type(obs, units.Zerg.Zergling)
    if len(zerglings) >= 10  :
        #send attack at attack locations
        if self.unit_type_is_selected(obs, units.Zerg.Zergling):
            if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                   
            
                return actions.FUNCTIONS.Attack_minimap("now", 
                                                        self.attack_coordinates)
        
        #select zerglings
        if self.can_do(obs, actions.FUNCTIONS.select_army.id):
            return actions.FUNCTIONS.select_army("select")



  def my_attack(self, obs):
    #if enough hydras and zerlings ,send attack

    zerglings = self.get_units_by_type(obs, units.Zerg.Zergling)
    hydras = self.get_units_by_type(obs, units.Zerg.Hydralisk)
    if len(zerglings) >= 10 and len(hydras) >= 6 :
        #send attack at attack locations
        if self.unit_type_is_selected(obs, units.Zerg.Zergling):
            if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):

                return actions.FUNCTIONS.Attack_minimap("now", 
                                                        self.attack_coordinates)
        
        #select all the army 
        if self.can_do(obs, actions.FUNCTIONS.select_army.id):
            return actions.FUNCTIONS.select_army("select")
 
  



  def my_spawning_pool(self, obs):
    #if there is no barraks (spawning pool) build one


    spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
    if len (spawning_pools) == 0 :
        # if drone is selected build spawning pool
        if self.unit_type_is_selected(obs, units.Zerg.Drone):        
            if self.can_do(obs,actions.FUNCTIONS.Build_SpawningPool_screen.id):
                x = random.randint(0,20)
                y = random.randint(0,60)
                

                return actions.FUNCTIONS.Build_SpawningPool_screen("now", (x,y))
            
        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)                
        if len(drones) > 0 :
            drone = random.choice(drones)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(drone.x, drone.y))

# The Hydralisk Den is a Zerg building that allows the Zerg player to create Hydralisks. 
  def my_den(self, obs):
    den = self.get_units_by_type(obs, units.Zerg.HydraliskDen)
    spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
# if you don't have a Hydralisk Den bild one
    if len (den) == 0 :
        if self.unit_type_is_selected(obs, units.Zerg.Drone):        
            if self.can_do(obs,actions.FUNCTIONS.Build_HydraliskDen_screen.id):
                x = random.randint(0,63)
                y = random.randint(20,40)
                

                return actions.FUNCTIONS.Build_HydraliskDen_screen("now", (x,y))
            
        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)                
        if len(drones) > 0 :
            drone = random.choice(drones)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(drone.x, drone.y))

#The Infestation Pit is a second-tier Zerg building that unlocks the Hive, Infestor,
#Swarm Host, as well as the Infestor and Swarm Host upgrades.

  def my_InfestationPit(self, obs):
    InfestationPit = self.get_units_by_type(obs, units.Zerg.InfestationPit)

# if you don't have a InfestationPit bild one
    if len (InfestationPit) == 0 :
        if self.unit_type_is_selected(obs, units.Zerg.Drone):        
            if self.can_do(obs,actions.FUNCTIONS.Build_InfestationPit_screen.id):
                x = random.randint(0,63)
                y = random.randint(20,40)
                

                return actions.FUNCTIONS.Build_InfestationPit_screen ("now", (x,y))
            
        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)                
        if len(drones) > 0 :
            drone = random.choice(drones)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(drone.x, 
                                                                  drone.y))


#The Lair is a Zerg building that is the direct upgrade from a Hatchery.
  def my_lair(self, obs):

    lair = self.get_units_by_type(obs, units.Zerg.Lair)
    hatchery = self.get_units_by_type(obs, units.Zerg.Hatchery)
    if len (lair) == 0 or (hatchery == 1 ):
        if self.unit_type_is_selected(obs, units.Zerg.Hatchery):        
            if self.can_do(obs,actions.FUNCTIONS.Morph_Lair_quick.id):
                return actions.FUNCTIONS.Morph_Lair_quick("now")
            
        # select some random drone for the next choice
        hatchery = self.get_units_by_type(obs, units.Zerg.Hatchery)                
        if len(hatchery) > 0 :
            hatchery = random.choice(hatchery)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(hatchery.x, hatchery.y))


#The Hive is the final upgrade to the Hatchery 
  def my_Hive(self, obs):
    Hive = self.get_units_by_type(obs, units.Zerg.Hive)
    Lair = self.get_units_by_type(obs, units.Zerg.Lair)
    if len (Hive) == 0:
        if self.unit_type_is_selected(obs, units.Zerg.Lair):        
            if self.can_do(obs,actions.FUNCTIONS.Morph_Hive_quick.id):
                return actions.FUNCTIONS.Morph_Hive_quick("now")
            
        # select some random drone for the next choice
        Lair = self.get_units_by_type(obs, units.Zerg.Lair)                
        if len(Lair) > 0 :
            Lair = random.choice(Lair)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(Lair.x, Lair.y))

#he Extractor is the Zerg building from which Drones collect Vespene Gas. 
  def my_extractor(self, obs):
    extractor = self.get_units_by_type(obs, units.Zerg.Extractor)
    geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)

    if len (extractor) != len(geysers) :
        if self.unit_type_is_selected(obs, units.Zerg.Drone):        
            if self.can_do(obs,actions.FUNCTIONS.Build_Extractor_screen.id):
                geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
                if len(geysers) > 0 :
                    geyser = random.choice(geysers)
                    return actions.FUNCTIONS.Build_Extractor_screen("now", (geyser.x,geyser.y))
            
        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)                
        if len(drones) > 0 :
            drone = random.choice(drones)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(drone.x,drone.y))

  def my_harvest_gas(self,obs):
        extractor = self.get_units_by_type(obs, units.Zerg.Extractor)
        if len(extractor) > 0:
            extractor = random.choice(extractor)
            if extractor['assigned_harvesters'] < 3:
                if self.unit_type_is_selected(obs, units.Zerg.Drone):
                    if len(obs.observation.single_select) < 2 and len(obs.observation.multi_select) < 2 :
                        if self.can_do(obs,actions.FUNCTIONS.Harvest_Gather_screen.id):                       
                            return actions.FUNCTIONS.Harvest_Gather_screen("now",(extractor.x, extractor.y))


                drones = self.get_units_by_type(obs, units.Zerg.Drone)                
                if len(drones) > 0 :
                    drone = random.choice(drones)                            
                    return actions.FUNCTIONS.select_point("select",(drone.x,drone.y))

#The Spine Crawler is a Zerg static defense structure 
  def my_SpineCrawler(self, obs):
    #if there is no SpineCrawler build one
    SpineCrawler = self.get_units_by_type(obs, units.Zerg.SpineCrawler)
    if len (SpineCrawler) < 2:
        # if drone is selected build spawning pool
        if self.unit_type_is_selected(obs, units.Zerg.Drone):        
            if self.can_do(obs,actions.FUNCTIONS.Build_SpineCrawler_screen.id):
                x = random.randint(50,60)
                y = random.randint(5,60)
     
                return actions.FUNCTIONS.Build_SpineCrawler_screen ("now", (y,x))
            
        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)                
        if len(drones) > 0 :
            drone = random.choice(drones)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(drone.x, drone.y))

#The Ultralisk Cavern is one of two Zerg tech buildings that are available after the completion of Hive.
  def my_UltraliskCavern(self, obs):
    #if there is no UltraliskCavern build one
    UltraliskCavern = self.get_units_by_type(obs, units.Zerg.UltraliskCavern)
    if len (UltraliskCavern) == 0 :
        # if drone is selected build UltraliskCavern
        if self.unit_type_is_selected(obs, units.Zerg.Drone):        
            if self.can_do(obs,actions.FUNCTIONS.Build_UltraliskCavern_screen.id):
                x = random.randint(0,63)
                y = random.randint(0,63)

                return actions.FUNCTIONS.Build_UltraliskCavern_screen("now", (y,x))
            
        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)                
        if len(drones) > 0 :
            drone = random.choice(drones)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(drone.x, drone.y))


  def my_Hatchery_2(self, obs):
    Hatchery = self.get_units_by_type(obs, units.Zerg.Hatchery)
    if len (Hatchery) == 0 :
        # if drone is selected build Hatchery
        if self.unit_type_is_selected(obs, units.Zerg.Drone):        
            if self.can_do(obs,actions.FUNCTIONS.Build_Hatchery_screen.id):
                x = random.randint(0,80)
                y = random.randint(0,80)
                

                return actions.FUNCTIONS.Build_Hatchery_screen("now", (x,y))
            
        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)                
        if len(drones) > 0 :
            drone = random.choice(drones)
                    
            return actions.FUNCTIONS.select_point("select_all_type",(drone.x, drone.y))


  def my_more_units(self, obs, type):
    #make units
    if self.unit_type_is_selected(obs, units.Zerg.Larva):
        free_supply = (obs.observation.player.food_cap - obs.observation.player.food_used)
        
        # if there are no more houses (overlords) build more
        if free_supply < 2 :
            if self.can_do(obs, actions.FUNCTIONS.Train_Overlord_quick.id):
                return actions.FUNCTIONS.Train_Overlord_quick("now")

        if type == "zergling":
            # if it is possible build troops zergling      
            if self.can_do(obs, actions.FUNCTIONS.Train_Zergling_quick.id):
                    return actions.FUNCTIONS.Train_Zergling_quick("now")
        
        if type == "drone":
            # if it is possible build troops drone  
            if self.can_do(obs, actions.FUNCTIONS.Train_Drone_quick.id):
                    return actions.FUNCTIONS.Train_Drone_quick("now")
                    
        if type == "hydralisk":
            # if it is possible build troops hydralisk 
            if self.can_do(obs, actions.FUNCTIONS.Train_Hydralisk_quick.id):
                    return actions.FUNCTIONS.Train_Hydralisk_quick("now")

        if type == "Ultralisk":   
             # if it is possible build troops Ultralisk
            if self.can_do(obs, actions.FUNCTIONS.Train_Ultralisk_quick.id):
                    return actions.FUNCTIONS.Train_Ultralisk_quick("now")

    
    larvae = self.get_units_by_type(obs, units.Zerg.Larva)
    if len(larvae) > 0 :
        larva = random.choice(larvae)

        return actions.FUNCTIONS.select_point("select_all_type", (larva.x, larva.y))


  def step(self, obs):
    super(ZergAgent, self).step(obs)
         
  
    #select/guess the location of the enemies
    if obs.first():
        player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                               features.PlayerRelative.SELF).nonzero()
        
        xmean = player_x.mean()
        ymean = player_y.mean()

        if xmean <= 31 and ymean <= 31:
            #set pair of coordintates
            self.attack_coordinates = [39,45]
            self.safe_coordinates = [12,17]
            self.second_base = [15,12]
        else:
            #set pair of coordintates
            self.attack_coordinates = [20,20]
            self.safe_coordinates = [49,49]
            self.second_base = [20,46]      



    #make more drones
    drones =  self.get_units_by_type(obs, units.Zerg.Drone)
    if len(drones) <= 19 :
        make_units = self.my_more_units(obs,"drone")
        if make_units:
            return make_units

    #build spawning pool
    spawning_pool = self.my_spawning_pool(obs)
    if spawning_pool:
        return spawning_pool


    #build extractor
    extractor = self.my_extractor(obs)
    if extractor:
        return extractor
    
    #harvest gas
    gas = self.my_harvest_gas(obs)
    if gas:
        return gas

    SpineCrawler = self.my_SpineCrawler(obs)
    if SpineCrawler:
        return SpineCrawler
    

    #build Lair
    lair = self.my_lair(obs)
    if lair:
        return lair


    #camaramove = self.move_camera_S_B()
    #return camaramove 

    #train a Queen 
    queens = self.get_units_by_type(obs, units.Zerg.Queen)
    if len(queens) <1 :
        if self.unit_type_is_selected(obs, units.Zerg.Lair):        
            if self.can_do(obs,actions.FUNCTIONS.Train_Queen_quick.id):
                    return actions.FUNCTIONS.Train_Queen_quick("now")

    #build a Hydralisden
    den = self.my_den(obs)
    if den:
        return den

    #build a InfestationPit
    InfestationPit = self.my_InfestationPit(obs)
    if InfestationPit:
        return InfestationPit

    #build a Hive
    Hive = self.my_Hive(obs)
    if Hive:
        return Hive

    #build a UltraliskCavern
    Ultra = self.my_UltraliskCavern(obs)
    if Ultra:
        return Ultra

    queens = self.get_units_by_type(obs, units.Zerg.Queen)
    print ("numero de reina",len(queens))
    if len(queens) <1:
        if self.unit_type_is_selected(obs, units.Zerg.Lair):        
            if self.can_do(obs,actions.FUNCTIONS.Train_Queen_quick.id):
                return actions.FUNCTIONS.Train_Queen_quick("now")
        
    else :
        
        Ultralisk =  self.get_units_by_type(obs, units.Zerg.Ultralisk)
        zerglings =  self.get_units_by_type(obs, units.Zerg.Zergling)
        hydras = self.get_units_by_type(obs, units.Zerg.Hydralisk)
        Hatchery = self.get_units_by_type(obs, units.Zerg.Hatchery)
        Hive = self.get_units_by_type(obs, units.Zerg.Hive)

        print ("numero de hydras ", len(hydras))
        print ("numero de zerglings ", len(zerglings))

        if len(Hive) == 1 and len(Hatchery) == 0 :
            Hatchery = self.my_Hatchery_2(obs)
            if Hatchery:
                return Hatchery

        if len (hydras) < 9  :
            zergling_attack = self.my_attack1(obs)  

            if zergling_attack:
                print("zeratacando")
                return zergling_attack

        if len(Ultralisk) <2:
            make_units = self.my_more_units(obs,"Ultralisk")
            if make_units:
                return make_units 

        if len(zerglings) - len(hydras) <= 2 :
            make_units = self.my_more_units(obs,"zergling")
            if make_units:
                return make_units 
        else:  
            if len (hydras) > 9  :
                all_attack = self.my_attack(obs)  
                if all_attack:
                    print("all attack")
                    return all_attack

            hatchery_evolu = self.get_units_by_type(obs, units.Zerg.Lair)   
            if len(hatchery_evolu) <1 :
                if hatchery_evolu:
                    return hatchery_evolu 
            make_units = self.my_more_units(obs,"hydralisk")
            if make_units:
                return make_units

    return actions.FUNCTIONS.no_op()  #do not do anything if there were no matches

def main(unused_argv):
  agent = ZergAgent()
  try:
    while True:
      with sc2_env.SC2Env(
          map_name="Simple64",
          players=[sc2_env.Agent(sc2_env.Race.zerg),
                   sc2_env.Bot(sc2_env.Race.random,
                               sc2_env.Difficulty.medium)],
          agent_interface_format=features.AgentInterfaceFormat(
              feature_dimensions=features.Dimensions(screen=84, minimap=64),
              use_feature_units=True),
          step_mul=10,
          game_steps_per_episode=0,
          visualize=True) as env:
          
        agent.setup(env.observation_spec(), env.action_spec())
        
        timesteps = env.reset()
        agent.reset()
        
        while True:
          step_actions = [agent.step(timesteps[0])]
          if timesteps[0].last():
            break
          timesteps = env.step(step_actions)
      
  except KeyboardInterrupt:
    pass
  
if __name__ == "__main__":
    app.run(main)
