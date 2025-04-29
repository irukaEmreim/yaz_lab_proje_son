select * from academic_announcements

select * from application_documents
DROP TABLE application_documents
ALTER TABLE application_documents ADD COLUMN faaliyet_kodu VARCHAR(10);

TRUNCATE TABLE application_activities CASCADE
TRUNCATE TABLE applications CASCADE
select * from users
select * from juries
select * from application_activities
select * from applications
select * from application_criteria
select * from academic_announcements
TRUNCATE TABLE academic_announcements CASCADE
TRUNCATE TABLE applications CASCADE
select * from jury_reports

select * from applications
select * from bolumler


select * from aday_faaliyetleri