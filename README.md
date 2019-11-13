# SoccerAnalytics
Data Visualization Toolkit for Soccer Analytics

## Introduction
The class SoccerAnalytics try to parse a json file containing a soccer match's information. 
Our sample data record the events in the FIFA 2018 World Cup 1/8 final Spain vs Russia. 
The data are provided by StatsBomb. They have tons of detailed match data of La Liga and international cup competitions.
The sample game mentioned above has the id "7582" in the data source. You can refer to <https://github.com/statsbomb/open-data> for detailed information. Here we include their logo below.

![StatsBomb Logo](/img/stats-bomb-logo.png)

Generally, we implement the heat map which describes the movement of certain 
players. Additionally, position information and pass between different area can also be visualized using our project.

## Function Usage

First you should import the module and initialize the class "SoccerAnalytics".
Game_id should be delivered to the class.

```{python}
sa = SoccerAnalytics(7582)
```

### Description

print the team_ids and player_ids for reference.

```{python}
sa.describe()
```

```{}
Country:
772 Spain

ID: 3064, Name: David Silva, Number: 21, Country: Spain 
ID: 3333, Name: David de Gea, Number: 1, Country: Spain 
ID: 5210, Name: Isco, Number: 22, Country: Spain 
ID: 5198, Name: Diego Costa, Number: 19, Country: Spain 
ID: 5199, Name: Koke, Number: 8, Country: Spain 
ID: 5201, Name: Sergio Ramos, Number: 15, Country: Spain 
ID: 5202, Name: Nacho, Number: 4, Country: Spain 
ID: 5203, Name: Sergio Busquets, Number: 5, Country: Spain 
ID: 5211, Name: Jordi Alba, Number: 18, Country: Spain 
ID: 5213, Name: Gerard Piqué, Number: 3, Country: Spain 
ID: 5216, Name: Andrés Iniesta, Number: 6, Country: Spain 
ID: 5217, Name: Iago Aspas, Number: 17, Country: Spain 
ID: 5718, Name: Rodrigo, Number: 9, Country: Spain 
ID: 5719, Name: Marco Asensio, Number: 20, Country: Spain 
ID: 5721, Name: Daniel Carvajal, Number: 2, Country: Spain 



Country:
796 Russia

ID: 5170, Name: Mário Fernandes, Number: 2, Country: Russia 
ID: 5171, Name: Roman Zobnin, Number: 11, Country: Russia 
ID: 5172, Name: Igor Akinfeev, Number: 1, Country: Russia 
ID: 5174, Name: Sergei Ignashevich, Number: 4, Country: Russia 
ID: 5175, Name: Ilya Kutepov, Number: 3, Country: Russia 
ID: 5177, Name: Aleksandr Golovin, Number: 17, Country: Russia 
ID: 5179, Name: Daler Kuzyaev, Number: 7, Country: Russia 
ID: 5182, Name: Aleksandr Samedov, Number: 19, Country: Russia 
ID: 5186, Name: Denis Cheryshev, Number: 6, Country: Russia 
ID: 5193, Name: Yuri Zhirkov, Number: 18, Country: Russia 
ID: 5194, Name: Fyodor Smolov, Number: 10, Country: Russia 
ID: 5195, Name: Artem Dzyuba, Number: 22, Country: Russia 
ID: 5677, Name: Fedor Kudryashov, Number: 13, Country: Russia 
ID: 6353, Name: Vladimir Granat, Number: 14, Country: Russia 
ID: 6354, Name: Aleksandr Erokhin, Number: 21, Country: Russia 
```

### Heat Map (players)

Deliver a list of player_ids to plot the heat map of those players.
You can also use "start_end" to control the time_period. For example, (12.30,25.12) means from 12'30'' to 25'12''. The default value of start_end is (0.0,130.0), which is the same in other functions.
Parameter "title" can also define the name of the picture.

```{python}
sa.heatmap_players([5177], (45.00,90.00),title="Heat map for Russia 5 (Left Forward)")
```

![heatmap golovin](/img/heatmap_player_sample.png)

### Heat Map (team)

Parameters: team_id, start_end.

```{python}
sa.heatmap_team(772,(80,90))
```

![heatmap spain](/img/heatmap_team_sample.png)

### Display Starting XI

Parameters: team_id.

```{python}
sa.display_starting_XI(796)
```

![starting_XI_sample](/img/starting11_russia.png)

### Average Position Plot

Plot the average position for every players in a time period.

Parameters: team_id, start_end

```{python}
sa.formation_plot(772,(80,90))
```

![formation_sample](/img/formation_sample.png)

### Attacking Direction Pie Chart and Area Chart

Pie chart reflects the directions percentage (right, middle and left) a team chooses to pass the ball.

Parameters: team_id, start_end

 ```{python}
sa.direction_pie_plot(772,(80,90))
```

![pie_chart_sample](/img/pie_chart_sample.png)

Area Chart reflects the attacking direction through time.


Parameters: team_id, start_end

 ```{python}
sa.direction_area_plot(796)
```

![area_sample](/img/area_sample.png)

### Pass Map

We split the soccer field into 6 partitions.

![area_split](/img/area_partition.png).

And the heat matrix reflects the frequency of passing between different partitions. The largest 5 values will be displayed on the map.
A circle means that players tend to pass in the same partition, while an arrow means that they tend to pass from one to another.

Parameters: team_id, start_end

```{python}
sa.heat_matrix(772,(80,90))
sa.pass_map_display(772,(80,90))
```

![heat_matrix_sample](/img/heat_matrix_sample.png)
![passmap_sample](/img/passmap_sample.png)

