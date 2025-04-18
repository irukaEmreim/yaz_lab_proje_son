-- Kullanıcılar Tablosu
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


-- Akademik İlanlar Tablosu
CREATE TABLE academic_announcements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    position_type VARCHAR(30) CHECK(position_type IN ('Dr. Öğr. Üyesi', 'Doçent', 'Profesör')) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Başvurular Tablosu
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    announcement_id INTEGER REFERENCES academic_announcements(id) ON DELETE CASCADE,
    candidate_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(15) CHECK(status IN ('Beklemede', 'Onaylandı', 'Reddedildi')) DEFAULT 'Beklemede',
    jury_evaluation_completed BOOLEAN DEFAULT FALSE,
    final_decision VARCHAR(20),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finalized_at TIMESTAMP
);

-- Başvuru Belgeleri Tablosu
CREATE TABLE application_documents (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id) ON DELETE CASCADE,
    document_type VARCHAR(50),
    file_path TEXT,
    file_url TEXT,
    description TEXT,
    metadata JSONB,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Başvuru Kriterleri
CREATE TABLE application_criteria (
    id SERIAL PRIMARY KEY,
    announcement_id INTEGER REFERENCES academic_announcements(id) ON DELETE CASCADE,
    criteria JSONB NOT NULL,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jüri Atamaları Tablosu
CREATE TABLE juries (
    id SERIAL PRIMARY KEY,
    announcement_id INTEGER REFERENCES academic_announcements(id) ON DELETE CASCADE,
    jury_member_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (announcement_id, jury_member_id)
);

-- Jüri Değerlendirme Raporları
CREATE TABLE jury_reports (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id) ON DELETE CASCADE,
    jury_member_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    evaluation_result VARCHAR(10) CHECK(evaluation_result IN ('olumlu', 'olumsuz')),
    explanation TEXT,
    report_file_path TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Akademik Faaliyetler (Tablo 5 puanlamaları için)
CREATE TABLE academic_activities (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id) ON DELETE CASCADE,
    activity_type VARCHAR(50),
    activity_name VARCHAR(255),
    activity_score DECIMAL(10,2),
    activity_metadata JSONB,
    activity_details TEXT
);

-- Bildirimler
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
