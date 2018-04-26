SET FOREIGN_KEY_CHECKS = 0; 
TRUNCATE table polls_choice;
TRUNCATE table polls_question;
TRUNCATE table polls_information;
SET FOREIGN_KEY_CHECKS = 1;

TRUNCATE TABLE posts_attachment;
DELETE FROM auth_user WHERE id != 1;
TRUNCATE TABLE posts_tag;
TRUNCATE TABLE posts_post;
TRUNCATE TABLE posts_posttag;

