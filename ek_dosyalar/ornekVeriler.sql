-- 1) users tablosu (2 kayıt)
INSERT INTO users (tc_kimlik_no, first_name, last_name, email, password, role, is_active, is_staff, is_superuser) VALUES
  	('12345678901', 'Ahmet',   'Yılmaz',   'ahmet.yilmaz@admin.com',   'pbkdf2_sha256$...', 'admin',    TRUE,  FALSE, FALSE),
  	('23456789012', 'Mehmet',  'Kara',     'mehmet.kara@aday.com',    'pbkdf2_sha256$...', 'aday',     TRUE,  FALSE, FALSE);
	('34567890123', 'Ebru',    'Yıldız',   'ebru.yildiz@yonetici.com',   'pbkdf2_sha256$...', 'yonetici', TRUE,  FALSE, FALSE),
	('45678901234', 'Furkan',  'Akar',     'furkan.akar@juri.com',   'pbkdf2_sha256$...', 'juri',     TRUE,  FALSE, FALSE);


-- 2) academic_announcements tablosu (2 kayıt)
INSERT INTO academic_announcements (title, position_type, description, start_date, end_date, created_by) VALUES
  ('Bilgisayar Müh. Dr. Öğr. Üyesi İlanı', 'Dr. Öğr. Üyesi',
   'Bilgisayar mühendisliği kadrosu açılmıştır.', '2025-05-01', '2025-05-15', 1),
  ('Elektronik Müh. Doçentlik İlanı',      'Doçent',
   'Elektronik mühendisliği doçentlik başvuruları kabul edilecektir.', '2025-06-01', '2025-06-20', 1);

-- 3) applications tablosu (2 kayıt)
INSERT INTO applications (announcement_id, candidate_id, status, jury_evaluation_completed) VALUES
  (1, 2, 'Beklemede', FALSE),
  (2, 2, 'Onaylandı', TRUE);

-- 4) application_documents tablosu (2 kayıt)
INSERT INTO application_documents (application_id, document_type, file_path, file_url, description, metadata) VALUES
  (1, 'CV',      '/docs/cv1.pdf',      'http://example.com/docs/cv1.pdf',      'Curriculum Vitae',      '{"pages":2}'),
  (2, 'Diploma', '/docs/diploma2.pdf', 'http://example.com/docs/diploma2.pdf', 'Lisans Diploması',      '{"grade":"A"}');

-- 5) application_criteria tablosu (2 kayıt)
INSERT INTO application_criteria (announcement_id, criteria, created_by) VALUES
  (1, '{"min_publications":4, "min_score":120}',                   1),
  (2, '{"min_experience_years":3, "required_documents":["CV","Diploma"]}', 1);

-- 6) juries tablosu (2 kayıt)
INSERT INTO juries (announcement_id, jury_member_id) VALUES
  (1, 1),
  (2, 1);

-- 7) jury_reports tablosu (2 kayıt)
INSERT INTO jury_reports (application_id, jury_member_id, evaluation_result, explanation, report_file_path) VALUES
  (1, 1, 'olumlu',  'Aday belgelerini eksiksiz sunmuştur.',         '/reports/report1.pdf'),
  (2, 1, 'olumsuz', 'Akademik faaliyetler yetersiz bulunmuştur.', '/reports/report2.pdf');

-- 8) academic_activities tablosu (2 kayıt)
INSERT INTO academic_activities (application_id, activity_type, activity_name, activity_score, activity_metadata, activity_details) VALUES
  (1, 'publication', 'Blender Modelleme Çalışması', 15.50, '{"journal":"Journal of Engineering"}', 'Blender ile motor modeli yayınlandı.'),
  (2, 'conference',  'Ulusal ML Konferansı Sunumu',  8.00,  '{"location":"Ankara"}',             'Makine öğrenmesi bildirisi sundu.');

-- 9) notifications tablosu (2 kayıt)
INSERT INTO notifications (user_id, message) VALUES
  (2, 'Başvurunuz başarıyla alınmıştır.'),
  (1, 'Yeni bir başvuru yapılmıştır.');
