### List of Changes (release alpha v0.1.1) 
19th Feb 2020 

1. Protocol #23 (Get my score) format is changed
    - a 4 bytes array indicating the number of levels is added in front of the score bytes array

2. Naive agent and DQ agent are adapted

### List of Changes (release alpha v0.1) 
10th Feb 2020 

This is a brief introduction of what has been changed in this version. Please refer to the [README](https://gitlab.com/sail-on-anu/sciencebirdsframework_release/-/blob/release/alpha-0.1/README.md) file for details.

1. Speed up
    - a new protocol code is added to change the simulation speed of Unity
    - a speed of d $\in$ (0 - 50] is allowed
            - where d $\in$ (0, 1) means to slow down the simulator for 1/d times
            - d = 1 means the normal speed
            - d $\in$ (1, 50] means to speed up the simulation for d times  
    
2. The change of (noisy) groundtruth representation  
    - add trajectory points
    - change object type representation
        - object other than ground, slingshot
    - add colour distribution
3. Headless run
    - graphic-free science birds can be produced by a server build from Unity 
    - the headless run should not need any spectial command using the server build version of science birds
4. Baseline agents are added including:
    - Eagle Wings (Planning)
    - DQ agent (Deep Q learning)

5. Score changing problem after WON/LOST banner shown up is solved
6. Protocol code 13 (get best score) has been removed as it performs the same as 23 (get my score) given only one agent will play the game.


