select name,description from Events where Events.venueId = 0;
select firstname,lastname from Artist outer join ArtistToEvent on Artist.id = ArtistToEvent.artistId
and ArtistToEvent.eventId = 0;