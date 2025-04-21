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
