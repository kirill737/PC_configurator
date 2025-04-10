-- INSERT INTO users (name, email, password_hash, role) VALUES
-- ('test', 'test1@yandex.ru', 'test_hash'::BYTEA, 'user');

-- SELECT * FROM users;
 
-- SELECT * FROM build_components;
-- SELECT * FROM components;

-- SELECT bc.component_id, c.type 
-- FROM build_components as bc
-- LEFT JOIN components as c ON c.id = bc.component_id
-- WHERE bc.build_id = 4 ;

-- SELECT c.id 
-- FROM components as c
-- LEFT JOIN cpus ON c.id = cpus.component_id
-- WHERE bc.build_id = 4 ;

-- SELECT * FROM components;
-- TRUNCATE TABLE builds;
-- DELETE FROM builds WHERE id = 1;
-- SELECT * FROM builds;


-- SELECT * FROM components
-- WHERE id in (1, 2);
SELECT c.id AS component_id
FROM build_components bc
JOIN components c ON bc.component_id = c.id
WHERE bc.build_id = 1 AND c.type = 'cpu';
