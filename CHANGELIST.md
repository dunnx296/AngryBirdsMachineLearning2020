### List of Changes (release alpha v0.3.7)
1. Shooting related commdands changed
    - only release point is needed
2. ReportNoveltyLikelihood command is extended
    - novelty object IDs 
    - novelty level
    - novelty description 
3. After loading a new game instance, the first groun truth will be returned after the scene is fully zoomed out
4. Novelty level 3 type 7 is not working in 0.3.6. It has been fixed in this version 
5. Adapted DQ agent to the new interface
### List of Changes (release alpha v0.3.6)
1. Development mode is added
  - use --dev when running the game playing interface to access more information about the game objects
  - under dev mode, the type of the object in the ground truth is the true object type
  - under dev mode, agent command groundtruthwithscreenshot and groundtruthwithoutscreenshot will return non-noisy groundtruth
  - under dev mode, agent command ShootAndRecordGroundTruth will return non-noisy groundtruth
2. Coordination system of the agent and the science birds game is consistent
3. The log of the science birds game can be found in the same folder as the game executable, named sciencebirds.log
4. The ground truth json format has been changed to GeoJSON inspired format (the differences can be found in README.md). Details about the new format is here[link] (an example of the new format can be found here[link]). 
5. The published novelty level 3 type 7 has been fixed
6. Add command line argument --agent-port that specify the port for the agent to connect
7. The old argument --agent-start-port has been renamed to --game-start-port to prevent misunderstanding

### List of Changes (release alpha v0.3.5)
1. Add --headlesss command line argument for that gameplayinginterface.jar that run the system headless
2. Reduce noise level to up to 2 pixels for the objects in the noisy ground truth
3. Change the object IDs in the groundtruth to unique IDs for each object that can be used for object tracking
4. Change the vertices representation for objects in the ground truth to a list of contours. Each contour contains a list of vertices.
5. Speed up the ground truth generation from ~100 (80 headless) ms/frame to ~30 (20 headless) ms/frame

### List of Changes (release alpha v0.3.4)
21st June 2020
1. Fixed the science birds game (SB) and game playing interface (GPI) crash bug when the batch ground truth request sent but the shot is not being executed.
    - one ground truth will be returned in such case
2. Fixed SB crash bug when sending zoom out request sometimes
3. The game level will be fully zoomed out by default after loading
4. Changed configMeta.xml format  (see README.md for details)
5. Changed game level name format
6. Allow multiple agents to connect to one GPI.
    - SB do not need to be started by the user, instead, one SB instance will be started automatically by the GPI when an new agent is connected to the GPI 
    - A few command line arguments were added to the GPI (see README.md for details)
7. Removed unstable game levels from the sample game levels

### List of Changes (release alpha v0.3.3)
19th May 2020
1. Add a new requet to send a batch of ground truths per n frames after a shot

### List of Changes (release alpha v0.3.0)
7th Apr 2020
1. Add test harness which generates test trials and send specific requests to the agent to perform the test trial
2. Add 6 new states and 3 requests related to test harness 

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
