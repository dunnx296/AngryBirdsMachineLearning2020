# Science Birds Basic Game Playing Software
#### <p style="text-align: center;"> Alpha v 0.3.0 </p>

## Table of contents
1. [Requirements](#Requirements)
	1. [Java Environment](#Java)
	2. [Python Environment](#Python)
	3. [The Science Birds Game](#SB)
2. [Run the Agent](#Run)
3. [Level Generation](#Level)
4. [Novel Levels Loading](#Novel)
5. [Outline of the Provided Files](#Files)
6. [Outline of the Agent Code](#Code)
7. [Ground Truth Data Structure](#Groundtruth)
8. [Agent-Game Communication Protocols](#Protocol)

## Requirements<a name="Requirements"></a>
This system has been tested on
- Ubuntu 18.04
- MacOS 10.9 and 10.12
- Windows 10
#### Java Environment<a name="Java"></a>

The framework has been tested with the Java 12 and above.

Java Environment can be downloaded  from [this link](http://www.oracle.com/technetwork/java/javase/downloads/index.html).

#### Python Environment<a name="Python"></a>
- python version>=3.6
- numpy
- shapely
- open cv
- tensorflow
- install the dependencies

<code>pip3 install -r requirements.txt</code>

#### The Science Birds Game<a name="SB"></a>
Pre-compiled Science Birds for different platforms are in folder:

<code>ScienceBirds</code>

## Run the Agent<a name="Run"></a>
1. Run the game playing interface
	- the runnable jar file is in the root folder of the repository called game_playing_interface.jar
	- use the code below to run:

<code>java -jar  game_playing_interface.jar</code>

2. Run the Science Birds game executable file to start a game instance
	- The Science Birds game used in this framework is a modified version of Lucas N. Ferreira's work that can be found in his [Github repository](https://github.com/lucasnfe/science-birds)
3. Run the Python naive agent 

<code>python3 main.py</code>

4. Run the Python deep Q-learning agent 
    - The dq agent is placed in ./src/demo/ddqn_test_harness_agent.py
    - To run it: <code>python3 ddqn_test_harness_agent.py</code>

5. Eagle Wings
    - The eagle wings agent is located in the [science birds repository](https://gitlab.com/aibirds/sciencebirds)
    - A readme file on running the agent is included in the agent's zip file

## Generate Levels<a name="Level"></a>
1. Game levels are stored in the folder:
	- Linux
	
	<code>ScienceBirds_Linux/ScienceBirds_Linux_Data/StreamingAssets/Levels/</code>
	- MacOS
	
	<code>ab.app/Contents/Resources/Data/StreamingAssets/Levels/</code>
	- Windows

	<code>ScienceBirds_Win/Science Birds_Data/StreamingAssets/Levels/</code>

2. Game levels can be dynamically added or removed to the above folder during the running of the [pipeline](#Run)
3. New levels can be generated by running 

<code>python3 IratusAves.py</code>

in folder levelgenerator
  - the level generator is based on Matthew Stephenson's work. 
  - the latest changes on the level generator can be found in his [repository](https://github.com/stepmat/IratusAves/tree/Sail-on) 

4. A brief description about the level generator is [here](#generate)
5. A detailed description of the level generator is [here](levelgenerator/README.md)

## Novel Levels Loading<a name="Novel"></a>
1. In science birds game Levels folder as shwon in the previous [section](#Level), there will be a set of folders named novelty_level_*
2. In each of these folders, there will be a set of folders named type*
3. Each set of novel levels are placed in one type* folder which contain two subfolders:  [asset bundle] and [levels]
4. By default, there are 2600 levels pre-installed, where the first 200 levels are non-novelty levels used for generating the novelty levels
5. To change to levels installed: simply add/remove the type* folders. This operation can be done at the run time of the game


## Outline of the Provided Files <a name="Files"></a>
This framework provided the following components:
1. The python naive agent 
	- setup.py in root folder ./
		- the setup file for the python naive agent
	- requirements.txt in root folder ./
		- the dependencies for the python naive agent
	- all source code of the agent is in ./src and will be explained in detail in a [separate section](#Code)
2. The game playing interface 
	- game_playing_interface.jar in root folder ./
		- the compiled game playing interface that handles commnication between the agent and the Science Birds game	 
3. The Science Birds game
	- three (Linux, MacOS and Windows) versions of the science birds game are provided in ./ScienceBirds
4. The level generator<a name="generate"></a>
	- located in ./levelgenerator
	- use the command:

	<code>python3 IratusAves.py</code>
	
	to generator levels

	- The levels will be generated into the same folder as the IratusAves.py
	- Currently the generated levels can be directly copied into the [game level folders](#Level) 
## Outline of the Agent Code <a name="Code"></a>
The ./src folder contains all the source code of the python naive agent. The agent is called naive agent because it ignores all other objects in the game but only aims and shoots at the pigs. Below is the outline of the code (this is a simple description. Detailed documentation in progress):
1. Files under ./src/demo/
	- naive_agent_groundtruth.py
		- A naive agent that interacts with the game by the pre-defined protocols
2. Files under ./src/client/
	- agent_client.py
		- it encodes the commands from the naive agent to send to the interface
		- it decodes the received interface messages into corresponding python object
	- server_client_config.json
		- the config file for the agent-interface connection
3. Files under ./src/trajectory_planner/
	- trajectory_planner.py
		- The implementation of the trajectory module
		- It calculates two possible trajectories given a directly reachable target point
		- It returns None if the target is non-reachable by the bird
4. Files under ./src/computer_vision
	- VisionMBR.py
		- image segmenting component that outputs a list of minimal bounding boxes (MBRs) to represent objects of a screenshot
	- VisionRealShape.py
		- image segmenting component that outputs a list of real shapes to represent objects a screenshot
	- ImageSegmentor.py
		- Implementation of region growing based image segmentation
	- GroundTruthReader.py
		- Parse the ground truth json object
		- Ground gruth data structure is detailed in [this section](#Groundtruth)
	- game_object.py
		- classes for representing game objects
	- cv_utils.py
		- utilities for vision
5. Files under ./src/utils
	- Point2D.py
		- A simple 2d point class used by the naive agent and the trajectory planner
6. ./main.py
	- main entry to run the agent

## The Game Environment<a name="Env"></a>
1. The coordination system
	- in the python naive agent and the game playing interface, the game objects are represented in a Cartesian coordinate system with the origin point to be up-left corner. X coordinate increases along the right direction and Y coordinate increases along the downwards direction.
	- in the science birds game, the origin point (0,0) is the buttom-left corner and the Y coordinate increases along the upwards direction, otherwise the same as above.
	- this is to preserve compatibility with the existing game agents based on the Chrome game. We plan to change the coordinate system of ScienceBirds to match the default coordinates (origin at top left).

## Ground Truth Data Structure<a name="Groundtruth"></a>

1. Ground truth data of game objects are stored in a Json object. The json object describs an array where each element describes a game object. Game object categories and their properties are described below:
	- Ground: the lowest unbreakable flat support surface 
		- property: id = 'object [i]' 
		- property: type = 'Ground'
		- property: yindex = [the y coordinate of the ground line]
	- Platform: Unbreakable obstacles
		- property: id = 'object [i]'	
		- property: type = 'Object'
		- property: vertices = [a list of ordered 2d points that represents the polygon shape of the object]
		- property: colormap = [a list of compressed 8-bit (RRRGGGBB) colour and their percentage in the object]
	- Trajectory: the dots that represent the trajectories of the birds
		- property: id = 'object [i]'
		- property: type = 'Trajectory'
		- property: location = [a list of 2d points that represents the trajectory dots]

	- Slingshot: Unbreakable slingshot for shooting the bird
		- property: id = 'object [i]'
		- property: type = 'Slingshot'
		- property: vertices = [a list of ordered 2d points that represents the polygon shape of the object]
		- property: colormap = [a list of compressed 8-bit (RRRGGGBB) colour and their percentage in the object]
	- Red Bird:
		- property: id = 'object [i]'
		- property: type = 'Object'
		- property: vertices = [a list of ordered 2d points that represents the polygon shape of the object]
		- property: colormap = [a list of compressed 8-bit (RRRGGGBB) colour and their percentage in the object]	
	- all objects below have the same representation as red bird
	- Blue Bird:
	- Yellow Bird:
	- White Bird:	
	- Black Bird:
	- Small Pig:
	- Medium Pig:
	- Big Pig:
	- TNT: an explosive block
	- Wood Block: Breakable wooden blocks
	- Ice Block: Breakable ice blocks
	- Stone Block: Breakable stone blocks
	
2. ./src/computer_vision/GroundTruthReader.py is sample tool to read the parse ground truth json object. The coordination system are from the Science Birds and has been converted to the agent's coordination system.
3. Round objects are also represented as polygons with a list of vertices
4. Ground truth with noise
	- If noisy ground truth is requested, the noise will be applied to each point in vertices of the game objects except the **ground**, **all birds** and the **slingshot**
	- The noise for 'vertices' is applied to all vertices with the same amount within 5 pixels
	- The colour map has a noise of +/- 2%. 
	- The colour is the colour map compresses 24 bit RGB colour into 8 bit
	    - 3 bits for Red, 3 bits for Green and 2 bits for Blue
		- the percentage of the colour that accounts for the object is followed by colour
		- example: (127, 0.5) means 50% pixels in the objects are with colour 127  
	- The noise is uniformly distributed
	- We will later offer more sophisticated and adjustable noise. 
## Communication Protocols<a name="Protocol"></a>

<table style="text-align:center;">
    <thead>
        <tr>
            <th>Message ID</th>
            <th>Request</th>
            <th>Format (byte[ ])</th>
			<th>Return</th>
			<th>Format (byte[ ])</th>
        </tr>
    </thead>
    <tbody>
		<tr>
			<td>1-10</td>
			<td colspan=4>Configuration Messages</td>			
		</tr>	
		<tr>
			<td>1</td>
			<td>Configure team ID<br /> Configure running mode</td>
			<td>[1][ID][Mode]<br />ID: 4 bytes<br />Mode: 1 byte<br/>
			COMPETITION = 0<br/>TRAINING = 1</td>
			<td> Four bytes array.<br />
			The first byte indicates the round;<br />
			the second specifies the time limit in minutes;<br />
			the third specifies the number of available levels<br /></td>
			<td>[round info][time limit][available levels]<br />
			Note: in training mode, the return will be [0][0][0].<br />
			As the round info is not used in training,<br />
			the time limit will be 600 hours, <br />
			and the number of levels needs to be requested via message ID 15 
			</td>	
		</tr>	
		<tr>
			<td>2</td>
			<td>Set simulation speed<br />speed$\in$[0.0, 50.0]
			<br />Note: this command can be sent at anytime during playing to change the simulation speed</td>
			<td>[2][speed]<br />speed: 4 bytes</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>	
		</tr>	
		<tr>
			<td>11-30</td>
			<td colspan=4>Query Messages</td>		
		</tr>
		<tr>
			<td>11</td>
			<td>Do Screenshot</td>
			<td>[11]</td>
			<td>Width, height, image bytes<br/>
			Note: this command only returns screenshots without groundtruth </td>
			<td>[width][height][image bytes]<br />width, height: 4 bytes</td>
		</tr>
		<tr>
			<td>12</td>
			<td>Get game state</td>
			<td>[12]</td>
			<td>One byte indicates the ordinal of the state</td>
			<td>[0]: UNKNOWN<br />
			[1] : MAIN_MENU<br />
			[2]: EPISODE_MENU<br />
			[3]: LEVEL_SELECTION<br />
			[4]: LOADING<br />
			[5]: PLAYING<br />
			[6]: WON<br />
			[7]: LOST</td>
		</tr>
		<tr>
			<td>14</td>
			<td>Get the current level</td>
			<td>[14]</td>
			<td>four bytes array indicates the index of the current level</td>
			<td>[level index]
		</tr>
		<tr>
			<td>15</td>
			<td>Get the number of levels</td>
			<td>[15]</td>
			<td>four bytes array indicates the number of available levels</td>
			<td>[number of level]</td>
		</tr>
		<tr>
			<td>23</td>
			<td>Get my score</td>
			<td>[23]</td>
			<td>A 4 bytes array indicating the number of levels <br/> followed by ([number_of_levels] * 4) bytes array with every four<br/> slots indicates a best score for the corresponding level</td>
			<td>[number_of_levels][score_level_1]....[score_level_n]<br/>
			Note: This should be used carefully for the training mode, <br/>
			becaues there may be large amount of levels used in the training.<br/>
			Instead, when the agent is in winning state,<br/>
			use message ID 65 to get the score of a single level at winning state</td>
		</tr>
		<tr>
			<td>31-50</td>
			<td colspan=4>In-Game Action Messages</td>		
		</tr>
		<tr>
			<td>31</td>
			<td>Shoot using the Cartesian coordinates [Safe mode*]<br\>
			</td>
			<td>[31][fx][fy][dx][dy][t1][t2]<br/>
			focus_x : the x coordinate of the focus point<br/>
			focus_y: the y coordinate of the focus point<br/>
			dx: the x coordinate of the release point minus focus_x<br/>
			dy: the y coordinate of the release point minus focus_y<br/>
			t1: the release time<br/>
			t2: the gap between the release time and the tap time.<br/>
			If t1 is set to 0, the server will execute the shot immediately.<br/>
			The length of each parameter is 4 bytes</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>
		</tr>
		<tr>
			<td>32</td>
			<td>Shoot using Polar coordinates [Safe mode*]</td>
			<td>[32][fx][fy][theta][r][t1][t2]<br/>
			theta: release angle<br/>
			r: the radial coordinate<br/>
			The length of each parameter is 4 bytes</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>
		</tr>
		<tr>
			<td>33</td>
			<td>Sequence of shots [Safe mode*]</td>
			<td>[33][shots length][shot message ID][Params]...[shot message ID][Params]<br/>
			Maximum sequence length: 16 shots</td>
			<td>An array with each slot indicates good/bad shot.<br/>
			The bad shots are those shots that are rejected by the server</td>
			<td>For example, the server received 5 shots, and the third one<br/> 
			was not executed due to some reason, then the server will return<br/>
			[1][1][0][1][1]</td>
		</tr>
		<tr>
			<td>41</td>
			<td>Shoot using the Cartesian coordinates [Fast mode**]<br\>
			</td>
			<td>[41][fx][fy][dx][dy][t1][t2]<br/>
			The length of each parameter is 4 bytes</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>
		</tr>
		<tr>
			<td>42</td>
			<td>Shoot using Polar coordinates [Fast mode**]</td>
			<td>[42][fx][fy][theta][r][t1][t2]<br/>
			The length of each parameter is 4 bytes</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>
		</tr>
		<tr>
			<td>43</td>
			<td>Sequence of shots [Fast mode**]</td>
			<td>[43][shots length][shot message ID][Params]...[shot message ID][Params]<br/>
			Maximum sequence length: 16 shots</td>
			<td>An array with each slot indicates good/bad shot.<br/>
			The bad shots are those shots that are rejected by the server</td>
			<td>For example, the server received 5 shots, and the third one<br/> 
			was not executed due to some reason, then the server will return<br/>
			[1][1][0][1][1]</td>
		</tr>
		<tr>
			<td>34</td>
			<td>Fully Zoom Out</td>
			<td>[34]</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>
		</tr>
		<tr>
			<td>35</td>
			<td>Fully Zoom In</td>
			<td>[35]</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>
		</tr>
		<tr>
			<td>51-60</td>
			<td colspan=4>Level Selection Messages</td>		
		</tr>
		<tr>
			<td>51</td>
			<td>Load a level</td>
			<td>[51][Level]<br/>
			Level: 4 bytes</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>
		</tr>
		<tr>
			<td>52</td>
			<td>Restart a level</td>
			<td>[52]</td>
			<td>OK/ERR</td>
			<td>[1]/[0]</td>
		</tr>
		<tr>
			<td>53</td>
			<td>Load next available level</td>
			<td>[53]</td>
			<td>Loaded Level Index</td>
			<td>[level index]<br/>
			level index: 4 bytes</td>
		</tr>
		<tr>
			<td>61-70</td>
			<td colspan=4>Science Birds Specific Messages</td>		
		</tr>
		<tr>
			<td>61</td>
			<td>Get Ground Truth With Screenshot</td>
			<td>[61]</td>
			<td>ground truth and corresponding screenshot</td>
			<td>[groundtruth byte array length][ground truth bytes][image width][image height][image bytes]<br/>
			groundtruth byte array length: 4 bytes<br/>
			image width: 4 bytes
			image height: 4 bytes</td>
		</tr>
		<tr>
			<td>62</td>
			<td>Get Ground Truth Without Screenshot</td>
			<td>[62]</td>
			<td>ground truth</td>
			<td>[groundtruth byte array length][ground truth bytes]</td>
		</tr>
		<tr>
			<td>63</td>
			<td>Get Noisy Ground Truth With Screenshot</td>
			<td>[63]</td>
			<td>noisy ground truth and corresponding screenshot</td>
			<td>[groundtruth byte array length][ground truth bytes][image width][image height][image bytes]</td>
		</tr>
		<tr>
			<td>64</td>
			<td>Get Noisy Ground Truth Without Screenshot</td>
			<td>[64]</td>
			<td>noisy ground truth</td>
			<td>[groundtruth byte array length][ground truth bytes]</td></tr>
		<tr>
			<td>65</td>
			<td>Get Current Level Score</td>
			<td>[65]</td>
			<td>current score<br/>
			Note: this score can be requested at any time at Playing/Won/Lost state<br/>
			This is used for agents that take intermediate score seriously during training/reasoning<br/>
			To get the winning score, please make sure to execute this command when the game state is "WON"</td>
			<td>[score]<br/>
			score: 4 bytes</td>
		</tr>
		<tr>
			<td>66</td>
			<td>Report Novelty Likelihood</td>
			<td>[66][novelty_likelihood][non_novelty_likelihood]<br/>
			The length of each parameter is 4 bytes</td>
			<td>OK/ERR</td/>
			<td>[1][0]</td>
		</tr>
		<tr>
			<td>67</td>
			<td>Report Novelty Description</td>
			<td>[67][msg_length][novelty_description]<br/>
			msg_length:4 bytes int<br/>
			novelty_description:[msg_length] bytes string</td>
			<td>OK/ERR</td/>
			<td>[1][0]</td>
		</tr>
		<tr>
			<td>68</td>
			<td>Ready for New Set</td>
			<td>[68]</td>
			<td>a 18 bytes array indicating the time limit, interaction limit, number of levels, if in training or testing mode and if levels are sequenced or as a set</td/>
			<td>[time_limit]:4 bbytes integer<br/>
			[interaction_limit] 4 byte integer<br/>
			[#levels] 4 bytes integer<br/>
			[attempts_per_level]4 bytes integer<br/>
			[mode] 1 byte, 0 -> training, 1 -> testing <br/>
			[if_as_a_set]:1 byte, 0 -> set, 1 -> sequence 
			</td>
		</tr>
		<tr>
			<td colspan=5>* Safe Mode: The server will wait until the state is static after making a shot.</td>
		</tr>
		<tr>
			<td colspan=5>** Fast mode: The server will send back a confirmation once a shot is made. 
			The server will not do any check for the appearance of the won page.</td>
		</tr>


	</tbody>

</table>
