# Backend(Spring Boot API using JPA)
* Version
  * Spring Boot 2.2.7
  * java 1.8
  * MySql 8
## Database(Mysql) Schema
<pre>
<code>
create table News(
news_id int not null,
title varchar(2000) not null,
url varchar(2000) not null,
date timestamp not null,
constraint pk_news primary key(news_id)
);

create table GenderAnalysis(
gender_id int not null,
news_id int not null,
male double not null,
female double not null,
constraint pk_gender primary key(gender_id),
constraint fk_gender foreign key(news_id) references News(news_id)
);

create table AgeAnalysis(
age_id int not null,
news_id int not null,
10s double not null,
20s double not null,
30s double not null,
40s double not null,
50s double not null,
60sup double not null,
constraint pk_age primary key(age_id),
constraint fk_age foreign key(news_id) references News(news_id)
);

create table Comments(
comments_id int not null,
news_id int not null,
contents varchar(3000) not null,
writer varchar(20) not null,
recommended int not null,
unrecommended int not null,
date timestamp not null,
constraint pk_comments primary key(comments_id),
constraint fk_comments foreign key(news_id) references News(news_id)
);
</code>
</pre>


