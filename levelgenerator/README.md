# IratusAves (MSGv2.0)
Winning entry for the 2017 and 2018 AIBIRDS level generation competitions:
https://aibirds.org/other-events/level-generation-competition.html

Used to generate levels for the Science-Birds game by Lucas N. Ferreira:
https://github.com/lucasnfe/Science-Birds

Please note that the agent performance and stability analysis features have been removed due to compatability issues.

The number and content of the generated levels can be changed by altering the parameters.txt file.
This file contains the necessary information about the levels that will be generated.
This information is provided in blocks of four lines, with each block containing the following information in the given order
- The starting index of level name
- Number of levels to generate (positive integer)
- Forbidden block and material combinations (list of valid materials/block types, may be empty)
- Range for number of pigs (two positive integers, minimum and maximum)
- Time limit to generate levels (minutes) (positive integer)

Note that for this generator version the "Time limit" parameter makes no difference to the generated content.


![Alt text](/example_screenshots/1.PNG?raw=true "example generated level #1")

![Alt text](/example_screenshots/2.png?raw=true "example generated level #2")

![Alt text](/example_screenshots/3.png?raw=true "example generated level #3")

![Alt text](/example_screenshots/4.png?raw=true "example generated level #4")
