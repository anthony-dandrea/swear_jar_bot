create table comments (
    id integer primary key autoincrement,
    user text not null,
    swear_comment text not null,
    paid integer not null
);
