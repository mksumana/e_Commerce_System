CREATE DATABASE ecom2;
USE ecom2;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE,
    name VARCHAR(50),
    pno int UNIQUE,
    email VARCHAR(50) UNIQUE,
    address varchar(255),
    password VARCHAR(25),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

CREATE TRIGGER before_user_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF NEW.user_id IS NULL THEN
        SET NEW.user_id = CONCAT('USR', LPAD((SELECT COUNT(*) FROM users) + 1, 3, '0'));
    END IF;
END//

DELIMITER ;

select * from users;

CREATE TABLE product_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cat_id VARCHAR(100) UNIQUE, -- Matches type with product table
    cat_name VARCHAR(200) UNIQUE
);

 insert into product_category(cat_id,cat_name) values
 ('CAT001','electronics'),
 ('CAT002','fashion'),
 ('CAT003','footwear'),
 ('CAT004','grocery');
 
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    img_link varchar(200),
    category_id VARCHAR(100), 
    category_name VARCHAR(200),
    FOREIGN KEY (category_id) REFERENCES product_category(cat_id),
    FOREIGN KEY (category_name) REFERENCES product_category(cat_name)
);

select * from product;

DELIMITER //
CREATE TRIGGER before_product_insert
BEFORE INSERT ON product
FOR EACH ROW
BEGIN
    DECLARE max_id INT;
    SELECT IFNULL(MAX(id), 0) + 1 INTO max_id FROM product;
    SET NEW.product_id = CONCAT('PROD', LPAD(max_id, 6, '0'));
END//

DELIMITER ;

INSERT INTO product (name, price, img_link, category_id, category_name) VALUES 
('Product 1', 10.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\E1.png','CAT001','electronics'),
('Product 2', 20.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\E2.png','CAT001','electronics'),
('Product 3', 30.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\E3.png','CAT001','electronics'),
('Product 4', 40.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\E4.png','CAT001','electronics'),
('Product 5', 50.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\F1.png','CAT002','fashion'),
('Product 6', 60.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\F2.png','CAT002','fashion'),
('Product 7', 70.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\F3.png','CAT002','fashion'),
('Product 8', 90.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\F4.png','CAT002','fashion'),
('Product 9', 100.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\FW1.png','CAT003','footwear'),
('Product 10', 20.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\FW2.png','CAT003','footwear'),
('Product 11', 10.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\FW3.png','CAT003','footwear'),
('Product 12', 30.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\FW4.png','CAT003','footwear'),
('Product 13', 80.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\G1.png','CAT004','grocery'),
('Product 14', 20.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\G2.png','CAT004','grocery'),
('Product 15', 70.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\G3.png','CAT004','grocery'),
('Product 16', 200.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\G4.png','CAT004','grocery'),
('Product 17', 90.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\G5.png','CAT004','grocery'),
('Product 18', 30.00, 'C:\\Users\\MADHUMITHA V\\CSE\\SEM-5\\DBMS\\project_rough\\G6.png','CAT004','grocery');

TRUNCATE TABLE product;

select * from product;


CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id varchar(100),
    product_id varchar(100),
    quantity int,
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_table(
    order_no INT AUTO_INCREMENT PRIMARY KEY,
    user_id varchar(90),
    order_amount DECIMAL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_products (
    order_no INT,
    product_id varchar(90),
    quantity INT,
    PRIMARY KEY (order_no, product_id),
    FOREIGN KEY (order_no) REFERENCES order_table(order_no),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
select * from cart;

DELIMITER //
CREATE FUNCTION calculate_total(order_no INT)
RETURNS DECIMAL(10,2)
BEGIN
  RETURN (
    SELECT SUM(p.price * op.quantity)
    FROM products p
    JOIN order_products op ON p.product_id = op.product_id
    WHERE op.order_no = order_no
  )
END;
DELIMITER //

show tables;
/*
SELECT u.name AS user_name,p.name AS product_name,price AS product_price,c.quantity
FROM cart c
JOIN users u ON c.user_id = u.user_id
JOIN product p ON c.product_id = p.product_id
ORDER BY u.name, p.name;

SELECT 
    u.name AS user_name,
    SUM(p.price * c.quantity) AS total_cart_value
FROM cart c
JOIN users u ON c.user_id = u.user_id
JOIN product p ON c.product_id = p.product_id
GROUP BY u.user_id, u.name
ORDER BY total_cart_value DESC;

SELECT 
    p.category_name,
    COUNT(p.product_id) AS product_count
FROM product p
GROUP BY p.category_name
ORDER BY product_count DESC;

SELECT p.category_name,p.name AS product_name,p.price
FROM product p
WHERE p.price = (
        SELECT MAX(price)
        FROM product p2
        WHERE p2.category_name = p.category_name
    )
ORDER BY p.category_name;


DELIMITER $$*/


