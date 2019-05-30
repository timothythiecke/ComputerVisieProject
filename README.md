The script `main.py` expects one argument: the absolute or relative path to a video file. It will open five windows, as shown in the figure below:
![Application Example](https://i.imgur.com/KYURErO.jpg)
The rightmost frame is the video frame, which contains the live video as it is playing. The leftmost column holds two extraction windows. These show what the segmentation algorithm extracted from the video. There is no particular order in which window is used first, the only rule is that it is alternated. Because we use multithreading, using a single window is not plausible as multiple threads will write to the same window, which openCV cannot handle. Using two windows instead solves this issue.
The middle column follows the same principle, but holds the matches which the system found for the paintings that are extracted. These frames will only contain images from the database.

The most important code can be found in `Contour.py` and `Matching.py` which contain the code to respectively segment a painting and match the painting against the database.
