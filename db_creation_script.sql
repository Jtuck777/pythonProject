-- SJSU CMPE138 Team5 Project

-- 1. drop the database trainNet if it exists
-- 2. create the database trainNet
-- 3. set the current DB context to the newly created database, and then execute the DDL statements.

-- we don't need this drop stuff because we're using sqlite3 I think
-- drop database if exists trainNet;
-- create database trainNet;
-- use trainNet;

create table STATION (
	Sname    varchar(20) not null,
    location text        not null,
    primary key (Sname)
);

create table PASSENGER (
	Username varchar(15) not null,
	HashPass varchar(60)    not null,
    Fname    varchar(15) not null,
    Lname    varchar(15) not null,
    CardNum  char(16)    not null,
    ExpData  char(4)     not null,
    CVC      char(3)     not null,
    primary key (Username)
);

create table TICKET (
	Tnumber        int         not null,
    PurchDate      date        not null,
    ArrivalStation varchar(20) not null,
    DepartStation  varchar(20) not null,
    OwnerUser      varchar(15) not null,
    primary key (Tnumber),
    foreign key (ArrivalStation) references STATION(Sname)
		on delete cascade
        on update cascade,
    foreign key (DepartStation) references STATION(Sname)
		on delete cascade
        on update cascade,
    foreign key (OwnerUser) references PASSENGER(Username)
		on delete cascade
        on update cascade
);

create table TRAIN_TYPE (
	TType    varchar(20) not null,
    capacity int         not null,
    primary key (TType)
);

create table TRAIN_LINE (
	LineName     varchar(15) not null,
    LineColor    varchar(10) not null,
    TType        varchar(20) not null,
    StartStation varchar(20) not null,
    EndStation   varchar(20) not null,
    primary key (LineName),
    unique (LineColor),
    foreign key (TType) references TRAIN_TYPE(TType)
		on delete restrict
        on update cascade,
    foreign key (StartStation) references STATION(Sname)
		on delete restrict
        on update cascade,
    foreign key (EndStation) references STATION(Sname)
		on delete restrict
        on update cascade
);

create table EMPLOYEE (
	Username  varchar(15) not null,
    HashPass  char(60)    not null,
    Fname     varchar(15) not null,
    Lname     varchar(15) not null,
    StartDate date        not null,
    JobType   varchar(10) not null,
    primary key (Username)
);

create table TRAIN_LINE_INSTANCE (
	TrainNumber int         not null,
    TDate       date        not null,
    LineName    varchar(15) not null,
    OperatedBy  varchar(15) not null,
    primary key (TrainNumber, TDate),
    foreign key (LineName) references TRAIN_LINE(LineName)
		on delete cascade
        on update cascade,
    foreign key (OperatedBy) references EMPLOYEE(Username)
		on delete restrict
        on update cascade
);

create table TRAIN_SCHEDULE (
	TrainNumber        int          not null,
    TDate              date         not null,
    SName              varchar(20) not null,
    PlannedArrivalTime time         not null,
    ActualArrivalTime  time,
    ActualDepartTime   time,
    primary key (TrainNumber, TDate, SName),
    foreign key (TrainNumber, Tdate) references TRAIN_LINE_INSTANCE(TrainNumber, TDate)
		on delete cascade
        on update cascade,
    foreign key (SName) references STATION(SName)
		on delete cascade
        on update cascade
);

create table MANAGES (
	Username varchar(15) not null,
    LineName varchar(15) not null,
    primary key (Username, LineName),
    foreign key (Username) references EMPLOYEE(Username)
		on delete restrict
        on update cascade,
    foreign key (LineName) references TRAIN_LINE(LineName)
		on delete cascade
        on update cascade
);

create table VISITS (
    LineName varchar(15) not null,
    SName    varchar(20) not null,
    primary key (LineName, SName),
    foreign key (LineName) references TRAIN_LINE(LineName)
		on delete cascade
        on update cascade,
    foreign key (SName) references STATION(SName)
		on delete cascade
        on update cascade
);

insert into STATION values ('Gilroy', '7150 Monterey St., Gilroy 95020'),
	('San Jose Diridon', '65 Cahill St., San Jose 95110'),
	('Mountain View', '600 W. Evelyn Ave., Mountain View 94041'),
	('Palo Alto', '95 University Ave., Palo Alto 94301'),
	('San Mateo', '385 First Ave., San Mateo 94401'),
	('Millbrae', '100 California Drive, Millbrae 94030'),
	('South San Francisco', '590 Dubuque Ave., South SF 94080'),
	('San Francisco', '700 4th St., San Francisco 94107');

insert into PASSENGER values
	('KingBradley', 'password', 'Brad', 'Styles', '1234567890123456', '0125', '123'),
	('theman42', 'password', 'Josh', 'Evans', '9999888877776666', '1124', '999'),
	('coolmath', 'password', 'John', 'Doe', '3333444455556666', '0823', '987');

insert into TICKET values
	(0, '2022-10-31', 'San Jose Diridon', 'San Francisco', 'KingBradley'),
	(1, '2022-10-31', 'San Francisco', 'San Jose Diridon', 'KingBradley'),
	(2, '2022-11-01', 'San Jose Diridon', 'San Francisco', 'KingBradley'),
	(3, '2022-11-01', 'Palo Alto','Millbrae','theman42'),
	(4, '2022-11-01','San Francisco','San Jose Diridon','KingBradley'),
	(5, '2022-11-02', 'San Jose Diridon', 'San Francisco', 'KingBradley'),
	(6, '2022-11-02', 'San Francisco', 'San Jose Diridon', 'KingBradley'),
	(7, '2022-11-03', 'San Jose Diridon', 'San Francisco', 'KingBradley'),
	(8, '2022-11-03', 'San Francisco', 'San Jose Diridon', 'KingBradley'),
	(9, '2022-11-04', 'San Jose Diridon', 'San Francisco', 'KingBradley'),
	(10, '2022-11-04', 'Millbrae', 'Palo Alto', 'theman42'),
	(11, '2022-11-04', 'Gilroy', 'South San Francisco', 'coolmath'),
	(12, '2022-11-04', 'San Francisco', 'San Jose Diridon', 'KingBradley');

insert into TRAIN_TYPE values
	('Electric' ,300),
	('Diesel', 200);

insert into TRAIN_LINE values
	('Local NB', 'Green', 'Diesel', 'Gilroy', 'San Francisco'),
	('Local SB', 'Blue', 'Diesel', 'San Francisco', 'Gilroy'),
	('Bullet NB', 'Red', 'Electric', 'San Jose Diridon', 'San Francisco'),
	('Bullet SB', 'Orange', 'Electric', 'San Francisco', 'San Jose Diridon');

insert into EMPLOYEE values
	('ilovetrains', 'password', 'Ray', 'Bradbury', '2020-08-22', 'Driver'),
	('trainsRcool', 'password', 'Carl', 'West', '2000-04-01', 'Driver'),
	('IwannaGOfast', 'password', 'Jeff', 'Gordon', '2012-12-03', 'Driver'),
	('ilovepower', 'password', 'Gordon', 'Freeman', '1999-12-31', 'Admin'),
	('xboxluver', 'password', 'Bill', 'Gates', '1970-01-01', 'Controller');

insert into TRAIN_LINE_INSTANCE values
	(100,'2022-10-31','Local NB','ilovetrains'),
	(101,'2022-10-31','Local SB','trainsRcool'),
	(500,'2022-10-31','Bullet NB','IwannaGOfast'),
	(102,'2022-10-31','Local NB','trainsRcool'),
	(103,'2022-10-31','Local SB','ilovetrains'),
	(104,'2022-10-31','Local NB','ilovetrains'),
	(105,'2022-10-31','Local SB','trainsRcool'),
	(106,'2022-10-31','Local NB','trainsRcool'),
	(107,'2022-10-31','Local SB','ilovetrains'),
	(501,'2022-10-31','Bullet SB','IwannaGOfast'),

	(100,'2022-11-01','Local NB','ilovetrains'),
	(101,'2022-11-01','Local SB','trainsRcool'),
	(500,'2022-11-01','Bullet NB','IwannaGOfast'),
	(102,'2022-11-01','Local NB','trainsRcool'),
	(103,'2022-11-01','Local SB','ilovetrains'),
	(104,'2022-11-01','Local NB','ilovetrains'),
	(105,'2022-11-01','Local SB','trainsRcool'),
	(106,'2022-11-01','Local NB','trainsRcool'),
	(107,'2022-11-01','Local SB','ilovetrains'),
	(501,'2022-11-01','Bullet SB','IwannaGOfast'),

	(100,'2022-11-02','Local NB','ilovetrains'),
	(101,'2022-11-02','Local SB','trainsRcool'),
	(500,'2022-11-02','Bullet NB','IwannaGOfast'),
	(102,'2022-11-02','Local NB','trainsRcool'),
	(103,'2022-11-02','Local SB','ilovetrains'),
	(104,'2022-11-02','Local NB','ilovetrains'),
	(105,'2022-11-02','Local SB','trainsRcool'),
	(106,'2022-11-02','Local NB','trainsRcool'),
	(107,'2022-11-02','Local SB','ilovetrains'),
	(501,'2022-11-02','Bullet SB','IwannaGOfast'),

	(100,'2022-11-03','Local NB','ilovetrains'),
	(101,'2022-11-03','Local SB','trainsRcool'),
	(500,'2022-11-03','Bullet NB','IwannaGOfast'),
	(102,'2022-11-03','Local NB','trainsRcool'),
	(103,'2022-11-03','Local SB','ilovetrains'),
	(104,'2022-11-03','Local NB','ilovetrains'),
	(105,'2022-11-03','Local SB','trainsRcool'),
	(106,'2022-11-03','Local NB','trainsRcool'),
	(107,'2022-11-03','Local SB','ilovetrains'),
	(501,'2022-11-03','Bullet SB','IwannaGOfast'),

	(100,'2022-11-04','Local NB','ilovetrains'),
	(101,'2022-11-04','Local SB','trainsRcool'),
	(500,'2022-11-04','Bullet NB','IwannaGOfast'),
	(102,'2022-11-04','Local NB','trainsRcool'),
	(103,'2022-11-04','Local SB','ilovetrains'),
	(104,'2022-11-04','Local NB','ilovetrains'),
	(105,'2022-11-04','Local SB','trainsRcool'),
	(106,'2022-11-04','Local NB','trainsRcool'),
	(107,'2022-11-04','Local SB','ilovetrains'),
	(501,'2022-11-04','Bullet SB','IwannaGOfast');

insert into TRAIN_SCHEDULE values
	(100,'2022-10-31','Gilroy','6:00:00','6:00:00','6:02:00'),
	(100,'2022-10-31','San Jose Diridon','6:15:00','6:15:00','6:17:00'),
	(100,'2022-10-31','Mountain View','6:25:00','6:25:00','6:27:00'),
	(100,'2022-10-31','Palo Alto','6:30:00','6:30:00','6:32:00'),
	(100,'2022-10-31','San Mateo','6:40:00','6:40:00','6:42:00'),
	(100,'2022-10-31','Millbrae','6:45:00','6:45:00','6:47:00'),
	(100,'2022-10-31','South San Francisco','6:50:00','6:50:00','6:52:00'),
	(100,'2022-10-31','San Francisco','7:00:00','7:00:00','7:02:00'),

	(101,'2022-10-31','San Francisco','6:00:00','6:00:00','6:02:00'),
	(101,'2022-10-31','South San Francisco','6:10:00','6:10:00','6:12:00'),
	(101,'2022-10-31','Millbrae','6:15:00','6:15:00','6:17:00'),
	(101,'2022-10-31','San Mateo','6:20:00','6:20:00','6:22:00'),
	(101,'2022-10-31','Palo Alto','6:30:00','6:30:00','6:32:00'),
	(101,'2022-10-31','Mountain View','6:35:00','6:35:00','6:37:00'),
	(101,'2022-10-31','San Jose Diridon','6:45:00','6:45:00','6:47:00'),
	(101,'2022-10-31','Gilroy','7:00:00','7:00:00','7:02:00'),

	(500,'2022-10-31','San Jose Diridon','6:00:00','6:00:00','6:02:00'),
	(500,'2022-10-31','San Francisco','6:30:00','6:30:00','6:32:00'),

	(102,'2022-10-31','Gilroy','10:00:00','10:00:00','10:02:00'),
	(102,'2022-10-31','San Jose Diridon','10:15:00','10:15:00','10:17:00'),
	(102,'2022-10-31','Mountain View','10:25:00','10:25:00','10:27:00'),
	(102,'2022-10-31','Palo Alto','10:30:00','10:30:00','10:32:00'),
	(102,'2022-10-31','San Mateo','10:40:00','10:40:00','10:42:00'),
	(102,'2022-10-31','Millbrae','10:45:00','10:45:00','10:47:00'),
	(102,'2022-10-31','South San Francisco','10:50:00','10:50:00','10:52:00'),
	(102,'2022-10-31','San Francisco','11:00:00','11:00:00','11:02:00'),

	(103,'2022-10-31','San Francisco','10:00:00','10:00:00','10:02:00'),
	(103,'2022-10-31','South San Francisco','10:10:00','10:10:00','10:12:00'),
	(103,'2022-10-31','Millbrae','10:15:00','10:15:00','10:17:00'),
	(103,'2022-10-31','San Mateo','10:20:00','10:20:00','10:22:00'),
	(103,'2022-10-31','Palo Alto','10:30:00','10:30:00','10:32:00'),
	(103,'2022-10-31','Mountain View','10:35:00','10:35:00','10:37:00'),
	(103,'2022-10-31','San Jose Diridon','10:45:00','10:45:00','10:47:00'),
	(103,'2022-10-31','Gilroy','11:00:00','11:00:00','11:02:00'),

	(104,'2022-10-31','Gilroy','14:00:00','14:00:00','14:02:00'),
	(104,'2022-10-31','San Jose Diridon','14:15:00','14:15:00','14:17:00'),
	(104,'2022-10-31','Mountain View','14:25:00','14:25:00','14:27:00'),
	(104,'2022-10-31','Palo Alto','14:30:00','14:30:00','14:32:00'),
	(104,'2022-10-31','San Mateo','14:40:00','14:40:00','14:42:00'),
	(104,'2022-10-31','Millbrae','14:45:00','14:45:00','14:47:00'),
	(104,'2022-10-31','South San Francisco','14:50:00','14:50:00','14:52:00'),
	(104,'2022-10-31','San Francisco','15:00:00','15:00:00','15:02:00'),

	(105,'2022-10-31','San Francisco','14:00:00','14:00:00','14:02:00'),
	(105,'2022-10-31','South San Francisco','14:10:00','14:10:00','14:12:00'),
	(105,'2022-10-31','Millbrae','14:15:00','14:15:00','14:17:00'),
	(105,'2022-10-31','San Mateo','14:20:00','14:20:00','14:22:00'),
	(105,'2022-10-31','Palo Alto','14:30:00','14:30:00','14:32:00'),
	(105,'2022-10-31','Mountain View','14:35:00','14:35:00','14:37:00'),
	(105,'2022-10-31','San Jose Diridon','14:45:00','14:45:00','14:47:00'),
	(105,'2022-10-31','Gilroy','15:00:00','15:00:00','15:02:00'),

	(106,'2022-10-31','Gilroy','18:00:00','18:00:00','18:02:00'),
	(106,'2022-10-31','San Jose Diridon','18:15:00','18:15:00','18:17:00'),
	(106,'2022-10-31','Mountain View','18:25:00','18:25:00','18:27:00'),
	(106,'2022-10-31','Palo Alto','18:30:00','18:30:00','18:32:00'),
	(106,'2022-10-31','San Mateo','18:40:00','18:40:00','18:42:00'),
	(106,'2022-10-31','Millbrae','18:45:00','18:45:00','18:47:00'),
	(106,'2022-10-31','South San Francisco','18:50:00','18:50:00','18:52:00'),
	(106,'2022-10-31','San Francisco','19:00:00','19:00:00','19:02:00'),

	(107,'2022-10-31','San Francisco','18:00:00','18:00:00','18:02:00'),
	(107,'2022-10-31','South San Francisco','18:10:00','18:10:00','18:12:00'),
	(107,'2022-10-31','Millbrae','18:15:00','18:15:00','18:17:00'),
	(107,'2022-10-31','San Mateo','18:20:00','18:20:00','18:22:00'),
	(107,'2022-10-31','Palo Alto','18:30:00','18:30:00','18:32:00'),
	(107,'2022-10-31','Mountain View','18:35:00','18:35:00','18:37:00'),
	(107,'2022-10-31','San Jose Diridon','18:45:00','18:45:00','18:47:00'),
	(107,'2022-10-31','Gilroy','19:00:00','19:00:00','19:02:00'),

	(501,'2022-10-31','San Francisco','18:00:00','18:00:00','18:02:00'),
	(501,'2022-10-31','San Jose Diridon','18:30:00','18:30:00','18:32:00'),

    (100,'2022-11-01','Gilroy','6:00:00','6:00:00','6:02:00'),
	(100,'2022-11-01','San Jose Diridon','6:15:00','6:15:00','6:17:00'),
	(100,'2022-11-01','Mountain View','6:25:00','6:25:00','6:27:00'),
	(100,'2022-11-01','Palo Alto','6:30:00','6:30:00','6:32:00'),
	(100,'2022-11-01','San Mateo','6:40:00','6:40:00','6:42:00'),
	(100,'2022-11-01','Millbrae','6:45:00','6:45:00','6:47:00'),
	(100,'2022-11-01','South San Francisco','6:50:00','6:50:00','6:52:00'),
	(100,'2022-11-01','San Francisco','7:00:00','7:00:00','7:02:00'),

	(101,'2022-11-01','San Francisco','6:00:00','6:00:00','6:02:00'),
	(101,'2022-11-01','South San Francisco','6:10:00','6:10:00','6:12:00'),
	(101,'2022-11-01','Millbrae','6:15:00','6:15:00','6:17:00'),
	(101,'2022-11-01','San Mateo','6:20:00','6:20:00','6:22:00'),
	(101,'2022-11-01','Palo Alto','6:30:00','6:30:00','6:32:00'),
	(101,'2022-11-01','Mountain View','6:35:00','6:35:00','6:37:00'),
	(101,'2022-11-01','San Jose Diridon','6:45:00','6:45:00','6:47:00'),
	(101,'2022-11-01','Gilroy','7:00:00','7:00:00','7:02:00'),

	(500,'2022-11-01','San Jose Diridon','6:00:00','6:00:00','6:02:00'),
	(500,'2022-11-01','San Francisco','6:30:00','6:30:00','6:32:00'),

	(102,'2022-11-01','Gilroy','10:00:00','10:00:00','10:02:00'),
	(102,'2022-11-01','San Jose Diridon','10:15:00','10:15:00','10:17:00'),
	(102,'2022-11-01','Mountain View','10:25:00','10:25:00','10:27:00'),
	(102,'2022-11-01','Palo Alto','10:30:00','10:30:00','10:32:00'),
	(102,'2022-11-01','San Mateo','10:40:00','10:40:00','10:42:00'),
	(102,'2022-11-01','Millbrae','10:45:00','10:45:00','10:47:00'),
	(102,'2022-11-01','South San Francisco','10:50:00','10:50:00','10:52:00'),
	(102,'2022-11-01','San Francisco','11:00:00','11:00:00','11:02:00'),

	(103,'2022-11-01','San Francisco','10:00:00','10:00:00','10:02:00'),
	(103,'2022-11-01','South San Francisco','10:10:00','10:10:00','10:12:00'),
	(103,'2022-11-01','Millbrae','10:15:00','10:15:00','10:17:00'),
	(103,'2022-11-01','San Mateo','10:20:00','10:20:00','10:22:00'),
	(103,'2022-11-01','Palo Alto','10:30:00','10:30:00','10:32:00'),
	(103,'2022-11-01','Mountain View','10:35:00','10:35:00','10:37:00'),
	(103,'2022-11-01','San Jose Diridon','10:45:00','10:45:00','10:47:00'),
	(103,'2022-11-01','Gilroy','11:00:00','11:00:00','11:02:00'),

	(104,'2022-11-01','Gilroy','14:00:00','14:00:00','14:02:00'),
	(104,'2022-11-01','San Jose Diridon','14:15:00','14:15:00','14:17:00'),
	(104,'2022-11-01','Mountain View','14:25:00','14:25:00','14:27:00'),
	(104,'2022-11-01','Palo Alto','14:30:00','14:30:00','14:32:00'),
	(104,'2022-11-01','San Mateo','14:40:00','14:40:00','14:42:00'),
	(104,'2022-11-01','Millbrae','14:45:00','14:45:00','14:47:00'),
	(104,'2022-11-01','South San Francisco','14:50:00','14:50:00','14:52:00'),
	(104,'2022-11-01','San Francisco','15:00:00','15:00:00','15:02:00'),

	(105,'2022-11-01','San Francisco','14:00:00','14:00:00','14:02:00'),
	(105,'2022-11-01','South San Francisco','14:10:00','14:10:00','14:12:00'),
	(105,'2022-11-01','Millbrae','14:15:00','14:15:00','14:17:00'),
	(105,'2022-11-01','San Mateo','14:20:00','14:20:00','14:22:00'),
	(105,'2022-11-01','Palo Alto','14:30:00','14:30:00','14:32:00'),
	(105,'2022-11-01','Mountain View','14:35:00','14:35:00','14:37:00'),
	(105,'2022-11-01','San Jose Diridon','14:45:00','14:45:00','14:47:00'),
	(105,'2022-11-01','Gilroy','15:00:00','15:00:00','15:02:00'),

	(106,'2022-11-01','Gilroy','18:00:00','18:00:00','18:02:00'),
	(106,'2022-11-01','San Jose Diridon','18:15:00','18:15:00','18:17:00'),
	(106,'2022-11-01','Mountain View','18:25:00','18:25:00','18:27:00'),
	(106,'2022-11-01','Palo Alto','18:30:00','18:30:00','18:32:00'),
	(106,'2022-11-01','San Mateo','18:40:00','18:40:00','18:42:00'),
	(106,'2022-11-01','Millbrae','18:45:00','18:45:00','18:47:00'),
	(106,'2022-11-01','South San Francisco','18:50:00','18:50:00','18:52:00'),
	(106,'2022-11-01','San Francisco','19:00:00','19:00:00','19:02:00'),

	(107,'2022-11-01','San Francisco','18:00:00','18:00:00','18:02:00'),
	(107,'2022-11-01','South San Francisco','18:10:00','18:10:00','18:12:00'),
	(107,'2022-11-01','Millbrae','18:15:00','18:15:00','18:17:00'),
	(107,'2022-11-01','San Mateo','18:20:00','18:20:00','18:22:00'),
	(107,'2022-11-01','Palo Alto','18:30:00','18:30:00','18:32:00'),
	(107,'2022-11-01','Mountain View','18:35:00','18:35:00','18:37:00'),
	(107,'2022-11-01','San Jose Diridon','18:45:00','18:45:00','18:47:00'),
	(107,'2022-11-01','Gilroy','19:00:00','19:00:00','19:02:00'),

	(501,'2022-11-01','San Francisco','18:00:00','18:00:00','18:02:00'),
	(501,'2022-11-01','San Jose Diridon','18:30:00','18:30:00','18:32:00'),

    (100,'2022-11-02','Gilroy','6:00:00',null,null),
	(100,'2022-11-02','San Jose Diridon','6:15:00',null,null),
	(100,'2022-11-02','Mountain View','6:25:00',null,null),
	(100,'2022-11-02','Palo Alto','6:30:00',null,null),
	(100,'2022-11-02','San Mateo','6:40:00',null,null),
	(100,'2022-11-02','Millbrae','6:45:00',null,null),
	(100,'2022-11-02','South San Francisco','6:50:00',null,null),
	(100,'2022-11-02','San Francisco','7:00:00',null,null),

	(101,'2022-11-02','San Francisco','6:00:00',null,null),
	(101,'2022-11-02','South San Francisco','6:10:00',null,null),
	(101,'2022-11-02','Millbrae','6:15:00',null,null),
	(101,'2022-11-02','San Mateo','6:20:00',null,null),
	(101,'2022-11-02','Palo Alto','6:30:00',null,null),
	(101,'2022-11-02','Mountain View','6:35:00',null,null),
	(101,'2022-11-02','San Jose Diridon','6:45:00',null,null),
	(101,'2022-11-02','Gilroy','7:00:00',null,null),

	(500,'2022-11-02','San Jose Diridon','6:00:00',null,null),
	(500,'2022-11-02','San Francisco','6:30:00',null,null),

	(102,'2022-11-02','Gilroy','10:00:00',null,null),
	(102,'2022-11-02','San Jose Diridon','10:15:00',null,null),
	(102,'2022-11-02','Mountain View','10:25:00',null,null),
	(102,'2022-11-02','Palo Alto','10:30:00',null,null),
	(102,'2022-11-02','San Mateo','10:40:00',null,null),
	(102,'2022-11-02','Millbrae','10:45:00',null,null),
	(102,'2022-11-02','South San Francisco','10:50:00',null,null),
	(102,'2022-11-02','San Francisco','11:00:00',null,null),

	(103,'2022-11-02','San Francisco','10:00:00',null,null),
	(103,'2022-11-02','South San Francisco','10:10:00',null,null),
	(103,'2022-11-02','Millbrae','10:15:00',null,null),
	(103,'2022-11-02','San Mateo','10:20:00',null,null),
	(103,'2022-11-02','Palo Alto','10:30:00',null,null),
	(103,'2022-11-02','Mountain View','10:35:00',null,null),
	(103,'2022-11-02','San Jose Diridon','10:45:00',null,null),
	(103,'2022-11-02','Gilroy','11:00:00',null,null),

	(104,'2022-11-02','Gilroy','14:00:00',null,null),
	(104,'2022-11-02','San Jose Diridon','14:15:00',null,null),
	(104,'2022-11-02','Mountain View','14:25:00',null,null),
	(104,'2022-11-02','Palo Alto','14:30:00',null,null),
	(104,'2022-11-02','San Mateo','14:40:00',null,null),
	(104,'2022-11-02','Millbrae','14:45:00',null,null),
	(104,'2022-11-02','South San Francisco','14:50:00',null,null),
	(104,'2022-11-02','San Francisco','15:00:00',null,null),

	(105,'2022-11-02','San Francisco','14:00:00',null,null),
	(105,'2022-11-02','South San Francisco','14:10:00',null,null),
	(105,'2022-11-02','Millbrae','14:15:00',null,null),
	(105,'2022-11-02','San Mateo','14:20:00',null,null),
	(105,'2022-11-02','Palo Alto','14:30:00',null,null),
	(105,'2022-11-02','Mountain View','14:35:00',null,null),
	(105,'2022-11-02','San Jose Diridon','14:45:00',null,null),
	(105,'2022-11-02','Gilroy','15:00:00',null,null),

	(106,'2022-11-02','Gilroy','18:00:00',null,null),
	(106,'2022-11-02','San Jose Diridon','18:15:00',null,null),
	(106,'2022-11-02','Mountain View','18:25:00',null,null),
	(106,'2022-11-02','Palo Alto','18:30:00',null,null),
	(106,'2022-11-02','San Mateo','18:40:00',null,null),
	(106,'2022-11-02','Millbrae','18:45:00',null,null),
	(106,'2022-11-02','South San Francisco','18:50:00',null,null),
	(106,'2022-11-02','San Francisco','19:00:00',null,null),

	(107,'2022-11-02','San Francisco','18:00:00',null,null),
	(107,'2022-11-02','South San Francisco','18:10:00',null,null),
	(107,'2022-11-02','Millbrae','18:15:00',null,null),
	(107,'2022-11-02','San Mateo','18:20:00',null,null),
	(107,'2022-11-02','Palo Alto','18:30:00',null,null),
	(107,'2022-11-02','Mountain View','18:35:00',null,null),
	(107,'2022-11-02','San Jose Diridon','18:45:00',null,null),
	(107,'2022-11-02','Gilroy','19:00:00',null,null),

	(501,'2022-11-02','San Francisco','18:00:00',null,null),
	(501,'2022-11-02','San Jose Diridon','18:30:00',null,null),

    (100,'2022-11-03','Gilroy','6:00:00',null,null),
	(100,'2022-11-03','San Jose Diridon','6:15:00',null,null),
	(100,'2022-11-03','Mountain View','6:25:00',null,null),
	(100,'2022-11-03','Palo Alto','6:30:00',null,null),
	(100,'2022-11-03','San Mateo','6:40:00',null,null),
	(100,'2022-11-03','Millbrae','6:45:00',null,null),
	(100,'2022-11-03','South San Francisco','6:50:00',null,null),
	(100,'2022-11-03','San Francisco','7:00:00',null,null),

	(101,'2022-11-03','San Francisco','6:00:00',null,null),
	(101,'2022-11-03','South San Francisco','6:10:00',null,null),
	(101,'2022-11-03','Millbrae','6:15:00',null,null),
	(101,'2022-11-03','San Mateo','6:20:00',null,null),
	(101,'2022-11-03','Palo Alto','6:30:00',null,null),
	(101,'2022-11-03','Mountain View','6:35:00',null,null),
	(101,'2022-11-03','San Jose Diridon','6:45:00',null,null),
	(101,'2022-11-03','Gilroy','7:00:00',null,null),

	(500,'2022-11-03','San Jose Diridon','6:00:00',null,null),
	(500,'2022-11-03','San Francisco','6:30:00',null,null),

	(102,'2022-11-03','Gilroy','10:00:00',null,null),
	(102,'2022-11-03','San Jose Diridon','10:15:00',null,null),
	(102,'2022-11-03','Mountain View','10:25:00',null,null),
	(102,'2022-11-03','Palo Alto','10:30:00',null,null),
	(102,'2022-11-03','San Mateo','10:40:00',null,null),
	(102,'2022-11-03','Millbrae','10:45:00',null,null),
	(102,'2022-11-03','South San Francisco','10:50:00',null,null),
	(102,'2022-11-03','San Francisco','11:00:00',null,null),

	(103,'2022-11-03','San Francisco','10:00:00',null,null),
	(103,'2022-11-03','South San Francisco','10:10:00',null,null),
	(103,'2022-11-03','Millbrae','10:15:00',null,null),
	(103,'2022-11-03','San Mateo','10:20:00',null,null),
	(103,'2022-11-03','Palo Alto','10:30:00',null,null),
	(103,'2022-11-03','Mountain View','10:35:00',null,null),
	(103,'2022-11-03','San Jose Diridon','10:45:00',null,null),
	(103,'2022-11-03','Gilroy','11:00:00',null,null),

	(104,'2022-11-03','Gilroy','14:00:00',null,null),
	(104,'2022-11-03','San Jose Diridon','14:15:00',null,null),
	(104,'2022-11-03','Mountain View','14:25:00',null,null),
	(104,'2022-11-03','Palo Alto','14:30:00',null,null),
	(104,'2022-11-03','San Mateo','14:40:00',null,null),
	(104,'2022-11-03','Millbrae','14:45:00',null,null),
	(104,'2022-11-03','South San Francisco','14:50:00',null,null),
	(104,'2022-11-03','San Francisco','15:00:00',null,null),

	(105,'2022-11-03','San Francisco','14:00:00',null,null),
	(105,'2022-11-03','South San Francisco','14:10:00',null,null),
	(105,'2022-11-03','Millbrae','14:15:00',null,null),
	(105,'2022-11-03','San Mateo','14:20:00',null,null),
	(105,'2022-11-03','Palo Alto','14:30:00',null,null),
	(105,'2022-11-03','Mountain View','14:35:00',null,null),
	(105,'2022-11-03','San Jose Diridon','14:45:00',null,null),
	(105,'2022-11-03','Gilroy','15:00:00',null,null),

	(106,'2022-11-03','Gilroy','18:00:00',null,null),
	(106,'2022-11-03','San Jose Diridon','18:15:00',null,null),
	(106,'2022-11-03','Mountain View','18:25:00',null,null),
	(106,'2022-11-03','Palo Alto','18:30:00',null,null),
	(106,'2022-11-03','San Mateo','18:40:00',null,null),
	(106,'2022-11-03','Millbrae','18:45:00',null,null),
	(106,'2022-11-03','South San Francisco','18:50:00',null,null),
	(106,'2022-11-03','San Francisco','19:00:00',null,null),

	(107,'2022-11-03','San Francisco','18:00:00',null,null),
	(107,'2022-11-03','South San Francisco','18:10:00',null,null),
	(107,'2022-11-03','Millbrae','18:15:00',null,null),
	(107,'2022-11-03','San Mateo','18:20:00',null,null),
	(107,'2022-11-03','Palo Alto','18:30:00',null,null),
	(107,'2022-11-03','Mountain View','18:35:00',null,null),
	(107,'2022-11-03','San Jose Diridon','18:45:00',null,null),
	(107,'2022-11-03','Gilroy','19:00:00',null,null),

	(501,'2022-11-03','San Francisco','18:00:00',null,null),
	(501,'2022-11-03','San Jose Diridon','18:30:00',null,null),

    (100,'2022-11-04','Gilroy','6:00:00',null,null),
	(100,'2022-11-04','San Jose Diridon','6:15:00',null,null),
	(100,'2022-11-04','Mountain View','6:25:00',null,null),
	(100,'2022-11-04','Palo Alto','6:30:00',null,null),
	(100,'2022-11-04','San Mateo','6:40:00',null,null),
	(100,'2022-11-04','Millbrae','6:45:00',null,null),
	(100,'2022-11-04','South San Francisco','6:50:00',null,null),
	(100,'2022-11-04','San Francisco','7:00:00',null,null),

	(101,'2022-11-04','San Francisco','6:00:00',null,null),
	(101,'2022-11-04','South San Francisco','6:10:00',null,null),
	(101,'2022-11-04','Millbrae','6:15:00',null,null),
	(101,'2022-11-04','San Mateo','6:20:00',null,null),
	(101,'2022-11-04','Palo Alto','6:30:00',null,null),
	(101,'2022-11-04','Mountain View','6:35:00',null,null),
	(101,'2022-11-04','San Jose Diridon','6:45:00',null,null),
	(101,'2022-11-04','Gilroy','7:00:00',null,null),

	(500,'2022-11-04','San Jose Diridon','6:00:00',null,null),
	(500,'2022-11-04','San Francisco','6:30:00',null,null),

	(102,'2022-11-04','Gilroy','10:00:00',null,null),
	(102,'2022-11-04','San Jose Diridon','10:15:00',null,null),
	(102,'2022-11-04','Mountain View','10:25:00',null,null),
	(102,'2022-11-04','Palo Alto','10:30:00',null,null),
	(102,'2022-11-04','San Mateo','10:40:00',null,null),
	(102,'2022-11-04','Millbrae','10:45:00',null,null),
	(102,'2022-11-04','South San Francisco','10:50:00',null,null),
	(102,'2022-11-04','San Francisco','11:00:00',null,null),

	(103,'2022-11-04','San Francisco','10:00:00',null,null),
	(103,'2022-11-04','South San Francisco','10:10:00',null,null),
	(103,'2022-11-04','Millbrae','10:15:00',null,null),
	(103,'2022-11-04','San Mateo','10:20:00',null,null),
	(103,'2022-11-04','Palo Alto','10:30:00',null,null),
	(103,'2022-11-04','Mountain View','10:35:00',null,null),
	(103,'2022-11-04','San Jose Diridon','10:45:00',null,null),
	(103,'2022-11-04','Gilroy','11:00:00',null,null),

	(104,'2022-11-04','Gilroy','14:00:00',null,null),
	(104,'2022-11-04','San Jose Diridon','14:15:00',null,null),
	(104,'2022-11-04','Mountain View','14:25:00',null,null),
	(104,'2022-11-04','Palo Alto','14:30:00',null,null),
	(104,'2022-11-04','San Mateo','14:40:00',null,null),
	(104,'2022-11-04','Millbrae','14:45:00',null,null),
	(104,'2022-11-04','South San Francisco','14:50:00',null,null),
	(104,'2022-11-04','San Francisco','15:00:00',null,null),

	(105,'2022-11-04','San Francisco','14:00:00',null,null),
	(105,'2022-11-04','South San Francisco','14:10:00',null,null),
	(105,'2022-11-04','Millbrae','14:15:00',null,null),
	(105,'2022-11-04','San Mateo','14:20:00',null,null),
	(105,'2022-11-04','Palo Alto','14:30:00',null,null),
	(105,'2022-11-04','Mountain View','14:35:00',null,null),
	(105,'2022-11-04','San Jose Diridon','14:45:00',null,null),
	(105,'2022-11-04','Gilroy','15:00:00',null,null),

	(106,'2022-11-04','Gilroy','18:00:00',null,null),
	(106,'2022-11-04','San Jose Diridon','18:15:00',null,null),
	(106,'2022-11-04','Mountain View','18:25:00',null,null),
	(106,'2022-11-04','Palo Alto','18:30:00',null,null),
	(106,'2022-11-04','San Mateo','18:40:00',null,null),
	(106,'2022-11-04','Millbrae','18:45:00',null,null),
	(106,'2022-11-04','South San Francisco','18:50:00',null,null),
	(106,'2022-11-04','San Francisco','19:00:00',null,null),

	(107,'2022-11-04','San Francisco','18:00:00',null,null),
	(107,'2022-11-04','South San Francisco','18:10:00',null,null),
	(107,'2022-11-04','Millbrae','18:15:00',null,null),
	(107,'2022-11-04','San Mateo','18:20:00',null,null),
	(107,'2022-11-04','Palo Alto','18:30:00',null,null),
	(107,'2022-11-04','Mountain View','18:35:00',null,null),
	(107,'2022-11-04','San Jose Diridon','18:45:00',null,null),
	(107,'2022-11-04','Gilroy','19:00:00',null,null),

	(501,'2022-11-04','San Francisco','18:00:00',null,null),
	(501,'2022-11-04','San Jose Diridon','18:30:00',null,null);

insert into MANAGES values
	('xboxluver','Local NB'),
	('xboxluver','Local SB'),
	('xboxluver','Bullet NB'),
	('xboxluver','Bullet SB');

insert into VISITS values
	('Local NB','Gilroy'),
	('Local NB','San Jose Diridon'),
	('Local NB','Mountain View'),
	('Local NB','Palo Alto'),
	('Local NB','San Mateo'),
	('Local NB','Millbrae'),
	('Local NB','South San Francisco'),
	('Local NB','San Francisco'),

	('Local SB','San Francisco'),
	('Local SB','South San Francisco'),
	('Local SB','Millbrae'),
	('Local SB','San Mateo'),
	('Local SB','Palo Alto'),
	('Local SB','Mountain View'),
	('Local SB','San Jose Diridon'),
	('Local SB','Gilroy'),

	('Bullet NB','San Jose Diridon'),
	('Bullet NB','San Francisco'),

	('Bullet SB','San Francisco'),
	('Bullet SB','San Jose Diridon');