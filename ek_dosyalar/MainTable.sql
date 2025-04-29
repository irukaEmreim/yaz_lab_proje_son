
CREATE TABLE bolumler (
    id SERIAL PRIMARY KEY,
    ad VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO bolumler (ad) VALUES
('Sağlık/Fen/Ziraat/Matematik/Mühendislik/Ziraat/Orman ve Su Ürünleri'),
('Eğitim/Sosyal/Beşeri'),
('Hukuk/İlahiyat'),
('Güzel Sanatlar');

-- ===============================
-- 1. Kullanıcılar Tablosu
-- ===============================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tc_kimlik_no VARCHAR(11) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(10) CHECK(role IN ('aday', 'admin', 'yonetici', 'juri')) NOT NULL,
	is_active BOOLEAN DEFAULT TRUE,        -- Hesap aktif/pasif kontrolü
    is_staff BOOLEAN DEFAULT FALSE,        -- Django admin panel erişimi kontrolü
    is_superuser BOOLEAN DEFAULT FALSE,    -- Tam yetkili kullanıcı (superuser)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 2. Akademik İlanlar Tablosu
-- ===============================
CREATE TABLE academic_announcements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    position_type VARCHAR(30) CHECK(position_type IN ('Dr. Öğr. Üyesi', 'Doçent', 'Profesör')) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bolum_id INTEGER REFERENCES bolumler(id)
);

-- ===============================
-- 3. Başvurular Tablosu
-- ===============================
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    announcement_id INTEGER REFERENCES academic_announcements(id),
    candidate_id INTEGER REFERENCES users(id),
    status VARCHAR(15) CHECK(status IN ('Beklemede', 'Onaylandı', 'Reddedildi')) DEFAULT 'Beklemede',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ===============================
-- 5. Başvuru Belgeleri Tablosu
-- ===============================
CREATE TABLE application_documents ( ------ YENİDEN OLUŞACAK
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    file_path TEXT,
    description TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    faaliyet_kodu VARCHAR(10);
);

-- ===============================
-- 6. Başvuru Kriterleri Tablosu
-- ===============================
CREATE TABLE application_criteria (
    id SERIAL PRIMARY KEY,
    announcement_id INTEGER REFERENCES academic_announcements(id),
    criteria JSONB NOT NULL,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 7. Jüri Atamaları Tablosu
-- ===============================
CREATE TABLE juries (
    id SERIAL PRIMARY KEY,
    announcement_id INTEGER REFERENCES academic_announcements(id),
    jury_member_id INTEGER REFERENCES users(id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 8. Jüri Değerlendirme Raporları Tablosu
-- ===============================
CREATE TABLE jury_reports (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id) ON DELETE CASCADE,
    jury_member_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    evaluation_result VARCHAR(10) CHECK (evaluation_result IN ('olumlu', 'olumsuz')),
    report_file_path TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    jury_reports ADD COLUMN description Text
);


-- ===============================
-- 9. Akademik Faaliyetler Tablosu
-- ===============================
CREATE TABLE academic_activities (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    activity_type VARCHAR(50),
    activity_name VARCHAR(255),
    activity_score DECIMAL(10,2),
    activity_details TEXT
);

-- ===============================
-- 10. Bildirimler Tablosu
-- ===============================
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    message TEXT,
    notification_type VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE application_activities (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    faaliyet_kodu VARCHAR(10),
    adet INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); -- Her bir başvuruya kaç belge yüklendiği bilgisi

CREATE TABLE faaliyet_puanlari (
    id SERIAL PRIMARY KEY,
    faaliyet_kodu VARCHAR(10) NOT NULL,      -- Örnek: A.1, A.2, B.1, F.1
    faaliyet_adi TEXT NOT NULL,              -- Örnek: "Q1 makale", "Yüksek lisans tez danışmanlığı"
    aciklama TEXT,                            -- Daha detaylı tanım
    puan INTEGER NOT NULL                    -- O faaliyet türü için varsayılan puan
);

CREATE TABLE kadro_kriterleri (
    id SERIAL PRIMARY KEY,
    bolum_id INTEGER REFERENCES bolumler(id),
    unvan VARCHAR(20),               -- 'Dr. Öğr. Üyesi', 'Doçent', 'Profesör'
    faaliyet_kodu VARCHAR(20),
    asgari_adet INTEGER
);
-- A.1-A.2
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'A.1-A.2', 1),
       (1, 'Doçent', 'A.1-A.2', 3),
       (1, 'Profesör', 'A.1-A.2', 3);

-- A.1-A.4
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'A.1-A.4', 2),
       (1, 'Doçent', 'A.1-A.4', 4),
       (1, 'Profesör', 'A.1-A.4', 4);

-- A.1-A.5
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'A.1-A.5', 1),
		(1, 'Doçent', 'A.1-A.5', 0),
		(1, 'Profesör', 'A.1-A.5', 0);

-- A.1-A.6
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'A.1-A.6', 0),
		(1, 'Doçent', 'A.1-A.6', 0),
		(1, 'Profesör', 'A.1-A.6', 0);

-- A.1-A.8
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'A.1-A.8', 0),
		(1, 'Doçent', 'A.1-A.8', 0),
		(1, 'Profesör', 'A.1-A.8', 0);

-- Başlıca Yazar
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'Başlıca Yazar', 1),
       (1, 'Doçent', 'Başlıca Yazar', 2),
       (1, 'Profesör', 'Başlıca Yazar', 3);

-- Toplam Makale
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'Toplam Makale', 4),
       (1, 'Doçent', 'Toplam Makale', 7),
       (1, 'Profesör', 'Toplam Makale', 7);

-- Toplam Etkinlik
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'Etkinlik', 0),
       (1, 'Doçent', 'Etkinlik', 0),
       (1, 'Profesör', 'Etkinlik', 0);

-- F.1 veya F.2
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES 	(1, 'Dr. Öğr. Üyesi', 'F.1 veya F.2', 0),
		(1, 'Doçent', 'F.1 veya F.2', 1),
		(1, 'Profesör', 'F.1 veya F.2', 2);

-- H.1-12 veya H.13-17
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'H.1-12 veya H.13-17', 0),
       (1, 'Doçent', 'H.1-12 veya H.13-17', 1),
       (1, 'Profesör', 'H.1-12 veya H.13-17', 1);

-- H.1-12 veya H.13-22
INSERT INTO kadro_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_adet)
VALUES (1, 'Dr. Öğr. Üyesi', 'H.1-12 veya H.13-22', 0),
       (1, 'Doçent', 'H.1-12 veya H.13-22', 0),
       (1, 'Profesör', 'H.1-12 veya H.13-22', 0);

-- DROP TABLE puan_kriterleri;

CREATE TABLE puan_kriterleri (
    id SERIAL PRIMARY KEY,
    bolum_id INTEGER REFERENCES bolumler(id),
    unvan VARCHAR(20),               -- örn: 'Dr. Öğr. Üyesi', 'Doçent/Profesör'
    faaliyet_kodu VARCHAR(10),
    asgari_puan INTEGER,
    azami_puan INTEGER
);

-- A.1-A.4
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Dr. Öğr. Üyesi', 'A.1-A.4', 45, NULL),
       (1, 'Doçent/Profesör', 'A.1-A.4', 125, NULL);

-- A.1-A.5
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Dr. Öğr. Üyesi', 'A.1-A.5', 5, NULL);

-- A.1-A.6
-- Sadece Doçent/Profesör için var
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Doçent/Profesör', 'A.1-A.6', 40, 75);

-- A.1-A.8
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Doçent/Profesör', 'A.1-A.8', 50, 60);

-- D.1-D.6
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Dr. Öğr. Üyesi', 'D.1-D.6', NULL, 1500),
       (1, 'Doçent/Profesör', 'D.1-D.6', NULL, 1500);

-- E.1-E.4
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Dr. Öğr. Üyesi', 'E.1-E.4', 50, 50),
       (1, 'Doçent/Profesör', 'E.1-E.4', 50, 50);

-- F.1-F.2
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Dr. Öğr. Üyesi', 'F.1-F.2', NULL, 15),
       (1, 'Doçent/Profesör', 'F.1-F.2', NULL, 15);

-- H.1-H.17
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Doçent/Profesör', 'H.1-H.17', NULL, 20);

-- H.1-H.22
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Dr. Öğr. Üyesi', 'H.1-H.22', 10, 10),
       (1, 'Doçent/Profesör', 'H.1-H.22', 10, 10);

-- K.1-K.11
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Dr. Öğr. Üyesi', 'K.1-K.11', 50, 50),
       (1, 'Doçent/Profesör', 'K.1-K.11', 50, 50);

-- Toplam Puan
INSERT INTO puan_kriterleri (bolum_id, unvan, faaliyet_kodu, asgari_puan, azami_puan)
VALUES (1, 'Dr. Öğr. Üyesi', 'Toplam', 100, NULL),
       (1, 'Doçent/Profesör', 'Toplam', 250, NULL);



CREATE TABLE aday_faaliyetleri (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    ilan_id INTEGER NOT NULL REFERENCES academic_announcements(id),
    faaliyet_kodu VARCHAR(10) NOT NULL,
    aciklama TEXT,
    belge_linki TEXT, -- Belge AWS S3'e yüklendiğinde burada link olur
    puan INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO users (tc_kimlik_no, first_name, last_name, email, password, role, is_active, is_staff, is_superuser) VALUES
('12345678901', 'Ahmet', 'Yılmaz', 'ahmet.yilmaz@admin.com', 'ahmet123', 'admin',TRUE,FALSE,FALSE),
('10987654321', 'Ayşe', 'Kara', 'ayse.kara@aday.com', 'ayse123', 'aday',TRUE,FALSE,FALSE),
('11223344556', 'Mehmet', 'Can', 'mehmet.can@juri.com', 'mehmet123', 'juri',TRUE,FALSE,FALSE),
('22334455667', 'Fatma', 'Ak', 'fatma.ak@yonetici.com', 'fatma123', 'yonetici',TRUE,FALSE,FALSE);

INSERT INTO academic_announcements (title, position_type, description, start_date, end_date, created_by) VALUES
('Bilgisayar Mühendisliği Bölümü Dr. Öğr. Üyesi Alımı', 'Dr. Öğr. Üyesi', 'Bilgisayar Mühendisliği bölümüne Dr. Öğretim Üyesi alımı.', '2024-04-01', '2024-04-30', 1);

INSERT INTO applications (announcement_id, candidate_id) VALUES
(1, 2);

-- Belge türü olarak 'İndeksli Yayın' = ID: 1
INSERT INTO application_documents (application_id, file_path, description) VALUES
(1, '/uploads/yayin1.pdf', 'SCI-E dergisinde yayınlanmış makale.');

INSERT INTO application_criteria (announcement_id, criteria, created_by) VALUES
(1, '{"minimum_makale": 4, "minimum_puan": 75}', 4);

INSERT INTO juries (announcement_id, jury_member_id) VALUES
(1, 3);

INSERT INTO jury_reports (application_id, jury_member_id, evaluation_result, report_file_path) VALUES
(1, 3, 'olumlu', 87.5, '/uploads/report1.pdf');

INSERT INTO academic_activities (application_id, activity_type, activity_name, activity_score, activity_details) VALUES
(1, 'Makale', 'Bilgisayar Mühendisliğinde Yapay Zeka', 20.0, 'SCI-E dergisinde yayınlanmış bilimsel makale.');

INSERT INTO notifications (user_id, message, notification_type) VALUES
(2, 'Başvurunuz jüri değerlendirmesine gönderildi.', 'başvuru');



-- ÖRNEK VERİLER (KONTROL EDİLMELİ)

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
