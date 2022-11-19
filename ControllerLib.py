class PyGC(object):
    """     Controller Module       """
    """ 
    // #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            This API is created to handle  "virtual port(s)"  interactions and automate handeling with multiple controller inputs using pygame as input backend.
    // #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #       External Utility fuctions:
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    #       Get_button          (      port_id   ,   button   )                                     Gets the selected button state on a virtual port                             ( returns remmaped state if has set remmaped )
    #       Get_axis            (      port_id   ,   axis     )                                     Gets the selected axis position on a virtual port                            ( not nomrally used externally for sticks : used for L/R triggers )       
    #       Get_stick_angle     (      port_id   ,   axis     )                                     gets the stick angle in degrees about the center dead zone of the stick      ( used normally for sticks )
    #       set_rumble          (      port_id   ,   [ motor_L,motor_R,duration in seconds  ] )     Set the rumble of a controller on a port ( motor power 0 -> 1 )
    #       
    #       
    #       Update_             (      NA      )                                                    Limit speed in main loop // internal system updater ( match set fps )
    #                                                                                               * NOTE:
    #                                                                                               In settings timings must be multiplied by the set frame rate number 
    #                                                                                               Example:  4 seconds * 120 FPS  -> this allows the timers to function 
    #
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #      Initializing the lib: ( copy and paste )
    #               
    #               import Math                 # import required libraries 
    #               import pygame
    #               import PygameController
    #            
    #               PyGC__     =     PygameController.PyGC(  pygame , math , # of controllers (int) , fps reference (int) )
    #      
    #
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    API Writen By:                                   Steven Andrews II
    Project By:                                   [[ Steven Andrews II ]]                                       - Fall 2022 
    // #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """ 

    
    

    def __init__(   self    ,   pygame  ,  math ,  number_of_ports , set_fps ):
    #       load and defined defualt varables for lib 

       self.pygame                          = pygame                                #   load modules pushed from start of the class
       self.math                            = math                                  #   standard math lib
       
       #    Lib/ port settings  ( editable )
       self.settings = {
           "time_out_"                      :120 *set_fps,                          #   timeout state for controllers awaiting an open port
           "port_activity"                  :120 *set_fps,                          #   timeout state for virtual ports with dead or non active controllers 
           "port_activity_deley"            :1   *set_fps,                          #   deley that the activity atate will hold before resetting 
           "port_read_deley"                :10,                                    #   over read on USB port from event call                         ( safty, if unsure leave at 10 frames )  
           "stick_deadZone"                 :.3                                     #   stick sensitivity  
           "set_fps"                        :set_fps                                #   set to your FPS
       }
      
       #    variabls 
       self.controllers_                    = { 0 : {} , 1 : {} }                   #   Controller buffer // holds raw hardware objects   [  0 = joystick object  // 1 = connection timers  ]
       self.gamepad_count                   = pygame.joystick.get_count()           #   Indexing 
       self.port_read                       = False                                 #   read from port state
       self.port_read_t                     = 0                                     #   read timer 

  
       # Port generation and default macro  ( native supports Xbox )         
       self.port_ = { } # default constructors 
       self.mac_ = { }
       for i in range(number_of_ports):
           self.port_[i] = {  
                "attached"                  : "none" ,                              #   unique attached controller ID
                "hat_num"                   : 0 ,                                   #   hat buttons index length for controller 
                "axis_num"                  : 0  ,                                  #   axis index length for controller 
                "button_num"                : 0 ,                                   #   buttons index length for controller 
                "activity"                  : False ,                               #   Activity status of the port
                "act_t"                     : 0 ,                                   #   internal clk
                "act_lt"                    : 0 ,                                   #   internal clk
                "rumble_state"              : False,                                #   rumble toggle state 
                "rumble_t"                  : 0,                                    #   internal clk
                "rumble_dur"                : 0,                                    #   duration in seconds - for rumble 
                "L_motor"                   : 0,                                    #   rumble motor strngth 
                "R_motor"                   : 0,                                    #   rumble motor strngth 

            }

           self.mac_[i] = {
               "buttons" : {
               "A"              : {    "map_" : "A"  , "state" : False  ,  "index_" : 0   },
               "B"              : {    "map_" : "B"  , "state" : False  ,  "index_" : 1   },
               "X"              : {    "map_" : "X"  , "state" : False  ,  "index_" : 2   },
               "Y"              : {    "map_" : "Y"  , "state" : False  ,  "index_" : 3   },
               "LB"             : {    "map_" : "LB" , "state" : False  ,  "index_" : 4   },
               "RB"             : {    "map_" : "RB" , "state" : False  ,  "index_" : 5   }, 
               "BB"             : {    "map_" : "BB" , "state" : False  ,  "index_" : 6   }, #   back
               "ST"             : {    "map_" : "ST" , "state" : False  ,  "index_" : 7   }, #   start
               "LS"             : {    "map_" : "LS" , "state" : False  ,  "index_" : 8   },
               "RS"             : {    "map_" : "RS" , "state" : False  ,  "index_" : 9   }, 
               },

               "axis" :{
         
                   "L_stick" : { #  touple return 
                       "y"         : {    "val" : 0,   "invert": 1   ,  "index_" : 1   }, # note: invert = -1 or 1 only !
                       "x"         : {    "val" : 0,   "invert": 1   ,  "index_" : 0   },
                   },
           
                   "R_stick" : { #  touple return
                       "y"         : {    "val" : 0,   "invert": 1  ,  "index_" : 3    },
                       "x"         : {    "val" : 0,   "invert": 1  ,  "index_" : 2    },
                   },

                   "LT"            : {    "map_" : "LT" , "val" : 0  ,  "index_" : 4   },
                   "RT"            : {    "map_" : "RT" , "val" : 0  ,  "index_" : 5   },
               } 
           } #// EO_0 

    


    #-------------------------------------------------------------------------------------------------------------------
    # INTERNAL FUNCTIONS:   Virtual Port && Controller Handlers/MAnagers:
    #-------------------------------------------------------------------------------------------------------------------
   

    '''///        Handle new devices into dict       ///'''
    def plugged(self,j):
         if len(self.controllers_[0]) > 0 and self.port_read == False:
             sum        = 0 #           Track found items
             index      = 0 #           End of trce tick
             for k,v in self.controllers_[0].items():
                   index = index+1
                   if "ID_"+str(j.get_instance_id()) == k :  
                           sum = sum+1 
                           break
                   if "ID_"+str(j.get_instance_id()) != k  and sum == 0 and index >= len(self.controllers_[0]) :
                                print("Added controller:1 "+"ID_"+str(j.get_instance_id()))
                                self.controllers_[0].update(  { "ID_"+str(j.get_instance_id()) : j }  )
                                self.controllers_[1].update(  { "ID_"+str(j.get_instance_id()) : 0 }  )
                                break               
         elif len(self.controllers_[0]) == 0:
                print("Added controller:0 "+"ID_"+str(j.get_instance_id()))
                self.controllers_[0].update(  { "ID_"+str(j.get_instance_id()) : j }  ) 
                self.controllers_[1].update(  { "ID_"+str(j.get_instance_id()) : 0 }  )
                self.port_read = True
                return




    '''///        Auto removes IDs from dict on uplugging       ///'''
    def unplugged(self,i):
        for k,v in self.controllers_[0].items():
             if k == "ID_"+str(i):
                print("controller_   "+k+"  uplugged...")
                self.controllers_[0].pop("ID_"+str(i))
                self.controllers_[1].pop("ID_"+str(i))
                return
               



    '''///       handle dead controller ids not on port // controller state machine      ///'''
    def time_out(self):
            for k,v in self.controllers_[0].items():
                # only operates on controllers not on ports 
                index = 0
                for i in range(len(self.port_)):
                     if k == self.port_[i]["attached"]:
                         index = index +1
                if i == len(self.port_)-1 and index == 0:
                    if  self.controllers_[1][k] < self.settings["time_out_"]:
                        self.controllers_[1][k]         =       self.controllers_[1][k]     +   1
                    elif self.controllers_[1][k] >= self.settings["time_out_"]:
                         print("controller_   "+k+"  timed out, was removed")
                         self.controllers_[0].pop(k)
                         self.controllers_[1].pop(k)
                         break




    '''///       Manage the virtual ports // state machine    (super fast)  ///'''
    def port_manager(self):
        #   hardware port over read deley ( deleys the read from the event call from hardware read in pygame )
        if self.port_read == True :
             self.port_read_t =self.port_read_t+1
             if self.port_read_t >= self.settings["port_read_deley"]:
                    self.port_read = False
                    self.port_read_t = 0
        #   port auto handlers 
        for i in range(len( self.port_)):
            if self.port_[i]["attached"] != "none":
                #   port activity state ( state of the controller on a port)        // clear virtual port + remove controller obj
                for k,v in self.controllers_[0].items():
                    if self.port_[i]["attached"] == k:
                        if self.port_[i]["activity"] == False :
                            self.port_[i]["act_t"] = self.port_[i]["act_t"] +1
                            if self.port_[i]["act_t"] >= self.settings["port_activity"]:
                                print("port manager:     Detatched port [   "+ str(i) +"   ] due to inactivity:  ")
                                self.detach_(  i  )     #   pop all && reset
                                self.controllers_[0].pop(k)
                                self.controllers_[1].pop(k)
                                return
                        else: #     reset the activity state 
                                self.port_[i]["act_t"] = 0 
                                self.port_[i]["act_lt"] = self.port_[i]["act_lt"] +1
                                if self.port_[i]["act_lt"] >= self.settings["port_activity_deley"]:
                                    self.port_[i]["activity"]   = False
                                    self.port_[i]["act_lt"]     = 0
                #   dead controller detection on a port                             // clear virtual port
                sum     = 0
                for k,v in self.controllers_[0].items():
                    if self.port_[i]["attached"] != k:
                        sum = sum  + 1 
                    if  sum  >= len(self.controllers_[0].items()):
                        print("port manager:     Detatched dead controller from port [   "+ str(i) +"   ]")
                        self.detach_(  i  )
                if len(self.controllers_[0]) == 0:  # handle no controller 
                        print("port manager:     Detatched dead controller from port [   "+ str(i) +"   ]")
                        self.detach_(  i  )
                 #   auto assign port to next awaiting controller                   // attach to virtual port
            if self.port_[i]["attached"] == "none":
                for k,v in self.controllers_[0].items(): 
                    index = 0
                    for i__ in range(len(self.port_)):
                        if k == self.port_[i__]["attached"]: 
                            index = index+1
                    if i__ >= len(self.port_)-1 and index == 0:
                        print("port manager:    Controller_ "+k+" was bound to port: "+str(i))                                                         
                        self.attach_( i , k )
                        return
                            
                 

        
    '''///       Handles button states & axis values for each controller at port + port activity state update    ///'''
    def input_handler(self):
        for i in range(len( self.port_)):
            if self.port_[i]["attached"] != "none":
                for k,v in self.controllers_[0].items():
                    if k ==  self.port_[i]["attached"]:
                        for k_mac,v_mac in  self.mac_[i]["buttons"].items():
                            v_mac["state"] =  self.controllers_[0][ k ].get_button( v_mac["index_"])
                            if  v_mac["state"] == 1 :
                                self.port_[i]["activity"] = True
                        # triggers 
                        for k_mac_axis,v_mac_axis in self.mac_[i]["axis"].items():
                            if k_mac_axis != "L_stick" and k_mac_axis != "R_stick":
                                v_mac_axis["val"] =  self.controllers_[0][ k ].get_axis( v_mac_axis["index_"])
                                if  v_mac_axis["val"] > 0 : 
                                    self.port_[i]["activity"] = True
                                else:
                                     v_mac_axis["val"]  = 0          
                            else:
                        # sticks 
                                 for stick_k , stick_v in v_mac_axis.items():
                                      stick_v["val"] =  self.controllers_[0][ k ].get_axis( stick_v["index_"])
                                      if stick_v["val"] > self.settings["stick_deadZone"] or stick_v["val"] < -self.settings["stick_deadZone"] : 
                                            self.port_[i]["activity"] = True
                                      else:
                                          stick_v["val"] = 0        




    '''///      Handles rumble for controllers on ports  (durration in seconds)  ///'''
    def rumble_handler(self):
        for k,v in self.port_.items():
            if v["rumble_state"] == True:
                v["rumble_t"]           = v["rumble_t"] + 1
                if v["rumble_t"] >  v["rumble_dur"]*self.settings["set_fps"]:
                   v["rumble_t"]        = 0
                   v["rumble_state"]    = False
                if v["rumble_t"] <= v["rumble_dur"]*self.settings["set_fps"]:
                   for k_,v_ in self.controllers_[0].items():
                       if k_ == v["attached"]:
                           v_.rumble(
                               float(v["L_motor"]),
                               float(v["R_motor"]),
                               1
                               )
                           break


    #-------------------------------------------------------------------------------------------------------------------
    # EXTERNALLY USED FUNCTIONS: 
    #-------------------------------------------------------------------------------------------------------------------


    ''' EXTERNAL UTILITY:                Get button remaps '''
    def get_button(    self,   port_id   ,   button    ):
        if self.port_[port_id]["attached"] != "none":
            for k,v in  self.mac_[port_id]["buttons"].items():
               if k == button :
                   if v["map_"] == button:
                       return v["state"]                               # normal map return 
                   else:
                       for k_,v_ in  self.mac_[port_id]["buttons"].items():
                            if k_ == v["map_"]:
                                return  v_["state"]                    # remapped return 




    ''' EXTERNAL UTILITY:                Get trigger values and stick X/Y ( handles stick inversion )'''
    def get_axis(    self,   port_id   ,   axis    ):
        if self.port_[port_id]["attached"] != "none":
            for k,v in  self.mac_[port_id]["axis"].items():
               if k == axis :
                   if axis == "L_stick" or axis == "R_stick" :
                        return ( v["x"]["val"]*v["x"]["invert"]) , (v["y"]["val"]*v["y"]["invert"] )         # returns a touple ( X & Y stick location abt center )
                   else:
                       if k == axis :
                            if v["map_"] == axis:
                                return v["val"]                                                              # trigger returns single value  ( normal map return )
                            else:
                                for k_,v_ in   self.mac_[port_id]["axis"].items():
                                    if k_ == v["map_"]:
                                        return  v_["val"]                                                    # returns remapped trigger 
                        



    
    ''' EXTERNAL UTILITY:                Get the angle and magnitude about the center of the stick'''
    def get_stick_angle( self, port_id , axis):
        o_ = self.get_axis(int(port_id),str(axis))
        if o_:
            x,y  = o_
            magnitude = (self.math.sqrt(x*x+y*y))

            if magnitude > 1:
                magnitude = 1

            if magnitude != 0 :  
                return abs(self.math.degrees(self.math.atan2(x,y))-180), magnitude
            else:
                return None,None
        return None,None      
     



    ''' EXTERNAL UTILITY:                Set the vibration of a controller on a port'''
    def set_rumble(self,port_id,*args): 
        t    = next(   iter(args) , [1,1,1]  )
        if self.port_[port_id]["attached"] != "none" and self.port_[port_id]["rumble_state"] == False:
            self.port_[port_id]["L_motor"]                  =   t[0]
            self.port_[port_id]["R_motor"]                  =   t[1]
            self.port_[port_id]["rumble_dur"]               =   t[2]
            self.port_[port_id]["rumble_state"]             =   True 
            return True
        else:
            return False
        
    


    #-------------------------------------------------------------------------------------------------------------------
    # INTERNAL QUICK FUNCTIONS: 
    #-------------------------------------------------------------------------------------------------------------------

    ''' INTERNAL UTILITY:                Attach controller to port'''
    def attach_( self , port_id , joy_id ):
                if  self.port_[port_id]["attached"]         ==  "none":
                    self.controllers_[1][str(joy_id)]       =   0                        
                    self.port_[port_id]["attached"]         =   str(  joy_id  ) 
                    self.port_[port_id]["hat_num "]         =   self.controllers_[0][   str(joy_id)     ].get_numhats()
                    self.port_[port_id]["axis_num"]         =   self.controllers_[0][   str(joy_id)     ].get_numaxes()
                    self.port_[port_id]["button_num"]       =   self.controllers_[0][   str(joy_id)     ].get_numbuttons()
                    self.port_[port_id]["activity"]         =   True
                    self.port_[port_id]["act_t"]            =   0
                    self.port_[port_id]["act_lt"]           =   0
                    self.port_[port_id]["rumble_state"]     =   False
                    self.port_[port_id]["rumble_t"]         =   0
                    self.port_[port_id]["rumble_dur"]       =   0
                    self.port_[port_id]["L_motor"]          =   0
                    self.port_[port_id]["R_motor"]          =   0

                    return True
                else:
                    return False
                  


    ''' INTERNAL UTILITY:                Quick-Clear the port  '''
    def detach_( self , port_id  ):
        if self.port_[port_id]:
           self.port_[port_id]["attached"]                  =   "none"
           self.port_[port_id]["hat_num"]                   =   0
           self.port_[port_id]["axis_num"]                  =   0
           self.port_[port_id]["button_num"]                =   0
           self.port_[port_id]["activity"]                  =   False
           self.port_[port_id]["act_t"]                     =   0
           self.port_[port_id]["act_lt"]                    =   0
           self.port_[port_id]["rumble_state"]              =   False
           self.port_[port_id]["rumble_t"]                  =   0
           self.port_[port_id]["rumble_dur"]                =   0
           self.port_[port_id]["L_motor"]                   =   0
           self.port_[port_id]["R_motor"]                   =   0      

           return True 
        else:
           return False


       

    #-------------------------------------------------------------------------------------------------------------------
    # Internal updater: // Externally update at some set/locked FPS
    #-------------------------------------------------------------------------------------------------------------------
    def update_(self):
        # internal state machines 
        self.time_out() 
        self.port_manager()
        self.input_handler()
        self.rumble_handler()
         # Pygame event pull 

        for event in self.pygame.event.get():
                rt = None
                if event.type == self.pygame.JOYDEVICEADDED and not rt:
                     j = self.pygame.joystick.Joystick(event.device_index)
                     rt = self.plugged(j)
                    
                if event.type == self.pygame.JOYDEVICEREMOVED:
                     self.unplugged( event.instance_id )
