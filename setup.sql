create table entries (
  id    integer not null primary key,
  group_id  integer not null,
  date_string   text not null,
  time  integer not null,
  fee   integer not null,
  notes text,
  pending   integer not null default 1
);

create table groups (
  id    integer not null primary key,
  name  text not null,
  email text not null,
  payer text not null,
  active    integer not null default 1
); 
