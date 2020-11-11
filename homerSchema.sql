create table Artist (
    id		integer primary key autoincrement,
    firstname 	varchar(64) not null,
    lastname   	varchar(64) not null,
    hometown 	varchar(120) not null,
    description varchar(5000)
);

create table ArtistToEvent (
    id		integer primary key autoincrement,
    artistId    integer,
    eventId integer
);

create table Events (
    id		integer primary key autoincrement,
    venueId integer,
    name    varchar(64),
    description varchar (1000)
);

create table Venue (
    id		integer primary key autoincrement,
    name    varchar(64),
    description varchar(1000)
);