import json
import matplotlib.pyplot as plt

with open("timings-dict.json", "r") as timings_file:
    timings_dict = timings_file.read()
alg_to_time_dict = json.loads(timings_dict)

markers = ['s', '^', '*']
colours = ['blue', 'orange', 'green']


graph1 = plt.figure()
plt.xlabel("Number of opponents" )
plt.ylabel("log(Execution time) (seconds)")
plt.title("A plot to illustrate the log time taken to execute the tournaments")
for (algorithm, time), marker, colour in zip(alg_to_time_dict.items(), markers, colours):
    plt.semilogy(range(1, 10), time, marker=marker, color=colour, label=algorithm) 
plt.legend(title='Algorithm used to calculate Nash equilibria')
#plt.show()
graph1.savefig("../../images/log-timing-graph.pdf")


graph2 = plt.figure()
plt.xlabel("Number of opponents" )
plt.ylabel("Execution time (seconds)")
plt.title("A plot to illustrate the time taken to execute the tournaments")
for (algorithm, time), marker, colour in zip(alg_to_time_dict.items(), markers, colours):
    plt.plot(range(1, 10), time, marker=marker, color=colour, label=algorithm) 
plt.legend(title='algorithm used to calculate Nash equilibria')
#plt.show()
graph2.savefig("../../images/timing-graph.pdf")