import main
import time 
import numpy as np
import json

algorithm_to_time_dict = {
    "Support Enumeration": [],
    "Vertex Enumeration": [],
    "Lemke Howson": []
}

game_ending_probs = np.linspace(0.001, 1-0.001, 10)
number_of_opponents = 1

for algorithm in algorithm_to_time_dict:

  # print(algorithm)

  average_running_time = []
  while number_of_opponents <= 9:
    
    # print(number_of_opponents)

    average_running_time_for_same_players = []
    for same_number_of_players_repeat in range(1, 6):
        
     # print(same_number_of_players_repeat)

      players = main.who_is_playing(num_of_opponents=number_of_opponents)
        
      execution_time = []
      for same_opponents_repeat in range(5):

      #  print(same_opponents_repeat)
      #  print(players)

        initial_time = time.perf_counter()
        main.probabilities_of_defection(num_of_repeats=10, player_list=players, probs_of_game_ending=game_ending_probs, nash_equilibrium_algorithm=str(algorithm), set_seed=123)
        final_time = time.perf_counter()
        execution_time.append(final_time - initial_time)
            
      #  print(execution_time)



    #  print("Finished inner for loop!")

      mean_execution_time_for_same_players = sum(execution_time) / len(execution_time)
      average_running_time_for_same_players.append(mean_execution_time_for_same_players)

    #  print(average_running_time_for_same_players)


    
  #  print("Finished outer for loop!")

    mean_execution_time_for_same_num = sum(average_running_time_for_same_players) / len(average_running_time_for_same_players)
    average_running_time.append(mean_execution_time_for_same_num)

  #  print(average_running_time)

    number_of_opponents += 1
   
  
#  print("Finished while loop!")

  algorithm_to_time_dict[algorithm].extend(average_running_time)



# print("Code executed successfully- HOORAY!!")


save_to_json = json.dumps(algorithm_to_time_dict)
algorithm_dict_to_file = open("trial_run.json", "w")
algorithm_dict_to_file.write(save_to_json)
algorithm_dict_to_file.close()