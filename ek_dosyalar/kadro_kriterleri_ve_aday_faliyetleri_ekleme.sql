CREATE TABLE bolumler (
    id SERIAL PRIMARY KEY,
    ad VARCHAR(100) NOT NULL UNIQUE
);

-- Bölümler tablosuna
INSERT INTO bolumler (ad) VALUES
('Sağlık/Fen/Ziraat/Matematik/Mühendislik/Ziraat/Orman ve Su Ürünleri'),
('Eğitim/Sosyal/Beşeri'),
('Hukuk/İlahiyat'),
('Güzel Sanatlar');

-- DROP TABLE kadro_kriterleri;
select * from kadro_kriterleri
select * from faaliyet_puanlari
select * from puan_kriterleri
select * from academic_announcements
select * from application_documents
select * from document_types
select * from applications
select * from bolumler
CREATE TABLE kadro_kriterleri (
    id SERIAL PRIMARY KEY,
    bolum_id INTEGER REFERENCES bolumler(id),
    unvan VARCHAR(20),               -- 'Dr. Öğr. Üyesi', 'Doçent', 'Profesör'
    faaliyet_kodu VARCHAR(20),
    asgari_adet INTEGER
);

-- DROP TABLE puan_kriterleri;

CREATE TABLE puan_kriterleri (
    id SERIAL PRIMARY KEY,
    bolum_id INTEGER REFERENCES bolumler(id),
    unvan VARCHAR(20),               -- örn: 'Dr. Öğr. Üyesi', 'Doçent/Profesör'
    faaliyet_kodu VARCHAR(10),
    asgari_puan INTEGER,
    azami_puan INTEGER
);



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
