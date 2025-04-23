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

DELETE FROM kadro_kriterleri

