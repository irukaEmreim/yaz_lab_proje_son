ALTER TABLE academic_announcements
ADD COLUMN bolum_id INTEGER REFERENCES bolumler(id);
