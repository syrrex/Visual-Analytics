import pandas as pd
import numpy as np
import os
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Credits: 007Chakraphat - Kaggle
def create_football_field(linenumbers=True,
                          endzones=True,
                          highlight_line=False,
                          highlight_line_number=50,
                          highlighted_name='Line of Scrimmage',
                          fifty_is_los=False,
                          figsize=(12, 6.33)):
    """
    Function that plots the football field for viewing plays.
    Allows for showing or hiding endzones.
    """
    rect = patches.Rectangle((0, 0), 120, 53.3, linewidth=0.1,
                             edgecolor='r', facecolor='darkgreen', zorder=0)

    fig, ax = plt.subplots(1, figsize=figsize)
    ax.add_patch(rect)

    plt.plot([10, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80,
              80, 90, 90, 100, 100, 110, 110, 120, 0, 0, 120, 120],
             [0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3,
              53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 53.3, 0, 0, 53.3],
             color='white')
    if fifty_is_los:
        plt.plot([60, 60], [0, 53.3], color='gold')
        plt.text(62, 50, '<- Player Yardline at Snap', color='gold')
    # Endzones
    if endzones:
        ez1 = patches.Rectangle((0, 0), 10, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ez2 = patches.Rectangle((110, 0), 120, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ax.add_patch(ez1)
        ax.add_patch(ez2)
    plt.xlim(0, 120)
    plt.ylim(-5, 58.3)
    plt.axis('off')
    if linenumbers:
        for x in range(20, 110, 10):
            numb = x
            if x > 50:
                numb = 120 - x
            plt.text(x, 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,  # fontname='Arial',
                     color='white')
            plt.text(x - 0.95, 53.3 - 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,  # fontname='Arial',
                     color='white', rotation=180)
    if endzones:
        hash_range = range(11, 110)
    else:
        hash_range = range(1, 120)

    for x in hash_range:
        ax.plot([x, x], [0.4, 0.7], color='white')
        ax.plot([x, x], [53.0, 52.5], color='white')
        ax.plot([x, x], [22.91, 23.57], color='white')
        ax.plot([x, x], [29.73, 30.39], color='white')

    if highlight_line:
        hl = highlight_line_number + 10
        plt.plot([hl, hl], [0, 53.3], color='yellow')
        plt.text(hl + 2, 50, '<- {}'.format(highlighted_name),
                 color='yellow')
    return fig, ax


def try_printing_players():

    # Example usage
    train = pd.read_csv('train.csv/train.csv', low_memory=False)
    fig, ax = create_football_field()
    train.query("PlayId == 20170907000118 and Team == 'away'") \
        .plot(x='X', y='Y', kind='scatter', ax=ax, color='orange', s=30, legend='Away')
    train.query("PlayId == 20170907000118 and Team == 'home'") \
        .plot(x='X', y='Y', kind='scatter', ax=ax, color='blue', s=30, legend='Home')
    plt.title('Play # 20170907000118')
    plt.legend()
    plt.show()


    # LOS
    playid = 20181230154157
    train.query("PlayId == @playid").head()

    yl = train.query("PlayId == @playid")['YardLine'].tolist()[0]
    fig, ax = create_football_field(highlight_line=True,
                                    highlight_line_number=yl + 54)
    train.query("PlayId == @playid and Team == 'away'") \
        .plot(x='X', y='Y', kind='scatter', ax=ax, color='orange', s=30, legend='Away')
    train.query("PlayId == @playid and Team == 'home'") \
        .plot(x='X', y='Y', kind='scatter', ax=ax, color='blue', s=30, legend='Home')
    plt.title(f'Play # {playid}')
    plt.legend()
    plt.show()


    # Another example:
    train2021 = pd.read_csv('data/week11.csv')

    example_play_home = train2021.query('gameId == 2018111900 and playId == 5577 and team == "home"')
    example_play_away = train2021.query('gameId == 2018111900 and playId == 5577 and team == "away"')

    fig, ax = create_football_field()
    example_play_home.query('event == "ball_snap"').plot(x='x', y='y', kind='scatter', ax=ax, color='orange', s=30,
                                                         legend='Away')
    example_play_away.query('event == "ball_snap"').plot(x='x', y='y', kind='scatter', ax=ax, color='blue', s=30,
                                                         legend='Home')
    plt.title('Game #2018111900 Play #5577 at Ball Snap')
    plt.legend()
    plt.show()

    fig, ax = create_football_field()
    example_play_home.plot(x='x', y='y', kind='scatter', ax=ax, color='orange', s=30, legend='Away')
    example_play_away.plot(x='x', y='y', kind='scatter', ax=ax, color='blue', s=30, legend='Home')
    plt.title('Game #2018111900 Play #5577 at Ball Snap')
    plt.legend()
    plt.show()


try_printing_players()


class GameField:
    def __init__(self):
        self.whatever = 0
