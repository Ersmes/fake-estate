# fake-estate
This was my final project for CS50's Introduction to Computer Science course. It is a simple real estate Flask-based web app which uses the Realtor API to allow users to view and save properties. It requires a valid API key to function, which can be input to the "helpers.py" file. Independent of the API is the registration, login, and viewing of saved properties, which is managed through the Flask-Login extension and is persisted through the Flask-SQLAlchemy extension in a SQLite database named "fakeestate.db". The logo designs were made in GIMP, and the background image is a stock image from Google Images.
## future
Something I was unhappy with is the formatting of my code; there is plenty of overlapping in the CSS sheet which could be minimized through more modular classes and just better organization. If someone else was working on the styling alongside me on a development team or something, they probably would have a nightmare navigating the "style.css" sheet, as its long and contains so much redundancy. This was a result of laziness near the end of the development of the project, and is something I would like to fix if I were to ever return to this project, even though it would be a tedious task to do so. Migrating to a more open API would probably be the next order of business, as the Realtor API used severely limits the number of requests the app can make, and also requires a key which is a dependency I would love to be able to remove. If that promised land is impossible to reach and must be skipped, however, then there are several other ideas I've had for this app. Similar to CS50's Finance app, in which users are able to buy and sell imaginary stocks, being able to hypothetically sell and buy houses would also be an intriguing concept to implement. The modeling of real estate markets is something I also had in mind, and making this app like a kind of real estate investing game with some insane way to predict the housing market and future valuations of houses in an alternate universe is probably the absolute insanely farthest I would ever go.
## what i think
That's all there is to this project. I would probably call this my first *completed* computer science project ever. It was a great learning experience to work with the extensions and libraries Flask has to offer. Learning the ORM from SQLAlchemy was probably one of the most time-consuming parts of this project, and also learning the flexbox layout properties was difficult. Near the end of the project, I started to feel definitely more comfortable formatting and styling the page. I think that, in the end, the styling of the website was one of the best things I did in this project. That's not to say its good, but I like to think that I exhibited some kind of art and design skills. I definitely wasn't completely happy with the project, as the overall "vibe" of the website did not match with my original intention, and I was never able to figure out how to make that work. Code wise, learning AJAX was probably the coolest thing. The "Save Property" button was the subject of my thought for the longest time and I had no idea how to figure it out and make it work the way I wanted it to. However, when I stumbled upon AJAX, I felt like I had found the Holy Grail or something. Credit for that goes to Miguel Grinberg, whose Flask Mega-Tutorial was absolutely invaluable. If you've read this far, I'm about to say some self-analysis stuff so cover your eyes. I think overall, this has been one of the most gratifying things I've ever done on a computer. The days of incomplete Java games are over and I think completing this project has helped me mature a ton. CS50 is really cool.
