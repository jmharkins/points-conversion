import pandas as pd
import numpy as np
from ggplot import *
# load data
data = pd.read_csv('conversion_cleaned.csv')

# plot conversion this year against previous
ggplot(aes(x='crate', y='crate_next'), data=data) + geom_point() + geom_smooth(method = 'lm')

# define tmchg variable
data['tmchange'] = [(0 if x ==y else 1) for x,y in zip(data['team'],data['team_change'])]

#ggplot graphs


#broken out by tmchange
ggplot(aes(x='crate', y='crate_next', color = 'tmchange'), data=data) + geom_point() + xlab("2012 Conversion Rate") + ylab("2013 Conversion Rate")
# neat Team Change Label
data['Team Change'] = [("Changed Teams" if x ==1 else "Did Not Change Teams") for x in data['tmchange']]
ggplot(aes(x='crate', y='crate_next', color = 'Team Change'), data=data) + geom_point() + xlab("2012 Conversion Rate") + ylab("2013 Conversion Rate")


# scatter with fit and xy line
ggplot(aes(x='crate', y='crate_next'), data=data) + geom_point(size = 40, alpha = 0.8) + xlab("2012 Conversion Rate") + ylab("2013 Conversion Rate") + geom_abline(slope = 1, intercept = 0, colour = "red", linetype = "dotted") + geom_abline(slope = 0.0831, intercept =  0.1470)
ggplot(aes(x='crate', y='crate_next', colour = 'tmchange'), data=data) + geom_point(size = 40, alpha = 0.8) + xlab("2012 Conversion Rate") + ylab("2013 Conversion Rate") + geom_abline(slope = 1, intercept = 0, colour = "red", linetype = "dotted") + geom_smooth(method = "lm")

# conversion vs shot qual

ggplot(aes(x='shotq', y='conv'), data=stack) + geom_point() + xlab("Proportion of Shots in Area") + ylab("Conversion Rate")



## plotly graphs
import plotly.plotly as ply 
from plotly.graph_objs import *
py.sign_in("jharkins", "q7txy0n46q")

## simple scatter
trace1 = Scatter(x=x,y=y, text = data['name'], mode = 'markers', marker = Marker(color = 'blue', size = 10))
gdata = Data([trace1])

layout = Layout(hovermode = 'closest', xaxis = XAxis(title="2012 Conversion Rate"), yaxis = YAxis(title= "2013 Conversion Rate"))
ply.plot(data = gdata, layout = layout)


## broken out by team change
smtrace = Scatter(x = same['crate'], y = same['crate_next'], text = same['name'], mode = 'markers', marker = Marker(color = 'blue', size = 10))

chgtrace = Scatter(x = changed['crate'], y = changed['crate_next'],text = changed['name'], mode = 'markers', marker = Marker(color = 'orange', size = 10))
gdata3 = Data([chgtrace,smtrace])
fig3 = Figure(data = gdata3, layout = layout)

#regression
import statsmodels.api as sm
chgonly = data[data['tmchange'] == 1]
stayonly = data[data['tmchange'] == 0]
#onescol = np.ones((len(df),))
coeffs = []
for df in [chgonly,stayonly]:
	Y = df['crate_next'] 
	X = df['crate']
	X = sm.add_constant(X)
	result = sm.OLS(Y, X).fit()
	#print(result.summary())
	coeffs.append(result.params)

#plot with two regression lines, no intervals
ggplot(aes(x='crate', y='crate_next', colour = 'Team Change'), data=data) + geom_point(size = 40, alpha = 0.8) + xlab("2012 Conversion Rate") + ylab("2013 Conversion Rate") + geom_abline(slope = coeffs[0][1], intercept = coeffs[0][0], colour= "#f8766d") + geom_abline(slope = coeffs[1][1], intercept = coeffs[1][0], colour= "#00bfc4")

# full regression
Y = data['crate_next'] 
X = data[['crate', 'tmchange', 'in_area_prop_next']]
X = sm.add_constant(X)
result = sm.OLS(Y, X).fit()
print(result.summary())

Y = chgonly['crate_next'] 
X = chgonly[['crate', 'in_area_prop_next']]
X = sm.add_constant(X)
result = sm.OLS(Y, X).fit()
print(result.summary())