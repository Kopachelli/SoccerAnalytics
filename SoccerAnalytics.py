from matplotlib import pyplot as plt
from matplotlib.patches import *
import json
import seaborn as sns
import numpy as np


class SoccerAnalytics():
    def __init__(self,game_id):
        with open("events/"+str(game_id)+".json", "r", encoding="utf-8") as fl:
            self.match = json.load(fl)
        with open("lineups/"+str(game_id)+".json","r",encoding="utf-8") as fl:
            self.lineups = json.load(fl)

        self.team_players = dict()
        self.id_number = dict()
        for lineup in self.lineups:
            team_id = lineup["team_id"]
            self.team_players[team_id] = [part["player_id"] for part in lineup["lineup"]]
            self.id_number.update({part["player_id"]:part["jersey_number"] for part in lineup["lineup"]})

        self.player_locations = {k:[] for t in self.team_players.values() for k in t}
        self.id_name = dict()
        self.starting_XI = dict()
        self.id_team = dict()
        self.pass_list = None


        for event in self.match:
            if event['type']['name'] == "Starting XI":
                team = event['team']['name']
                team_id = event['team']['id']
                self.starting_XI[team_id] = event['tactics']['lineup']
                self.id_team[team_id] = team

            if "player" in event and "location" in event:
                id_ = event["player"]["id"]
                name_ = event["player"]["name"]
                if name_ not in self.id_name:
                    self.id_name[id_] = name_
                if id_ not in self.player_locations:
                    self.player_locations[id_] = []

                self.player_locations[id_].append(event["location"]+[event["minute"],event["second"],event["team"]["id"]])

    def _draw_pitch(self,ax,fill=False):
        # focus on only half of the pitch
        # Pitch Outline & Centre Line
        Pitch_out = Rectangle((0, 0), width=120, height=80, color="white", fill=False)
        Pitch = Rectangle((-4, -2), width=128, height=84, color="#2E8B57")

        # Left, Right Penalty Area and midline
        LeftPenalty = Rectangle((0, 18), width=18, height=44, fill=False, color="white")
        RightPenalty = Rectangle((102, 18), width=18, height=44, fill=False, color="white")
        midline = ConnectionPatch([60, 0], [60, 80], "data", "data", color="white")

        # Left, Right 6-yard Box
        LeftSixYard = Rectangle((0, 30), width=6, height=20, fill=False, color="white")
        RightSixYard = Rectangle((114, 30), width=6, height=20, fill=False, color="white")

        # Prepare Circles
        centreCircle = plt.Circle((60, 40), 8.1, color="white", fill=False)
        centreSpot = plt.Circle((60, 40), 0.5, color="white")
        # Penalty spots and Arcs around penalty boxes
        leftPenSpot = plt.Circle((12, 40), 0.5, color="white")
        rightPenSpot = plt.Circle((108, 40), 0.5, color="white")
        leftArc = Arc((12, 40), height=18.4, width=18.4, angle=0, theta1=310, theta2=50, color="white")
        rightArc = Arc((108, 40), height=18.4, width=18.4, angle=0, theta1=130, theta2=230, color="white")

        LeftGoal = Rectangle((-2, 36), width=2, height=8, fill=False, color="white")
        RightGoal = Rectangle((120, 36), width=2, height=8, fill=False, color="white")
        if fill:
            element = [Pitch,Pitch_out, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle,
                   centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc, LeftGoal, RightGoal]
        else:
            element = [Pitch_out, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle,
                       centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc, LeftGoal, RightGoal]
        for i in element:
            ax.add_patch(i)



    def heatmap_players(self,players,start_end=None,title="Heat map"):
        '''
        draw the heatmap for the players
        :param players: id list [int]
        :param start_end: (0.00,90.00)
        :return: no return, just draw the picture
        '''
        fig = plt.figure()
        fig.set_size_inches(7, 5)
        ax = fig.add_subplot(1, 1, 1)
        self._draw_pitch(ax)
        if not start_end:
            x_coord = [0.0, 0.0, 120.0, 120.0]
            y_coord = [0.0, 80.0, 0.0, 80.0]
            for player in players:
                x_coord += [i[0] for i in self.player_locations[player]]
                y_coord += [80 - i[1] for i in self.player_locations[player]]
        else:
            x_coord = [0.0, 0.0, 120.0, 120.0]
            y_coord = [0.0, 80.0, 0.0, 80.0]
            for player in players:
                x_coord += [i[0] for i in self.player_locations[player]
                            if i[2]+i[3]/100 >= start_end[0] and i[2]+i[3]/100 <= start_end[1]]
                y_coord += [80 - i[1] for i in self.player_locations[player]
                            if i[2]+i[3]/100 >= start_end[0] and i[2]+i[3]/100 <= start_end[1]]



        sns.kdeplot(x_coord, y_coord, shade="True", n_levels=15,
                    cmap=sns.diverging_palette(145, 10, n=15, as_cmap=True))
        plt.ylim(-2, 82)
        plt.xlim(-4, 124)
        plt.axis("off")
        plt.title(title)
        plt.show()

    def circle_color(self,postion_xy):
        if postion_xy[0] < 20:
            return "purple"
        elif postion_xy[0] < 40:
            return "blue"
        elif postion_xy[0] < 80:
            return "orange"
        else:
            return "red"

    def display_starting_XI(self,team_id):

        id_position = {
            1: (10,40),
            2: (24,71),
            3: (24,56),
            4: (24,40),
            5: (24,24),
            6: (24,9),
            7: (38,71),
            8: (38,9),
            9: (42,56),
            10:(42,40),
            11:(42,24),
            12:(60,71),
            13:(60,56),
            14:(60,40),
            15:(60,24),
            16:(60,9),
            17:(90,71),
            18:(78,56),
            19:(78,40),
            20:(78,24),
            21:(90,9),
            22:(108,56),
            23:(108,40),
            24:(108,24),
            25:(96,40)
        }


        fig = plt.figure()
        fig.set_size_inches(7, 5)
        ax = fig.add_subplot(1, 1, 1)
        self._draw_pitch(ax,fill=True)

        for player in self.starting_XI[team_id]:
            player_position_id = player['position']['id']

            ax.add_patch(plt.Circle(id_position[player_position_id], 5,
                                    color=self.circle_color(id_position[player_position_id])))
            ax.text(id_position[player_position_id][0] - 1, 80-id_position[player_position_id][1] - 1,
                    str(player['jersey_number']), fontsize=12, color="white")

        plt.ylim(-2, 82)
        plt.xlim(-4, 124)
        plt.axis("off")
        plt.title("Starting XI for Team " + str(self.id_team[team_id]))
        plt.show()

    def _location_partition(self,xy):
        if xy[0] <= 70:
            return 0
        elif xy[0] <= 95:
            if xy[1] <= 40:
                return 1
            else:
                return 2
        else:
            if xy[1] <= 18:
                return 3
            elif xy[1] >= 62:
                return 4
            else:
                return 5

    def _pass_partition(self):
        pass_list = [] # [(start_area,end_area,minute.second,team_id)]
        for event in self.match:
            if event['type']['id'] == 30: # id for pass
                start_location = event["location"]
                end_location = event["pass"]["end_location"]
                pass_list.append((start_location,end_location,event["minute"]+event["second"]/100,event["team"]["id"]))
        self.pass_list = pass_list

    def make_pass_matrix(self,team_id,start_end=(0.00,130.00)):
        pass_matrix = np.zeros((6,6))
        if not self.pass_list:
            self._pass_partition()
        for pas in self.pass_list:
            if pas[2] <= start_end[1] and pas[2] >= start_end[0] and pas[3] == team_id:
                start_area = self._location_partition(pas[0])
                end_area = self._location_partition(pas[1])
                pass_matrix[start_area][end_area] += 1
        return pass_matrix

    def heat_matrix(self,team_id,start_end=(0.00,130.00),if_half=True):

        pass_matrix = self.make_pass_matrix(team_id,start_end)
        if if_half:
            pass_matrix[0][0] = 0
        sns.heatmap(pass_matrix, cmap="Reds")
        plt.title("Area Passing Heat Matrix for Team "+ str(self.id_team[team_id]))
        plt.show()

    def heatmap_team(self,team_id,start_end = (0.00,130.00)):
        fig = plt.figure()
        fig.set_size_inches(7, 5)
        ax = fig.add_subplot(1, 1, 1)
        self._draw_pitch(ax)
        if not start_end:
            x_coord = [0.0, 0.0, 120.0, 120.0]
            y_coord = [0.0, 80.0, 0.0, 80.0]
            for player in self.team_players[team_id]:
                x_coord += [i[0] for i in self.player_locations[player]]
                y_coord += [80 - i[1] for i in self.player_locations[player]]
        else:
            x_coord = [0.0, 0.0, 120.0, 120.0]
            y_coord = [0.0, 80.0, 0.0, 80.0]
            for player in self.team_players[team_id]:
                x_coord += [i[0] for i in self.player_locations[player]
                            if i[2] + i[3] / 100 >= start_end[0] and i[2] + i[3] / 100 <= start_end[1]]
                y_coord += [80 - i[1] for i in self.player_locations[player]
                            if i[2] + i[3] / 100 >= start_end[0] and i[2] + i[3] / 100 <= start_end[1]]

        sns.kdeplot(x_coord, y_coord, shade="True", n_levels=15,
                    cmap=sns.diverging_palette(145, 10, n=15, as_cmap=True))
        plt.ylim(-2, 82)
        plt.xlim(-4, 124)
        plt.axis("off")
        plt.title("Heat Map for Team "+ str(self.id_team[team_id]))
        plt.show()

    def direction_area_plot(self,team_id,interval = 10):
        directions = [] # [left,middle,right]
        start = 0.00
        end = start+interval
        while start < 90:
            directions.append(self.direction_dist(team_id,(start,end)))
            start = end
            end = start+interval
        directions.append(self.direction_dist(team_id,(start,130.0)))

        directions_percent = np.array(list(map(lambda x: np.array(x)/np.sum(x), directions)))
        # Plot
        x = range(len(directions_percent))
        plt.stackplot(x,directions_percent.T, labels=['Right', 'Middle', 'Left'])
        plt.legend(loc='upper left')
        plt.title("Attacking Direction Composition Through Time for Team "+ str(self.id_team[team_id]))
        plt.show()


    def direction_dist(self,team_id,start_end):
        res = [0,0,0]
        if not self.pass_list:
            self._pass_partition()

        for pas in self.pass_list:
            if pas[2] <= start_end[1] and pas[2] >= start_end[0] and pas[3] == team_id:
                end_location= pas[1]
                ind = int(((80-end_location[1])*3-1) // 80)
                res[ind]+=1

        return res

    def direction_pie_plot(self,team_id,start_end=(0.0,130.0)):
        direction = self.direction_dist(team_id,start_end)
        # Pie chart
        labels = ['Right','Middle','Left']
        sizes = np.array(direction)*100
        # add colors
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax1.axis('equal')
        plt.tight_layout()
        plt.title("Attacking Direction Composition for Team "+ str(self.id_team[team_id]))
        plt.show()

    def formation_plot(self,team_id,start_end=(0.0,130.0)):
        fig = plt.figure()
        fig.set_size_inches(7, 5)
        ax = fig.add_subplot(1, 1, 1)
        self._draw_pitch(ax, fill=True)

        for player in self.team_players[team_id]:
            positions = np.array([(i[0],80-i[1]) for i in self.player_locations[player]
                        if i[2] + i[3] / 100 >= start_end[0] and i[2] + i[3] / 100 <= start_end[1]])
            if not len(positions): continue
            average_pos = np.mean(positions,axis=0)

            ax.text(average_pos[0], average_pos[1],
                    str(self.id_number[player]), fontsize=14, color="white")


        plt.ylim(-2, 82)
        plt.xlim(-4, 124)
        plt.axis("off")
        plt.title("Average position for team "+ str(self.id_team[team_id]))
        plt.show()

    def _draw_partition(self,ax):
        Back = Rectangle((3,3), width=64, height=74, color="#1E90FF",alpha=0.8)
        Left_Mid = 	Rectangle((73,43), width=19, height=34, color="#1E90FF",alpha=0.8)
        Right_Mid = Rectangle((73,3), width=19, height=34, color="#1E90FF", alpha=0.8)
        Left_Bottom = Rectangle((98,65),width=19,height=12,color="#1E90FF", alpha=0.8)
        Right_Bottom = Rectangle((98,3),width=19,height=12,color="#1E90FF", alpha=0.8)
        Shooting_Area = Rectangle((98,21),width=19,height=38,color="#1E90FF", alpha=0.8)
        elements = [Back,Left_Mid,Right_Mid,Left_Bottom,Right_Bottom,Shooting_Area]
        for i in elements:
            ax.add_patch(i)
        ax.text(35,40, "0", fontsize=14, color="white")
        ax.text(82.5, 60, "1", fontsize=14, color="white")
        ax.text(82.5, 20, "2", fontsize=14, color="white")
        ax.text(107.5,71,"3",fontsize=14, color="white")
        ax.text(107.5,9,"4",fontsize=14, color="white")
        ax.text(107.5, 40, "5", fontsize=14, color="white")


    def pass_map_display(self,team_id,start_end=(0.00,130.00),if_half=True):

        fig = plt.figure()
        fig.set_size_inches(7, 5)
        ax = fig.add_subplot(1, 1, 1)
        self._draw_pitch(ax, fill=True)
        self._draw_partition(ax)

        area_center={0:(35,40),1:(82.5, 60),
                     2:(82.5, 20),3:(107.5,71),
                     4:(107.5,9),5:(107.5, 40)}

        pass_matrix = self.make_pass_matrix(team_id,start_end)
        if if_half:
            pass_matrix[0][0] = 0

        sort_matrix = np.argsort(-np.reshape(pass_matrix,(1,36))[0])[:5]
        for ind in sort_matrix:
            start = int(ind // 6)
            end = int(ind % 6)
            if start == end:
                ax.add_patch(plt.Circle(area_center[start], 5,
                                        color="red",fill=False))
            else:
                ax.arrow(area_center[start][0],area_center[start][1],
                         area_center[end][0]-area_center[start][0],
                         area_center[end][1]-area_center[start][1], color = "red",head_width=1, head_length=2)



        plt.ylim(-2, 82)
        plt.xlim(-4, 124)
        plt.axis("off")
        plt.title("Attacking Pass Direction for Team "+str(self.id_team[team_id]))
        plt.show()

    def describe(self):
        for team in self.lineups:
            print("Country:")
            print("%d %s" % (team["team_id"],team["team_name"]))
            print()
            for player in team["lineup"]:
                print_name = player["player_nickname"]
                if not print_name:
                    print_name = player["player_name"]
                print("ID: %d, Name: %s, Number: %d, Country: %s " %
                      (player["player_id"],print_name,player["jersey_number"],player["country"]["name"]))
            print("\n\n")





if __name__ == "__main__":
    sa = SoccerAnalytics(7582)
    # sa.describe()
    # sa.heatmap_players([5177], (45.00,90.00),title="Heat map for Russia 5 (Left Forward)")
    sa.display_starting_XI(796)
    sa.heatmap_team(772,(80,90))
    sa.formation_plot(772,(80,90))
    sa.direction_pie_plot(772,(80,90))
    sa.heat_matrix(772,(80,90))
    # sa.heat_matrix(796)
    # sa.heatmap_team(772)
    # sa.direction_pie_plot(796)
    sa.direction_area_plot(796)
    # sa.formation_plot(772,(0,10))
    sa.pass_map_display(772,(80,90))
    # sa.heatmap_team(772, start_end=(0, 10))
    # sa.heatmap_team(772, start_end=(10, 20))
    # sa.heatmap_team(772, start_end=(20, 30))
    # sa.heatmap_team(772, start_end=(30, 40))
    # sa.heatmap_team(772, start_end=(40, 50))
    # sa.heatmap_team(772, start_end=(50, 60))
    # sa.heatmap_team(772, start_end=(60, 70))
    # sa.heatmap_team(772, start_end=(70, 80))
    # sa.heatmap_team(772, start_end=(80, 90))














