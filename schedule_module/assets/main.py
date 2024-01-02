import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random

class OS:
    def __init__(self,data):
        self.data = data
    def FCFS(self):
        data = self.data
        data = data.sort_values(by=['AT'])
        data.reset_index(inplace=True, drop=True)
        print(data)
        Process = []
        Start = []
        End = []
        At = []
        for index, row in data.iterrows():
            process = row['Process']
            at = row['AT']
            cbt = row['CBT']
            # for first process
            if index == 0:
                End.append(at+cbt)
                Start.append(at)
            # for other process
            else :
                Start.append(End[-1])
                End.append(End[-1] + cbt)
            Process.append(process)
            At.append(at)

        # make table
        self.print_table()

        print(Process)

        # make plot
        self.make_plot(Process,Start,End,At, 'FCFS Figure')

    def SPN(self):
        data = self.data
        Process = []
        Start = []
        End = []
        At = {}
        waiting = []

        # add at to process
        for index, row in data.iterrows():
            at = {row['Process']:row['AT']}
            At.update(at)

        # find process with lowest AT in first step
        min_rows = data[data['AT'] == data['AT'].min()]
        for i,process in min_rows.iterrows():
            # add all process in min_rows to waiting queue
            waiting.append(process)
        # romove all process in min_rows from dataset
        data:pd.DataFrame = data.drop(min_rows.index)

        # sort waiting queue by max CBT
        waiting.sort(key=lambda x : x['CBT'], reverse=True)

        # pop Process
        find_process = waiting.pop()
        # add find process to lists
        Process.append(find_process['Process'])
        Start.append(find_process['AT'])
        End.append(find_process['AT'] + find_process['CBT'])

        # Find the last process end time and add all processes with arrival times lower than this time.
        flag = True
        while flag:
            last_process_time = End[-1]
            if not data.empty :
                filtered_rows = data[data['AT'] < last_process_time]
                if not filtered_rows.empty :
                    # if find process with arrival times lower than last process endtime
                    while not filtered_rows.empty :
                        # Find the process with the biggest CBT in the filtered rows
                        max_cbt_process = filtered_rows.loc[[filtered_rows['CBT'].idxmax()]]
                        waiting.append(max_cbt_process)
                        # # remove this process from filtered rows
                        filtered_rows:pd.DataFrame = filtered_rows.drop(max_cbt_process.index)
                        # # remove this process from data
                        data:pd.DataFrame = data.drop(max_cbt_process.index)

                    # sort waiting queue by max CBT
                    waiting.sort(key=lambda x : x['CBT'].values[0], reverse=True)

                    # add last item to lists from waiting queue (with lowest CBT in waiting queue)
                    pop_waiting = waiting.pop()
                    last_process_end = End[-1]

                    Process.append(pop_waiting['Process'].values[0])
                    Start.append(last_process_end)
                    End.append(last_process_end + pop_waiting['CBT'].values[0])
                else :
                    # if can not found process with arrival times lower than last process endtime
                    if len(waiting) == 0 :
                        # we dont have any process in waiting queue
                        # find process with lowest AT in first step
                        min_rows = data[data['AT'] == data['AT'].min()]
                        for i,process in min_rows.iterrows():
                            # add all process in min_rows to waiting queue
                            waiting.append(process)
                        # romove all process in min_rows from dataset
                        data:pd.DataFrame = data.drop(min_rows.index)


                    # sort waiting queue by max CBT
                    waiting.sort(key=lambda x : x['CBT'])
                    find_process = waiting.pop()

                    # add find process to lists
                    Process.append(find_process['Process'])
                    Start.append(last_process_time)
                    End.append(last_process_time + find_process['CBT']) 
    
            else:
                flag = False
                # We don't have any processes in data, so pop all of the remaining processes to lists.
                for i in range(len(waiting)):
                    last_process_end = End[-1]
                    pop_waiting = waiting.pop()
                    Process.append(pop_waiting['Process'].values[0])
                    Start.append(last_process_end)
                    End.append(last_process_end + pop_waiting['CBT'].values[0])

        # sort AT base on Process List
        sorted_dict = dict(sorted(At.items(), key=lambda x: Process.index(x[0])))
        At_2 = [i for i in sorted_dict.values()]

        # make table
        self.print_table()

        print(Process)

        # make plot
        self.make_plot(Process,Start,End,At_2, 'SPN Figure')

    
    def HRRN(self):
        data:pd.DataFrame = self.data
        Process = []
        Start = []
        End = []
        At = {}
        Waiting = []

        # add at to process
        for index, row in data.iterrows():
            at = {row['Process']:row['AT']}
            At.update(at)

        # find process with lowest AT in first step
        min_rows = data[data['AT'] == data['AT'].min()]
        for i,process in min_rows.iterrows():
            # add all process in min_rows to waiting queue
            Waiting.append(process)
        # romove all process in min_rows from dataset
        data:pd.DataFrame = data.drop(min_rows.index)

        # check RR for all Process in Waiting
        check_rr = [self.calc_RR(x['AT'],x['CBT'],x['AT']+x['CBT']) for x in Waiting]
        if (all(num == check_rr[0] for num in check_rr)) :
            # sort waiting queue by max CBT
            Waiting.sort(key=lambda x : x['CBT'], reverse=True)
        else :
            # sort process by Highest Response ratio (small to large) 
            Waiting.sort(key=lambda x : self.calc_RR(x['AT'],x['CBT'],x['AT']+x['CBT']))
        # pop Process
        find_process = Waiting.pop()
        # add find process to lists
        Process.append(find_process['Process'])
        Start.append(find_process['AT'])
        End.append(find_process['AT'] + find_process['CBT']) 
        flag = True
        while flag:
            if not data.empty :
                last_process_time = End[-1]
                # do while data is not empty
                # find process with arrival times lower than last process endtime
                filtered_rows = data[data['AT'] < last_process_time]
                if not filtered_rows.empty :
                    for index, process in filtered_rows.iterrows() :
                        # add process in filtered_rows to Waiting queue
                        Waiting.append(process)
                    # remove this process from data
                    data:pd.DataFrame = data.drop(filtered_rows.index)
                else :
                    # if we can not found process with arrival times lower than last process endtime, and length waiting is 0
                    if len(Waiting) == 0 :
                        # query to find first process with lowest at
                        # find process with lowest AT in first step
                        min_rows = data[data['AT'] == data['AT'].min()]
                        for i,process in min_rows.iterrows():
                            # add all process in min_rows to waiting queue
                            Waiting.append(process)
                        # romove all process in min_rows from dataset
                        data:pd.DataFrame = data.drop(min_rows.index)
                        # find process with Highest Response ratio

                # check RR for all Process in Waiting
                check_rr = [self.calc_RR(x['AT'],x['CBT'],last_process_time) for x in Waiting]
                if (all(num == check_rr[0] for num in check_rr)) :
                    # sort waiting queue by max CBT
                    Waiting.sort(key=lambda x : x['CBT'], reverse=True)
                else :
                    # sort process by Highest Response ratio (small to large)
                    Waiting.sort(key=lambda x : self.calc_RR(x['AT'],x['CBT'],last_process_time))
                # pop Process
                find_process = Waiting.pop()
                
                # add find process to lists
                Process.append(find_process['Process'])
                Start.append(last_process_time)
                End.append(last_process_time + find_process['CBT']) 
            else :
                # if data is empty add all process in waiting queue to lists base on Highest Response ratio
                flag = False
                # find & add process with Highest Response ratio if len(waiting) is not 0
                if len(Waiting) != 0 :
                    while len(Waiting) != 0 :
                        last_process_time = End[-1]
                        # check RR for all Process in Waiting
                        check_rr = [self.calc_RR(x['AT'],x['CBT'],last_process_time) for x in Waiting]
                        if (all(num == check_rr[0] for num in check_rr)) :
                            # sort waiting queue by max CBT
                            Waiting.sort(key=lambda x : x['CBT'], reverse=True)
                        else :
                            # sort process by Highest Response ratio (small to large)
                            Waiting.sort(key=lambda x : self.calc_RR(x['AT'],x['CBT'],last_process_time))
                        # pop Process
                        find_process = Waiting.pop()
                        # add find process to lists
                        Process.append(find_process['Process'])
                        Start.append(last_process_time)
                        End.append(last_process_time + find_process['CBT']) 

        # sort AT base on Process List
        sorted_dict = dict(sorted(At.items(), key=lambda x: Process.index(x[0])))
        At_2 = [i for i in sorted_dict.values()]

        # make table
        self.print_table()

        print(Process)

        # make plot
        self.make_plot(Process,Start,End,At_2, 'HRRN Figure')

         
    def calc_RR(self,at,cbt,last_process_endtime):
        return ((last_process_endtime-at)+cbt)/cbt



    def Round_Robin(self, Quantum):
        data:pd.DataFrame = self.data
        Process = []
        Start = []
        End = []
        At = {}
        Waiting = []

        # add at to process
        for index, row in data.iterrows():
            at = {row['Process']:row['AT']}
            At.update(at)

        # find process with lowest AT in first step
        min_rows = data[data['AT'] == data['AT'].min()]
        for i,process in min_rows.iterrows():
            # add all process in min_rows to waiting queue
            Waiting.append(process)
        # romove all process in min_rows from dataset
        data:pd.DataFrame = data.drop(min_rows.index)

        # first calculation
        for process in Waiting:
            if process.CBT <= Quantum :
                Process.append(process.Process)
                Start.append(process.AT)
                End.append(process.AT + process.CBT)
                # remove this process from Waiting queue
                Waiting.remove(process)
            else :
                # decrease CBT for Quantum Time
                process.CBT = process.CBT - Quantum
                Process.append(process.Process)
                Start.append(process.AT)
                End.append(process.AT + Quantum)

        flag = True
        while flag:
            if not data.empty :
                last_process_time = End[-1]
                # do while data is not empty
                # find process with arrival times lower than last process endtime
                filtered_rows = data[data['AT'] < last_process_time]
                if not filtered_rows.empty :
                    for index, process in filtered_rows.iterrows() :
                        # if we find process, we should apply Qumtum time and then add to waiting list
                        # print('ok')
                        last_process_time = End[-1]
                        if process.CBT <= Quantum :
                            # whole of process will add
                            Process.append(process.Process)
                            Start.append(last_process_time)
                            End.append(last_process_time + process.CBT)
                        else :
                            # decrease CBT for Quantum Time
                            process.CBT = process.CBT - Quantum
                            Process.append(process.Process)
                            Start.append(last_process_time)
                            End.append(last_process_time + Quantum)
                            # The rest of the process will be queued
                            Waiting.append(process)
                    # remove this process from data
                    data:pd.DataFrame = data.drop(filtered_rows.index)
                else :
                    # if we can not found process with arrival times lower than last process endtime, and length waiting is 0
                    if len(Waiting) == 0 :
                        # query to find first process with lowest at
                        # find process with lowest AT in first step
                        min_rows = data[data['AT'] == data['AT'].min()]
                        for i,process in min_rows.iterrows():
                            # if we find process, we should apply Qumtum time and then add to waiting list
                            last_process_time = End[-1]
                            if process.CBT <= Quantum :
                                # whole of process will add
                                Process.append(process.Process)
                                Start.append(last_process_time)
                                End.append(last_process_time + process.CBT)
                            else :
                                # decrease CBT for Quantum Time
                                process.CBT = process.CBT - Quantum
                                Process.append(process.Process)
                                Start.append(last_process_time)
                                End.append(last_process_time + Quantum)
                                # The rest of the process will be queued
                                Waiting.append(process)
                        # romove all process in min_rows from dataset
                        data:pd.DataFrame = data.drop(min_rows.index)
                    else :
                        # we dont find any process lower than last process AT and also length waiting is not 0
                        Waiting, Process, Start, End = self.clacProcess_RoundRobin(Waiting, Process, Start, End, Quantum)
            else :
                # if data is empty add all process in waiting queue to lists base on Round Robin
                flag = False
                if len(Waiting) != 0 :
                    while len(Waiting) != 0 :
                        # we are using this way to remove process from waiting queue
                        fake_queue = []
                        for process in Waiting:
                            last_process_time = End[-1]
                            if process.CBT <= Quantum :
                                Process.append(process.Process)
                                Start.append(last_process_time)
                                End.append(last_process_time + process.CBT)
                                # remove this process from Waiting queue
                            else :
                                fake_queue.append(process)
                                # decrease CBT for Quantum Time
                                process['CBT'] = process['CBT'] - Quantum
                                Process.append(process.Process)
                                Start.append(last_process_time)
                                End.append(last_process_time + Quantum)
                        Waiting = fake_queue

        # sort AT base on Process List
        # sorted_dict = dict(sorted(At.items(), key=lambda x: Process.index(x[0])))
        # At_2 = [i for i in sorted_dict.values()]
        At_2 = []
        for p in Process:
            At_2.append(At[p])

        # make table
        self.print_table()

        print(Process)

        # make plot
        self.make_plot(Process,Start,End,At_2,'Round Robin Figure')



    def clacProcess_RoundRobin(self, Waiting, Process, Start, End, Quantum):
        if len(Process) == 0 :
            for process in Waiting:
                if process.CBT <= Quantum :
                    Process.append(process.Process)
                    Start.append(process.AT)
                    End.append(process.AT + process.CBT)
                    # remove this process from Waiting queue
                    Waiting.remove(process)
                else :
                    # decrease CBT for Quantum Time
                    process.CBT = process.CBT - Quantum
                    Process.append(process.Process)
                    Start.append(process.AT)
                    End.append(process.AT + Quantum)
        else :
            for process in Waiting:
                last_process_time = End[-1]
                if process.CBT <= Quantum :
                    Process.append(process.Process)
                    Start.append(last_process_time)
                    End.append(last_process_time + process.CBT)
                    # remove this process from Waiting queue
                    Waiting.remove(process)
                else :
                    # decrease CBT for Quantum Time
                    process.CBT = process.CBT - Quantum
                    Process.append(process.Process)
                    Start.append(last_process_time)
                    End.append(last_process_time + Quantum)

        return Waiting, Process, Start, End

    def print_table(self):
        print(tabulate(
            self.data,
            headers="keys",
            showindex=False,
            tablefmt="rounded_grid",
            colalign=('center','center','center',)
            ))
        
    def make_plot(self,Process,Start,End,At,plotTitle):
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 5))
        wt_dict = {}
        wt_li= []
        tt_dict = {}
        tt_li= []
        colors = ['red','blue','green','yellow','gray','pink','orange']
        AVG_watingTime = 0
        AVG_totalTime = 0


        # Plot each linear graph
        for i in range(len(Process)):
            process_name = Process[i]
            start_point = Start[i]
            end_point = End[i]
            at_point = At[i]
    
            # Plot the linear graph for each process
            ax.plot([start_point, end_point], [i, i], label=process_name, linewidth=3.5)
            
            # Mark the start point with a marker (circle in this case)
            ax.scatter(at_point, i, color='red', marker='X', label=f'Start ({process_name})')
            
            # # # Draw a dotted line from the start point to the x-axis
            ax.vlines(start_point, ymin=0, ymax=i, colors='grey', linestyles='dotted')
            ax.vlines(end_point, ymin=0, ymax=i, colors='grey', linestyles='dotted')

            # make waiting time legend
            #TODO : Fix Calculation for HRRN
            wt_dict[i] = mpatches.Patch(color=random.choice(colors), label=f' {process_name} = {start_point} - {at_point} = {start_point-at_point}')
            wt_li.append(wt_dict[i])
            AVG_watingTime += start_point-at_point

            # make total time legend
            #TODO : Fix Calculation for HRRN
            tt_dict[i] = mpatches.Patch(color=random.choice(colors), label=f' {process_name} = {end_point} - {at_point} = {end_point-at_point}')
            tt_li.append(tt_dict[i])
            AVG_totalTime += end_point-at_point
            
        # setting x-axis scale
        plt.xticks(range(0, End[-1]+10))

        # title of plot
        plt.title(plotTitle)

        # Set labels and legend
        ax.set_title(plotTitle)
        ax.set_xlabel(f'Time | Avg Waiting Time = {round(AVG_watingTime/len(Process),2)} | Avg Total Time = {round(AVG_totalTime/len(Process),2)}')
        ax.set_ylabel('Process')
        ax.set_yticks(range(len(Process)))
        ax.set_yticklabels(Process)
        ax.legend(loc=1) 
        ax2 = ax.twinx()
        ax3 = ax.twinx()
        ax2.legend(handles = wt_li, loc=4, title="Waiting Time Per Process")
        ax3.legend(handles = tt_li, loc=2, title="Total Time Per Process")
 
        # Show the plot
        plt.show()

# os = OS(
#     pd.DataFrame(
#         {"Process" : ['P0', 'P1','P2','P3','P4'],
#          "AT" : [0,2,4,6,8],
#          "CBT" : [4,5,3,6,3]
#         }
#     )
# )

# os = OS(
#     pd.DataFrame(
#         {"Process" : ['P1', 'P2','P3','P4','P5','P6'],
#          "AT" : [0,1,2,3,4,4],
#          "CBT" : [7,4,15,11,20,9]
#         }
#     )
# )


# os.FCFS()

# os.SPN()

# os.HRRN()
        
# os.Round_Robin(5)