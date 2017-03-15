import numpy as np


DATA_PATH = [
    "/home/rafael/codes/bcitp/data/session/mario_1/data_cal.npy",
    "/home/rafael/codes/bcitp/data/session/mario_4/data_cal.npy",
    # "/home/rafael/codes/bcitp/data/session/mario_4/data_cal.npy",
    # "/home/rafael/codes/bcitp/data/session/mario_5/data_cal.npy",
]


EVENTS_PATH = [
    "/home/rafael/codes/bcitp/data/session/mario_1/events_cal.npy",
    "/home/rafael/codes/bcitp/data/session/mario_4/events_cal.npy",
    # "/home/rafael/codes/bcitp/data/session/mario_4/events_cal.npy",
    # "/home/rafael/codes/bcitp/data/session/mario_5/events_cal.npy",
]

new_data = np.load(DATA_PATH[0])
new_events = np.load(EVENTS_PATH[0])

for data_path, events_path in zip(DATA_PATH[1:], EVENTS_PATH[1:]):

    ev_offset = new_data.shape[0]  # compute the offset of the new data

    # Stack data
    data = np.load(data_path)
    new_data = np.vstack([new_data, data])

    # Stack data
    events = np.load(events_path)
    events[:, 0] += ev_offset  # sum the offset to event timestamps
    new_events = np.vstack([new_events, events])

np.save('data_cal.npy', new_data)
np.save('events_cal.npy', new_events)
