This is a Trip Planner at your service!

It consists of two crews.

1.  CreateDashboard creates a dashboard for the users to put in their trip requirements.
	Source location
	Trip start date
	Trip end date
	Type of trip
	Preferred destination weather
	Trip preferences

It creates a backend code based on the dashboard requirements mentioned in main.py and also a gradio-based frontend code to finally build up a cool dashboard.

2.  TripPlanner creates day-wise itineraries for each day of the trip for the suggested top three trip locations based on user needs fed in the 		user dashboard created by CreateDashboard. The itinerary includes transportation details from their source location, meal suggestions, as well 		as a few notes to keep in mind before travelling.

Just an additional note: Please run the app.py after CreateDashboard creates the Gradio frontend code (Better to run the gradio code manually I guess). Feed in the trip details in the browser and submit them for our TripPlanner to start working on the itinerary.

Thanks!