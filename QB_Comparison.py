#!/usr/bin/env python
# coding: utf-8

# In[1]:


from config import nfl_key
import pandas as pd
import matplotlib.pyplot as plt
import collections as cc
from collections import defaultdict
from pprint import pprint
import requests
import json
import numpy as np
import time
from nfl import get_qb_data, get_all_qbs, explode_cols, get_pbp_stats

# SUPERBOWL LIV KC vs SF
qb_game_id = '0e00303b-ee60-4cf4-ad68-48efbe53901d'
            
#Mahomes Player_ID
mahomes_id = '11cad59d-90dd-449c-a839-dddaba4fe16c'
#Garoppolo Player_ID
garoppolo_id = '42de9d1d-0352-460b-9172-9452414fd7fd'


qb_season_stats = get_all_qbs()
qb_season_stats.head()


# qb_season_stats = rename_szn_stats_QB(qb_season_stats)

# qb_season_stats


# In[2]:


qb_season_stats = qb_season_stats.loc[qb_season_stats[2] == 'QB']
#qb_season_stats


# In[3]:


qb_season_stats.rename(columns = {0:  'Player ID',
                                    1:  'Name',
                                    2:  'Position',
                                    #passing
                                    3:  'Air Yards',
                                    4:  'Passing Yards',
                                    5:  'Avg Pocket Time',
                                    6:  'Yards Per Pass',
                                    7:  'Batted Passes',
                                    8:  'Completion Percentage',
                                    9:  'Times Blizted',
                                    10: 'Completions',
                                    11: 'Passes Defended',
                                    12: 'Dropped Passes',
                                    13: 'Gross Yards',
                                    14: 'Hurries',
                                    15: 'Interceptions',
                                    16: 'Knockdowns',
                                    17: 'Longest Completion',
                                    18: 'Longest Touchdown Pass',
                                    19: 'Net Yards Passing',
                                    20: 'On Target Throws',
                                    21: 'Total Seconds in Pocket',
                                    22: 'Poor Throws',
                                    23: 'Rating',
                                    24: 'Redzone Passing Attempts',
                                    25: 'Sacked Yards',
                                    26: 'Times Sacked',
                                    27: 'Spikes',
                                    28: 'Throw Aways',
                                    29: 'Passing Touchdowns',
                                    30: 'Yards',
                                    #rushing
                                    31: 'Scrambles',
                                    32: 'Rushing Attempts',
                                    33: 'Yards Per Rush',
                                    34: 'Broken Tackles',
                                    35: 'Kneel Downs',
                                    36: 'Longest Rush',
                                    37: 'Longest TD Run',
                                    38: 'Redzone Rushing Attempts',
                                    39: 'Negative Rushes',
                                    40: 'Yards Lost Rushing',
                                    41: 'Rushing Touchdowns',
                                    42: 'Total Rushing Yards',
                                    43: 'Yards After Contact',
                                    #fumbles
                                    44: 'Fumbles',
                                    45: 'Fumbles Lost'}, inplace=True)
     
qb_season_stats.head()


# ## Top 15 QBs w/ Most Passing Touchdowns

# In[4]:


all_qbs_df = qb_season_stats[['Name',
                              'Rating',
                              'Redzone Passing Attempts',
                              'Passing Touchdowns',
                              'Air Yards',
                              'On Target Throws',
                              'Completion Percentage']]

all_qbs_df = all_qbs_df.sort_values('Passing Touchdowns', ascending= False)
top_qbs_df = all_qbs_df[(all_qbs_df['Passing Touchdowns']>22)]

top_qbs_df


# In[5]:


avg_df = all_qbs_df["Redzone Passing Attempts"].mean()
print(f"Average number of Redzone passing attempts by QB = {avg_df}")


# In[31]:


fig,ax= plt.subplots(figsize=(19,4))

ax.bar(top_qbs_df["Name"],top_qbs_df["Redzone Passing Attempts"], color='steelblue');
ax.set_ylabel("Number of Redzone Passing Attempts")
ax.set_xlabel("Quarterbacks")
ax.set_title('Passing Attempts in the Redzone')
ax.tick_params(axis='x', labelrotation = 45)
ax.axhline(avg_df, color='tab:red', linestyle ="dotted")


# # Superbowl LIV : QB Play-By-Play Statistics

# ## #15 Patrick Mahomes II, Kansas City Chiefs
# 
# Below are the 4th Quarter Play-By-Play statistics for Mahomes

# In[109]:


quarterback_df = get_pbp_stats(qb_game_id, mahomes_id)

qb_df = quarterback_df[['attempt', 'inside_20','touchdown', 'on_target_throw', 'complete', 'firstdown', 'incompletion_type']]
qb_df


# ### Patrick M - Superbowl LIV 4th Qtr Summary

# In[110]:


m_attempt_count = qb_df["attempt"].count()
m_completions = qb_df["complete"].sum()
m_on_target_count = qb_df["on_target_throw"].sum()

m_times_in_redzone = qb_df["inside_20"].sum()
m_redzone_tds = qb_df["touchdown"].sum()





m_redzone_cvn_percentage = "{:.2%}".format(m_redzone_tds / m_times_in_redzone)

m_completion_percentage = "{:.2%}".format(m_completions / m_attempt_count)

m_on_target_percentage = "{:.2%}".format(m_on_target_count / m_attempt_count)


mahomes_summary_df = pd.DataFrame({"Total Passing Attempts": [m_attempt_count],
                            "Completions": m_completions,
                            "Incomplete"      
                            "Completion Percentage": m_completion_percentage,
                            "On Target Percentage": m_on_target_percentage,
                            "Redzone TD Percentage": m_redzone_cvn_percentage})
mahomes_summary_df


# ## #10 Jimmy Garoppolo, San Fransisco 49ers
# 
# Below are the 4th Quarter Play-By-Play statistics for Garoppolo

# In[111]:


quarterback_df = get_pbp_stats(qb_game_id, garoppolo_id)

qb_df = quarterback_df[['attempt', 'inside_20','touchdown', 'on_target_throw', 'complete', 'firstdown', 'incompletion_type']]
qb_df


# ### Jimmy G - Superbowl LIV 4th Qtr Summary

# In[112]:


g_attempt_count = qb_df["attempt"].count()
g_completions = qb_df["complete"].sum()
g_on_target_count = qb_df["on_target_throw"].sum()

g_times_in_redzone = qb_df["inside_20"].sum()
g_redzone_tds = qb_df["touchdown"].count()





g_redzone_cvn_percentage = "{:.2%}".format(g_redzone_tds / g_times_in_redzone)

g_completion_percentage = "{:.2%}".format(g_completions / g_attempt_count)

g_on_target_percentage = "{:.2%}".format(g_on_target_count / g_attempt_count)


garoppolo_summary_df = pd.DataFrame({"Total Passing Attempts": [g_attempt_count],
                            "Completion Percentage": g_completion_percentage,
                            "On Target Percentage": g_on_target_percentage,
                            "Redzone TD Percentage": [g_redzone_tds]})
garoppolo_summary_df


# # Superbowl LIV : QB 4th Quarter Pass Attempt Comparison

# In[113]:


pass_attempts = ["Completed", "Incomplete", "Touchdown"]
m_counts = [m_completions, 14 ,m_redzone_tds]
g_counts = [g_completions, 9 ,g_redzone_tds]
colors = ["steelblue", "tab:red", "skyblue"]
explode = (0.1,0,0)

fig1, (ax1,ax2) = plt.subplots(1,2,figsize=(10,4))
ax1.pie(m_counts, explode=explode, labels=pass_attempts, autopct='%1.1f%%',colors=colors,
        shadow=True, startangle=120)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Patrick Mahomes II, Chiefs', fontsize=15)



ax2.pie(g_counts, explode=explode, labels=pass_attempts, autopct='%1.1f%%',colors=colors,
        shadow=True, startangle=120)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax2.set_title('Jimmy Garoppolo, 49ers', fontsize=15)


plt.tight_layout()
plt.show()

