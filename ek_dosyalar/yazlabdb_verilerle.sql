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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
-- 4. Belge Türleri Tablosu
-- ===============================
CREATE TABLE document_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- ===============================
-- 5. Başvuru Belgeleri Tablosu
-- ===============================
CREATE TABLE application_documents (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    document_type_id INTEGER REFERENCES document_types(id),
    file_path TEXT,
    description TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    application_id INTEGER REFERENCES applications(id),
    jury_member_id INTEGER REFERENCES users(id),
    evaluation_result VARCHAR(10) CHECK(evaluation_result IN ('olumlu', 'olumsuz')),
    score DECIMAL(5,2),
    report_file_path TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

INSERT INTO document_types (name) VALUES
('İndeksli Yayın'),
('Diploma'),
('Yabancı Dil Belgesi'),
('Öğretim Belgesi');

INSERT INTO users (tc_kimlik_no, first_name, last_name, email, password, role) VALUES
('12345678901', 'Ahmet', 'Yılmaz', 'ahmet.yilmaz@example.com', 'hashedpassword1', 'admin'),
('10987654321', 'Ayşe', 'Kara', 'ayse.kara@example.com', 'hashedpassword2', 'aday'),
('11223344556', 'Mehmet', 'Can', 'mehmet.can@example.com', 'hashedpassword3', 'juri'),
('22334455667', 'Fatma', 'Ak', 'fatma.ak@example.com', 'hashedpassword4', 'yonetici');

INSERT INTO academic_announcements (title, position_type, description, start_date, end_date, created_by) VALUES
('Bilgisayar Mühendisliği Bölümü Dr. Öğr. Üyesi Alımı', 'Dr. Öğr. Üyesi', 'Bilgisayar Mühendisliği bölümüne Dr. Öğretim Üyesi alımı.', '2024-04-01', '2024-04-30', 1);

INSERT INTO applications (announcement_id, candidate_id) VALUES
(1, 2);

-- Belge türü olarak 'İndeksli Yayın' = ID: 1
INSERT INTO application_documents (application_id, document_type_id, file_path, description) VALUES
(1, 1, '/uploads/yayin1.pdf', 'SCI-E dergisinde yayınlanmış makale.');

INSERT INTO application_criteria (announcement_id, criteria, created_by) VALUES
(1, '{"minimum_makale": 4, "minimum_puan": 75}', 4);

INSERT INTO juries (announcement_id, jury_member_id) VALUES
(1, 3);

INSERT INTO jury_reports (application_id, jury_member_id, evaluation_result, score, report_file_path) VALUES
(1, 3, 'olumlu', 87.5, '/uploads/report1.pdf');

INSERT INTO academic_activities (application_id, activity_type, activity_name, activity_score, activity_details) VALUES
(1, 'Makale', 'Bilgisayar Mühendisliğinde Yapay Zeka', 20.0, 'SCI-E dergisinde yayınlanmış bilimsel makale.');

INSERT INTO notifications (user_id, message, notification_type) VALUES
(2, 'Başvurunuz jüri değerlendirmesine gönderildi.', 'başvuru');