/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2024/6/6 14:45:44                            */
/*==============================================================*/


drop table if exists charge_project;

drop table if exists publish_paper;

drop table if exists teach_course;

drop table if exists course;

drop table if exists paper;

drop table if exists project;

drop table if exists teacher;

/*==============================================================*/
/* Table: charge_project                                        */
/*==============================================================*/
create table charge_project
(
   job_number           char(5) not null,
   project_number       char(255) not null,
   ranking                 int,
   own_money            float,
   primary key (job_number, project_number)
);

/*==============================================================*/
/* Table: course                                                */
/*==============================================================*/
create table course
(
   course_number        char(255) not null,
   course_name          char(255),
   hours                int,
   course_nature        int,
   primary key (course_number)
);

/*==============================================================*/
/* Table: paper                                                 */
/*==============================================================*/
create table paper
(
   serial_number        int not null,
   paper_name           char(255),
   publish_source       char(255),
   publish_year         date,
   type                 int,
   level                int,
   primary key (serial_number)
);

/*==============================================================*/
/* Table: project                                               */
/*==============================================================*/
create table project
(
   project_number       char(255) not null,
   project_name         char(255),
   project_source       char(255),
   project_type         int,
   total_budget         float,
   start_year           date,
   end_year             date,
   primary key (project_number)
);

/*==============================================================*/
/* Table: publish_paper                                         */
/*==============================================================*/
create table publish_paper
(
   job_number           char(5) not null,
   serial_number        int not null,
   ranking                 int,
   corresponding_author bool,
   primary key (job_number, serial_number)
);

/*==============================================================*/
/* Table: teach_course                                          */
/*==============================================================*/
create table teach_course
(
   job_number           char(5) not null,
   course_number        char(255) not null,
   year                 int,
   term                 int,
   class_hour           int,
   primary key (job_number, course_number)
);

/*==============================================================*/
/* Table: teacher                                               */
/*==============================================================*/
create table teacher
(
   job_number           char(5) not null,
   name                 char(255),
   sex                  int,
   job_title            int,
   primary key (job_number)
);

alter table charge_project add constraint FK_charge_project foreign key (job_number)
      references teacher (job_number) on delete restrict on update restrict;

alter table charge_project add constraint FK_charge_project2 foreign key (project_number)
      references project (project_number) on delete restrict on update restrict;

alter table publish_paper add constraint FK_publish_paper foreign key (job_number)
      references teacher (job_number) on delete restrict on update restrict;

alter table publish_paper add constraint FK_publish_paper2 foreign key (serial_number)
      references paper (serial_number) on delete restrict on update restrict;

alter table teach_course add constraint FK_teach_course foreign key (job_number)
      references teacher (job_number) on delete restrict on update restrict;

alter table teach_course add constraint FK_teach_course2 foreign key (course_number)
      references course (course_number) on delete restrict on update restrict;

