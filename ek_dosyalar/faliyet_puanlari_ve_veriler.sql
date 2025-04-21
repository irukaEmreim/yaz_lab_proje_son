CREATE TABLE faaliyet_puanlari (
    id SERIAL PRIMARY KEY,
    faaliyet_kodu VARCHAR(10) NOT NULL,      -- Örnek: A.1, A.2, B.1, F.1
    faaliyet_adi TEXT NOT NULL,              -- Örnek: "Q1 makale", "Yüksek lisans tez danışmanlığı"
    aciklama TEXT,                            -- Daha detaylı tanım
    puan INTEGER NOT NULL                    -- O faaliyet türü için varsayılan puan
);

