import scipy.stats as stats
import matplotlib.pyplot as plt

def bayesian():
    m = 5   # number of iterations
    s = 20  # number of states
    
    """
    {s0 : {
	        s1: 0.0,
	        s2: 0.0,
	        s3: 1.0,
	      }
    }
    """

    # dictionary {
    #     alfa1 : integernumber,
    #     ...
    #     alfan : integernumber
    # }
    dictionary = dict()


    for i in range(s):
        dictionary["s% s" % i] = dict()
        for j in range(4):
            dictionary["s% s" % i]["s% s" % j] = 2      # TODO: second index should correspond to the correct (target) state number instead of 
                                                        #   	0,..,4 for each transition within state i

    for k in range(m):
        for i in range(s):
            for j in range(4):
                current_alfa = dictionary["s% s" % i]["s% s" % j]
                disctionary["s% s" % i]["s% s" % j] = current_alfa + calculate_probability(i, current_alfa, j) # TODO: second index should correspond to the correct (target) state number instead of 
                                                                                                              #   	0,..,4 for each transition within state i

    # P(s1, alfa, s) for each dictionary -> dictionary of alfa should be updated by: alfa = alfa + P(s1, alfa, s)

def calculate_probability(source_state, alfa, target_state):

