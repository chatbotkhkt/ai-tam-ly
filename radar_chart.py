import matplotlib.pyplot as plt
import numpy as np

def draw_radar(scores: dict):
    labels = list(scores.keys())
    values = list(scores.values())

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    values += values[:1]
    angles = np.concatenate([angles, [angles[0]]])

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.3)
    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)

    return fig
