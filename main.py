import logging
import src.demo.naive_agent_groundtruth as na

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    agent = na.ClientNaiveAgent()
    agent.run()
