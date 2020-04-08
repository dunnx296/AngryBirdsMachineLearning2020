### Evaluation Configuration 
The test harness uses the file config.xml in the science birds game resource folder <code>./StreamingAssets/</code> to determine how trials are run and what restrictions hold. The config.xml file is automatically created after editing the file configMeta.xml in the same folder.
In the following we describe how to initialise configMeta.xml in order to create a set of trials. Different trial settings according to our evaluation proposal can be defined.

Two sample configMeta.xml files are placed in ./ScienceBirds/configMetaSamples.
  - the first one configures a trial containing 100 training levels and 10 test levels as unordered sets with novelty <code>level 1, type 1</code> 
  - the second one configures a trial containing 100 training levels as a sequence with novelty <code>level 1, type 1</code> and two 10-level test sets as two sequences. The first test level sequence has no novelty and the second has the same novelty as the training sequence  
 
#### Trial Generation Parameters Configuration
The parameters for generating test trials are in <code>configMeta.xml</code>

1. Novelty likelihood recording
    - related element: <code>novelty_detection_measurement</code>
    - step: novelty likelihood will be requested every <code>$step$</code> interactions
        - allowed value: Integer
        - <code>step <= 0</code> means no data will be requested 
    - measure_in_training: if the request will be sent in training mode
        - allowed value: "true" or "false"
    - measure_in_testing: if the request will be sent in testing mode
        - allowed value: "true" or "false"
    
2. Trial configuration
    - related element: <code>trial</code>
    - count: the number of trials being generated
        - allowed value: Integer
        - <code>count <= 0</code> means no trial will be generated
    - <code>repeats</code>: the number of times that the trial will be executed during an evaluation before the next trial is started
        - allowed value: Integer
        - <code>repeats <= 0</code> means the trial will not be executed

3. Test checkpoint configuration
    - related element: <code>checkpoint</code>    
    - a checkpoint will be triggered once any limit is met 
    - time limit:
        - allowed value: Integer
        - in seconds
        - value <= 0 means no time limit
     - interaction limit
         - allowed value: Integer
         - value <= 0 means no interaction limit

 4. Training set configuration
     - related element: <code>training</code>
     -  the <code>limits</code> element specifies the overall limits of a the training in a trial
     -  the training will terminate once any limit is met
     - a final test will be performed after termination

     - time limit:
        - allowed value: Integer
        - value <= 0 means no time limit
     - interaction limit
         - allowed value: Integer
         - value <= 0 means no interaction limit
    - attempt per level limit
         - indicates how many attempts an agent can perform on each single level
         - one particular level will become inaccessible if the attempts on this level meets the llimit  
         - if an inaccessible level is being load by the agent, the request will not be executed and 0 will be returned
         - allowed value: Integer
         - value <= 0 means no interaction limit        
    - allow level selection limit
         - indicates if a level set is sequential or unordered
         - allowed value: <code>"true" or "false"</code>
         - true means the levels are unordered
         - false means the levels are as a sequence and can only be accessed in order

5. Test set configuration
      - related element: <code>test</code>
      - attribute <code>ordered</code> specifies if the level sets generated are in the same order as the order in element <code>game_level_set</code>
          - allow value:  <code>"true" or "false"</code>
          - "true" means the test sets are in the same order as configured
          - "false" means the generated test sets are shuffled before putting in config.xml
      - limits
            - except <code>set_appearance_percentage</code>, all other limits are mentioned similar to the previous section
            - <code>set_appearance_percentage</code> is used to calculate the number of test sets being generated in the specific configuration
      - calculation of the number of test sets
          - total_n_testsets = ceiling(training_time_limit/checkpoint_time_limit)+ceiling(training_interaction_limit/checkpoint_interaction_limit)
           - the number of the test sets with a single configuration, i.e., as specified in <code>game_level_set</code> is calculated as:
               - n_testsets = ceiling( total_n_testsets *  set_appearance_percentage /100)
           
                          
### Adapt the Agent
1. Four new requests are added
    - Load next available level: this request is recommended to use when the training/test levels are sequential which cannot be loaded in any order 
    - Report novelty likelihood: report the likelihood of a level set with/without novelty
    - Report novelty description: report other observation from the agent in free string format
    - Ready for new set: this should be sent when the agent is ready for the switch of training/test level sets  
    - encoding details about the new requests are in the <code>Communication Protocols</code> section in README.md
2. Six new states are added:
    - NEWTESTSET = 8
        - a new test set will be loaded 
        - The agent running on test sets should switch off its learning process 
        - this state should be handled by <code>Ready For New Set</code> (68) request when the agent is ready
    - NEWTRAININGSET = 9
        - a new training set will be loaded
        - the agent should backup and remove its trained model and start the training as a fresh one 
        - this state should be handled by <code>Ready For New Set</code> (68) request when the agent is ready
    - RESUMETRAINING = 10
        - the previous training set before checkpoint test will be loaded
        - the agent should switch on its learning process
        - the agent should restore its memory when being paused from the pervious state 
        - this state should be handled by <code>Ready For New Set</code> (68) request when the agent is ready
    - NEWTRIAL = 11
        - the agent should backup and remove its trained model and start as a fresh one
        - the agent should not assume the mode (training, test) of the next problem
        - a NEWTRAININGSET or NEWTESTSET state will follow this state
        - this state should be handled by <code>Ready For New Set</code> (68) request when the agent is ready
    - REQUESTNOVELTYLIKELIHOOD = 12
        - the agent is requested to report the likelihood that the problem set contains or not contains novelty
        - this state should be handled by <code>Report Novelty Likelihood</code>(66) request
        
    - EVALUATION_TERMINATED = 13
        - the evaluation is terminated, the agent should backup itself and exit safely
        
 3. A minimal demo on handling such states are in
       - demo/naive_agent_groundtruth.py 
       - client/agent_client.py
