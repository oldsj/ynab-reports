from xmlrpc.client import ProtocolError
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mail import *

fig = plt.figure()
# Data
df = pd.DataFrame(
    {
        "x_values": range(1, 11),
        "y1_values": np.random.randn(10),
        "y2_values": np.random.randn(10) + range(1, 11),
        "y3_values": np.random.randn(10) + range(11, 21),
    }
)

# multiple line plots
plt.plot(
    "x_values",
    "y1_values",
    data=df,
    marker="o",
    markerfacecolor="blue",
    markersize=12,
    color="skyblue",
    linewidth=4,
)
plt.plot("x_values", "y2_values", data=df, marker="", color="olive", linewidth=2)
plt.plot(
    "x_values",
    "y3_values",
    data=df,
    marker="",
    color="olive",
    linewidth=2,
    linestyle="dashed",
    label="toto",
)

# show legend
plt.legend()
# plt.show()


send_report(fig)

