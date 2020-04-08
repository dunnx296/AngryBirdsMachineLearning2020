import sys

import src.demo.naive_agent_groundtruth as na

def main(*args):
	print ('naive agent running')
	agent = na.ClientNaiveAgent()
	agent.run()

if __name__ == "__main__":
	main()
