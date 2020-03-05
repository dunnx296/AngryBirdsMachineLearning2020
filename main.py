import sys

import src.demo.naive_agent_groundtruth as na
import src.demo.ddqn_agent as ddq

def main(*args):
	if ('-dq' in sys.argv):
		print("ddq running")
		agent = ddq.ClientRLAgent()
	else:
		print ('naive agent running')
		agent = na.ClientNaiveAgent()
	agent.run()

if __name__ == "__main__":
	main()
