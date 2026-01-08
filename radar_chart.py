import matplotlib.pyplot as plt
import numpy as np

def plot_aq_radar(scores: dict):
    labels = list(scores.keys())
    values = list(scores.values())

    # Đóng vòng tròn
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 25)

    ax.set_title("Biểu đồ AQ – 4 nhóm chính", fontsize=14, pad=20)

    return fig
