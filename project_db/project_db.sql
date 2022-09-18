DROP TABLE HOTELROOMS;
DROP TABLE V_SEATS;
DROP TABLE vehicledetails;
DROP TABLE hoteldetails;
DROP TABLE travel_agency;
DROP TABLE tourist_places;
DROP TABLE hotel_site;
DROP TABLE C_BOOKINGS;
DROP TABLE travel_website;
DROP TABLE CUSTOMER;
DROP TABLE travel_packages;
DROP TABLE fp;
CREATE TABLE customer
(
c_name VARCHAR(20),
EMAIL VARCHAR(50),
c_pass  varchar(20),
dob varchar(20),
gender VARCHAR(10),
phonenumber INT,
PRIMARY KEY(EMAIL)
);

CREATE TABLE FP
(
EMAIL VARCHAR(50),
CODE VARCHAR(50)
);

CREATE TABLE travel_website
(
booking_id INT ,
start_date DATE,
return_date DATE,
travellers INT,
sourcee VARCHAR(20),
destination VARCHAR(20),
trip_expenses INT,
start_mode VARCHAR(20),
return_mode VARCHAR(20),
EMAIL VARCHAR(50),
FOREIGN KEY (EMAIL) REFERENCES customer(EMAIL)ON DELETE CASCADE,
PRIMARY KEY (booking_id)
);

CREATE TABLE C_BOOKINGS
(
booking_id INT,
H_NAME VARCHAR(20),
PLACE VARCHAR(20),
R_NO INT,
C_NO1 INT,
C_NO2 INT,
C_NO3 INT,
C_NO4 INT,
FOREIGN key (booking_id) REFERENCES travel_website ON DELETE CASCADE,
PRIMARY KEY (BOOKING_ID,H_NAME,R_NO)
);

CREATE TABLE travel_agency(
   start_vno INT ,
   return_vno INT,
   travelling_charges INT,
   booking_id INT,
FOREIGN KEY (booking_id) REFERENCES travel_website(booking_id)ON DELETE CASCADE,
 PRIMARY KEY (booking_id)
);
   



CREATE TABLE vehicledetails
(
vnod INT,
vno INT,
seat_capacity INT,
booked_seats INT,
seat_cost INT,
v_type varchar(6),
start_place varchar(20),
reach_place varchar(20),
s_date varchar(20),
PRIMARY KEY(vnod)
);
INSERT INTO vehicledetails VALUES(781820210519,7818,60,0,500,'bus','HYDERABAD','CHENNAI','19-may-2021');
INSERT INTO vehicledetails VALUES(781920210520,7819,60,0,500,'bus','HYDERABAD','CHENNAI','20-may-2021');
INSERT INTO vehicledetails VALUES(782820210521,7828,60,0,500,'bus','HYDERABAD','CHENNAI','21-may-2021');
INSERT INTO vehicledetails VALUES(781820210522,7818,60,0,500,'bus','HYDERABAD','CHENNAI','22-may-2021');
INSERT INTO vehicledetails VALUES(781920210523,7819,60,0,500,'bus','HYDERABAD','CHENNAI','23-may-2021');
INSERT INTO vehicledetails VALUES(782820210524,7828,60,0,500,'bus','HYDERABAD','CHENNAI','24-may-2021');
INSERT INTO vehicledetails VALUES(781920210525,7819,60,0,500,'bus','HYDERABAD','CHENNAI','25-may-2021');
INSERT INTO vehicledetails VALUES(783820210519,7838,500,0,300,'train','HYDERABAD','CHENNAI','19-may-2021');
INSERT INTO vehicledetails VALUES(784820210520,7848,500,0,300,'train','HYDERABAD','CHENNAI','20-may-2021');
INSERT INTO vehicledetails VALUES(785820210521,7858,500,0,300,'train','HYDERABAD','CHENNAI','21-may-2021');
INSERT INTO vehicledetails VALUES(783820210522,7838,500,0,300,'train','HYDERABAD','CHENNAI','22-may-2021');
INSERT INTO vehicledetails VALUES(784820210523,7848,500,0,300,'train','HYDERABAD','CHENNAI','23-may-2021');
INSERT INTO vehicledetails VALUES(785820210524,7858,500,0,300,'train','HYDERABAD','CHENNAI','24-may-2021');
INSERT INTO vehicledetails VALUES(784820210525,7848,500,0,300,'train','HYDERABAD','CHENNAI','25-may-2021');
INSERT INTO vehicledetails VALUES(791820210519,7918,100,0,5000,'flight','HYDERABAD','CHENNAI','19-may-2021');
INSERT INTO vehicledetails VALUES(731820210520,7318,100,0,5000,'flight','HYDERABAD','CHENNAI','20-may-2021');
INSERT INTO vehicledetails VALUES(971820210521,9718,100,0,5000,'flight','HYDERABAD','CHENNAI','21-may-2021');
INSERT INTO vehicledetails VALUES(791820210522,7918,100,0,5000,'flight','HYDERABAD','CHENNAI','22-may-2021');
INSERT INTO vehicledetails VALUES(731820210523,7318,100,0,5000,'flight','HYDERABAD','CHENNAI','23-may-2021');
INSERT INTO vehicledetails VALUES(971820210524,9718,100,0,5000,'flight','HYDERABAD','CHENNAI','24-may-2021');
INSERT INTO vehicledetails VALUES(731820210525,7318,100,0,5000,'flight','HYDERABAD','CHENNAI','25-may-2021');
INSERT INTO vehicledetails VALUES(781820210520,7818,60,0,500,'bus','CHENNAI','HYDERABAD','20-may-2021');
INSERT INTO vehicledetails VALUES(781920210521,7819,60,0,500,'bus','CHENNAI','HYDERABAD','21-may-2021');
INSERT INTO vehicledetails VALUES(782820210522,7828,60,0,500,'bus','CHENNAI','HYDERABAD','22-may-2021');
INSERT INTO vehicledetails VALUES(781820210523,7818,60,0,500,'bus','CHENNAI','HYDERABAD','23-may-2021');
INSERT INTO vehicledetails VALUES(781920210524,7819,60,0,500,'bus','CHENNAI','HYDERABAD','24-may-2021');
INSERT INTO vehicledetails VALUES(782820210525,7828,60,0,500,'bus','CHENNAI','HYDERABAD','25-may-2021');
INSERT INTO vehicledetails VALUES(781920210519,7819,60,0,500,'bus','CHENNAI','HYDERABAD','19-may-2021');
INSERT INTO vehicledetails VALUES(783820210520,7838,500,0,300,'train','CHENNAI','HYDERABAD','20-may-2021');
INSERT INTO vehicledetails VALUES(784820210521,7848,500,0,300,'train','CHENNAI','HYDERABAD','21-may-2021');
INSERT INTO vehicledetails VALUES(785820210522,7858,500,0,300,'train','CHENNAI','HYDERABAD','22-may-2021');
INSERT INTO vehicledetails VALUES(783820210523,7838,500,0,300,'train','CHENNAI','HYDERABAD','23-may-2021');
INSERT INTO vehicledetails VALUES(784820210524,7848,500,0,300,'train','CHENNAI','HYDERABAD','24-may-2021');
INSERT INTO vehicledetails VALUES(785820210525,7858,500,0,300,'train','CHENNAI','HYDERABAD','25-may-2021');
INSERT INTO vehicledetails VALUES(784820210519,7848,500,0,300,'train','CHENNAI','HYDERABAD','19-may-2021');
INSERT INTO vehicledetails VALUES(791820210520,7918,100,0,5000,'flight','CHENNAI','HYDERABAD','20-may-2021');
INSERT INTO vehicledetails VALUES(731820210521,7318,100,0,5000,'flight','CHENNAI','HYDERABAD','21-may-2021');
INSERT INTO vehicledetails VALUES(971820210522,9718,100,0,5000,'flight','CHENNAI','HYDERABAD','22-may-2021');
INSERT INTO vehicledetails VALUES(791820210523,7918,100,0,5000,'flight','CHENNAI','HYDERABAD','23-may-2021');
INSERT INTO vehicledetails VALUES(731820210524,7318,100,0,5000,'flight','CHENNAI','HYDERABAD','24-may-2021');
INSERT INTO vehicledetails VALUES(971820210525,9718,100,0,5000,'flight','CHENNAI','HYDERABAD','25-may-2021');
INSERT INTO vehicledetails VALUES(731820210519,7318,100,0,5000,'flight','CHENNAI','HYDERABAD','19-may-2021');


CREATE TABLE v_seats
(
vnod INT,
s_no INT,
s_status NUMBER(1),
FOREIGN KEY (vnod) REFERENCES VEHICLEDETAILS(vnod) ON DELETE CASCADE,
PRIMARY KEY(vnod,S_NO)
);


CREATE TABLE  hotel_site
(
stay_place VARCHAR(20),
no_of_travellers INT,
accomodation_charges INT,
booking_id INT,
bs_date date,
be_date date,
hotel_name varchar(20),
booked_rooms INT,
FOREIGN KEY (booking_id) REFERENCES travel_website(booking_id) ON DELETE CASCADE,
PRIMARY KEY (booking_id)
);


CREATE TABLE hoteldetails
(
 h_name VARCHAR(20),
 address VARCHAR(100),
 place varchar(20),
 rating DECIMAL(2,1),
 roomrent INT,
 no_of_rooms INT,
 PRIMARY KEY (h_name,place)
);

INSERT INTO hoteldetails VALUES ('rayal villas','a','CHENNAI',3.5,6000,60);
INSERT INTO hoteldetails VALUES ('taj banjara','B','CHENNAI',3.8,9000,80);
INSERT INTO hoteldetails VALUES ('snow valley','C','CHENNAI',4,10000,60);
INSERT INTO hoteldetails VALUES ('samson','D','HYDERABAD',5,40000,75);
INSERT INTO hoteldetails VALUES ('Radisson Plaza','E','HYDERABAD',4.9,5000,70);
INSERT INTO hoteldetails VALUES ('ITC Goa','F','HYDERABAD',5,8000,65);


CREATE TABLE hotelrooms
(
   h_name varchar(20),
   place varchar(20),
   room_no int,
   status INT,
   s_day INT,
   FOREIGN KEY(H_NAME,PLACE) REFERENCES HOTELDETAILS(H_NAME,PLACE) ON DELETE CASCADE,
   PRIMARY KEY(room_no,s_day,h_name,place)
);

CREATE TABLE tourist_places(
   spot_name VARCHAR2(100),
   spot_address VARCHAR2(100),
   specialty VARCHAR2(100),
   destination VARCHAR2(20),
   restaurent_name VARCHAR2(30),
   rating FLOAT,
   PRIMARY KEY (spot_name,spot_address)
   );
INSERT INTO tourist_places VALUES('Hawa Ghar','Ridge,Shimla','Elevated pavilion offering vistas','SHIMLA','apple',3 );
INSERT INTO tourist_places VALUES('Chadwick Falls','Shimla,Himachal Pradhesh','waterfall in a dense forest','SHIMLA','blue mango',4 );
INSERT INTO tourist_places VALUES('Scandal Point','Mall Rd,Shimla','Great views of the Himalayas','SHIMLA','green hard',4.2 );
INSERT INTO tourist_places VALUES('Khilanmarg','Gulmarg,Jammu and Kashmir','carpeted with flowers','KASHMIR','whale', 3.8);
INSERT INTO tourist_places VALUES('Thaj glacier','Forest Block,Jammu','scenic golf course','KASHMIR','andi',3.4 );
INSERT INTO tourist_places VALUES('Shiv Khori','near hayat,Jammu','Miracle of God','KASHMIR','boleraj',4.1 );
INSERT INTO tourist_places VALUES('Dolhins nose','Cannoor,Ooty','Catherine Waterfalls','OOTY','udipi',4.2 );
INSERT INTO tourist_places VALUES('Ooty Boat House','North Lake Road,ooty','boating','OOTY','thard',4.5 );
INSERT INTO tourist_places VALUES('Tiger Hill','Ooty, Tamil Nadu','panoramic view of Mount Everest','OOTY','nanged',4.1 );
INSERT INTO tourist_places VALUES('Humayan tomb','Mathura road,New Delhi','tomb of famous Mughal Emperor','DELHI','khauj',4);
INSERT INTO tourist_places VALUES('Bahai Temple','Bahapur,Kalkaji','Famous for architecture','DELHI','Barbeque',4.6);
INSERT INTO tourist_places VALUES('Gardenofsenses','South of Saket,New Delhi','Famous for Nature Beauty','DELHI','Mandi',4.8);
INSERT INTO tourist_places VALUES('Baga Beach','Saunto,Goa','famous for parasailing','GOA','Udipi restaurant',3.5);
INSERT INTO tourist_places VALUES('Calangu Beach','North Goa','Coastal road with dining,lodging','GOA','Feliz',3.5);
INSERT INTO tourist_places VALUES('Dudhsagar Falls','Sonalium,Goa','famoous for adventrous trek','GOA','Rio Salao',3.5);
INSERT INTO tourist_places VALUES('SolangValley','Burwa,Manali','snow-capped mountains','MANALI','Renaissance',3.5);
INSERT INTO tourist_places VALUES('Jogini Waterfalls','Vashist Village,Manali','Shakti peeth','MANALI','John Cafe',3.5);
INSERT INTO tourist_places VALUES('Manali Gompa','Old Manali Road','roof built in pagoda style','MANALI','Drift Inn',3.5);
INSERT INTO tourist_places VALUES('Aruku valley','aruku,Vizag','hill station','VIZAG','vashistha',3.9 );
INSERT INTO tourist_places VALUES('Rishikonda beach','Bheemili road,Vizag','beach with golden and black sand','VIZAG','Bake hotel',4.3);
INSERT INTO tourist_places VALUES('Tenneti Park','Beach Road,Vizag','childrens park','VIZAG','Treebo Trend','4.6');
INSERT INTO tourist_places VALUES('Nandi hills','Chikkaballapur,Banglore','ancient hill fortification','BENGALURU','Leela palace',4.1);
INSERT INTO tourist_places VALUES('Banglore palace','Vasanth Nagar,Banglore','stylish archutecture towers','BENGALURU','haveli',4.4);
INSERT INTO tourist_places VALUES('Thottikallu Falls','Kanakapura Rd,Banglore','golden faced water falls','BENGALURU','Rasisson',4.7);
INSERT INTO tourist_places VALUES('Chennai Lighthouse','Marina beach road,Myykapore','facing bay of bengal on east coast','CHENNAI','cafe hotel',4.5);
INSERT INTO tourist_places VALUES('Semmozhi Poonga','Cathedra Rd,Teynampet','botanical garden','CHENNAI','Grand Chola',4.0);
INSERT INTO tourist_places VALUES('Anna Nagar','Anna Nagar,Chennai','first and only township in chennai','CHENNAI','Hilton chennai',4.2);


create table travel_packages
(
 s_date DATE,
 e_date DATE,
 s_place VARCHAR(20),
 r_place VARCHAR(20),
 s_transport VARCHAR(6),
 r_transport VARCHAR(6),
 price INT,
 no_of_days INT
);

DELETE FROM TRAVEL_WEBSITE ;
DELETE FROM customer ;
select * from vehicledetails where start_place='HYDERABAD' and s_date='19-may-2021' and reach_place='CHENNAI' AND (seat_capacity-booked_seats)>0  AND V_TYPE='bus';

UPDATE vehicledetails SET s_date='25-jul-2021' WHERE S_DATE='19-may-2021';
UPDATE vehicledetails SET s_date='26-jul-2021' WHERE S_DATE='20-may-2021';
UPDATE vehicledetails SET s_date='27-jul-2021' WHERE S_DATE='21-may-2021';
UPDATE vehicledetails SET s_date='28-jul-2021' WHERE S_DATE='22-may-2021';
UPDATE vehicledetails SET s_date='29-jul-2021' WHERE S_DATE='23-may-2021';
UPDATE vehicledetails SET s_date='30-jul-2021' WHERE S_DATE='24-may-2021';
UPDATE vehicledetails SET s_date='31-jul-2021' WHERE S_DATE='25-may-2021';
UPDATE vehicledetails SET booked_seats=0;
SELECT
    *
FROM travel_packages;
SELECT *FROM vehicledetails;
SELECT * FROM hoteldetails ;
select * from customer;
SELECT * FROM travel_website;
select * from travel_agency;
SELECT * FROM hotel_site;
select * from hotelrooms;
select * from c_bookings;
select * from v_seats;
select * from fp;