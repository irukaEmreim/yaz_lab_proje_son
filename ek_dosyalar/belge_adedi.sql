CREATE TABLE application_activities (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    faaliyet_kodu VARCHAR(10),
    adet INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); -- Her bir başvuruya kaç belge yüklendiği bilgisi

select * from application_activities
DROP TABLE application_activities

DROP TABLE application_documents
DROP TABLE document_types
CREATE TABLE application_documents (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications(id),
    file_path TEXT,
    description TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


select * from application_documents
