### List of Changes (release alpha v0.2.1)
5th Mar 2020

1. Modified the method of loading novelty levels.
    - now novelty levels with different novlety levels/types can be loaded at the same time
    - the combination of the level sets can be flexibly rearranged  

### List of Changes (release alpha v0.2.0)
28th Feb 2020

1. Added capability of reading novlety level 1-3 with 1200 sample levels
    -  Level 1: new objects with 5 novelty type samples provided (100 levels for each)
    -  Level 2: change of parameters of objects with 5 novelty type samples provided (100 levels for each)
    -  Level 3: change of representation with 2 novelty type samples provided (100 levels for each)
    - The original non-onvelty levels are also provided for comparasion
    - Note: the source code of the novelty generator is not included in the release
    - The instruction of loading novelty levels is in the Novel Levels Loading section of README.md 
2. Fixed cshoot return shoot successfully indicator before the level is stable problem. 
    - now the return value for cshoot/pshoot will be returned once the not objects in level is moving
    -  now the return value for cfastshoot/pfastshoot will be returned after the shoot procedure is finished, i.e., the drag and tap operations are executed 
3. Fixed science birds error message display bug 

### List of Changes (release alpha v0.1.2)
21th Feb 2020

1. The agent now can register an observer agent on port 2006 which allows the user to request the screenshots/groundtruth from another thread.
    - the observer agent can only execute 6 commands: configure (1), DoScreenshot (11) and the four groundtruth related (61-64)
    - the demo code of using this function is in src/demo/naive_agent_groundtruth.py line 53-81 and 153-154


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
