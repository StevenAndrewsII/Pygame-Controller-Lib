# Pygame-Controller-Lib
A full library to support multi-controllers in pygame!

This library was created to allow multiple gamepad objects to interface with Pygame. 
( Native support for Xbox controllers ) 



Features:

> Unlimited connected controler support 

> time out ( awating controllers time out )

> Virtual port time put ( dead controller detection )

> Multi controller rumble support 

> Remap/ macro support

> Full API settings 

-----------------------------------------------------------------------------------

Functions list: ( External use ) 

Get_button          (      port_id   ,   button   )                                     
>> Gets the selected button state of a controller at a virtual port

Get_axis            (      port_id   ,   axis     )                                     
>> Gets the selected axis positions of a controller at a virtual port  

Get_stick_angle     (      port_id   ,   axis     )                                     
>> gets the stick angle in degrees about the center dead zone of stick 

Set_rumble          (      port_id   ,   [ motor_L,motor_R,duration in seconds  ] )     
>> Set the rumble of a controller on a port ( motor power 0 -> 1 )



