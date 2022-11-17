# PygameController Lib
A full library to support multi-controllers in pygame!

This library was created to allow multiple gamepad objects to interface with Pygame. 
( Native support for Xbox controllers ) 



Features:

    >      Full controller support                      ( Native Xbox support )
    >      Multi controller support "virtual ports"     ( no set limit )
    >      Controller disconnecton handling             
    >      Controller remapping 
    >      Time out on "virtual ports" 
    >      Awaitng contollers timeout
    >      Muti controller rumble support
    >      Joystick handling
    >      Controller to port auto aisgnment 

-----------------------------------------------------------------------------------

Functions list: ( External use ) 

Get_button          (      port_id   ,   button   )                                     
> Gets the selected button state of a controller at a virtual port

Get_axis            (      port_id   ,   axis     )                                     
> Gets the selected axis positions of a controller at a virtual port  

Get_stick_angle     (      port_id   ,   axis     )                                     
> gets the stick angle in degrees about the center dead zone of stick 

Set_rumble          (      port_id   ,   [ motor_L,motor_R,duration in seconds  ] )     
> Set the rumble of a controller on a port ( motor power 0 -> 1 )


 Update             ( NA )  :  Internal state machine updater : ( call externally in main loop )
> Takes no arguments : limit speed in main loop ( see library for information on settings and timer calibration )






DEV NOTE:
   

    >      Activily developing this further
    >
    >      Future Features:
    >      D-pad support            
    >      Add virtual port  
    >      Remove virtual port
