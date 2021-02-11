INSERT INTO auth_user (username, email, password, admin)
VALUES
  ('Jone', 'jone@gmail.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', true),
  ('わたなべ', 'watanabe@outlook.co.jp', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', false),
  ('山田太郎', 'taro.yamada@yahoo.co.jp', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', false);

INSERT INTO book (isbn, title, author, publisher_name, sales_date, image_url, borrower_id, checkout_date)
VALUES
  ('1111111111111', 'title', 'author', 'publisher_name', 'sales_date', 'image_url', NULL, NULL),
  ('1234567890123', 'タイトル', '著者', '出版社', '出版日', 'URL', NULL, NULL),
  ('9784003271919', 'タタール人の砂漠', 'ディーノ・ブッツァーティ/脇功', '岩波書店', '2013年04月', 'https://xyz.image.co.jp', 1, '2021-01-31 06:24:23.642194');


