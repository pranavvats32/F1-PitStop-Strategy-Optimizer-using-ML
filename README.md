# F1-PitStop-Strategy-Optimizer-using-ML
Data Acquired from [FastF1](https://docs.fastf1.dev/) api as well as [Ergast](https://ergast.com/mrd/) API
Attempted Data exploration for Monaco 2023, to search for features which influence pitspot, monaco 2023 data is complex and skewed, the model is not confident (MLP).
(Early rain in the race leading to tyre compound switch  to wets or inters and early pitstops)
(The time difference between the dry compounds is negligible as the track is shorter with many curves and smaller straights )
Moving to a different race data to make specific model for optimised pitstop prediction.
The project in its completion should be able to give optimized pitspot strategy for each track, based on the historial data present.
Feature selection seems of the utmost importance here as alot of features are invovled.
FastF1 is the best dataset for this project, it is also used by the F1 teams aswell.
Ergast only contains the race result data and i am still not sure about its feasibility in this project because racetimes felt that they would 
Will update the readme as i keep working.

References:
https://docs.fastf1.dev/
https://ergast.com/mrd/
https://motorsportengineer.net/how-pit-stop-strategy-leads-to-victories-in-formula-1/
https://motorsportengineer.net/how-race-strategy-works-in-formula-1/#:~:text=The%20decision%20of%20when%20to,on%20opportunities%20or%20mitigate%20risks.
https://www.youtube.com/watch?v=2PUz2EvbHRw
