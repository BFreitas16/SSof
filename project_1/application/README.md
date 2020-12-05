# Fix Report of Group 32

## Phase 2 Deadline: 08Nov2020-23h59m

## Fixed vulnerabilities

- _Vulnerability 1: XSS when creating a post allows attacker to run javascript code on other user’s browsers_.
  - Root cause: The source of this vulnerability was the lack of input validation in the _create_post_ form.
  - Changes: Encoded the input fields (`new_content` and `type`) in function `create_post` in views.py

- _Vulnerability 2: XSS in editing a post allows attacker to run javascript code on other user’s browsers_.
  - Root cause: The source of this vulnerability was the lack of input validation in the _edit_post_ form.
  - Changes: Encoded the input fields (`new_content`, `new_type` and `post_id`) in function `edit_post` in views.py

- _Vulnerability 3: XSS in updating the profile’s name allows the attacker to run javascript code on other users’ browsers_.
  - Root cause: The source of this vulnerability was the lack of input validation in the _update_profile_ form.
  - Changes: Encoded the input fields (`new_name`, `new_about`, `new_photo_filename`, `current_password` and `new_password`) in function `update_profile` in views.py

- _Vulnerability 4: XSS in updating the profile’s about allows the attacker to run javascript code on other users’ browsers_.
  - Root cause: The source of this vulnerability was the lack of input validation in the _update_profile_ form.
  - Changes: Encoded the input fields (`new_name`, `new_about`, `new_photo_filename`, `current_password` and `new_password`) in function `update_profile` in views.py

- _Vulnerability 5: CSRF allows to create malicious posts_.
  - Root cause: The source of this vulnerability was the lack of user session validation.
  - Changes: Added flask_wtf.csrf package and used it for adding csrf.token hidden input to forms

- _Vulnerability 6: CSRF allows to send friend requests_.
  - Root cause: The source of this vulnerability was the lack of user session validation.
  - Changes: Added flask_wtf.csrf package and used it for adding csrf.token hidden input to forms

- _Vulnerability 7: SQL Injection in login form allows to login as admin_.
  - Root cause: The source of this vulnerability was the lack of input sanitization in the _login_ form.
  - Changes: Changed functions `login_user` and `get_all_results` to use prepared statements.

- _Vulnerability 8: SQL Injection search friend allows see all username-password or other table information (e.g. `Friends`, `FriendsRequests`, etc..).
  - Root cause: The source of this vulnerability was the lack of input sanitization in the _Search Friends_ form.
  - Changes: Changed functions `get_friends`, `get_friends_aux` and `get_all_results` to use prepared statements.

- _Vulnerability 9: XSS on profile picture allows attacker to run javascript code on other user’s browsers_.
  - Root cause: The source of this vulnerability was the lack of input validation in the _update_profile_ form.
  - Changes: Encoded the input fields (`new_name`, `new_about`, `new_photo_filename`, `current_password` and `new_password`) in function `update_profile` in views.py

- _Vulnerability 10: XSS in registry form allows attacker to run javascript code on other user’s browsers_.
  - Root cause: The source of this vulnerability was the lack of input validation in the _update_profile_ form.
  - Changes: Encoded the input fields (`username` and `password`) in function `register` in views.py

- _Vulnerability 11: SQL Injection search friend allows to drop any table present in database_.
  - Root cause: The source of this vulnerability was the lack of input sanitization in the _Search Friends_ form.
  - Changes: Changed functions `get_friends`, `get_friends_aux` and `get_all_results` to use prepared statements.

- _Vulnerability 12: SQL Injection add friend allows to drop any table present in database_.
  - Root cause: The source of this vulnerability was the lack of input sanitization in the _Add Friends_ form.
  - Changes: Changed functions `new_friend_request` and `get_all_results` to use prepared statements.

- _Vulnerability 13: SQL Injection creating a post allows to drop any table present in database_.
  - Root cause: The source of this vulnerability was the lack of input sanitization in the _New Post_ form.
  - Changes: Changed functions `new_post` and `get_all_results` to use prepared statements.

- _Vulnerability 14: SQL Injection editing a post allows to drop any table present in database_.
  - Root cause: The source of this vulnerability was the lack of input sanitization in the _Edit Post_ form.
  - Changes: Changed functions `edit_post` and `get_all_results` to use prepared statements.

- _Vulnerability 15: SQL Injection updating profile allows to drop any table present in database_.
  - Root cause: The source of this vulnerability was the lack of input sanitization in the _Edit Profile_ form.
  - Changes: Changed functions `update_user` and `get_all_results` to use prepared statements.

- _Vulnerability 16: Insecure cryptographic storage leads to a possible credentials’ leak and other important data (Present in Users table - password column)_.
  - Root cause: The source of this vulnerability was the lack of password hashing before inserting it into DB.
  - Changes: Added sha3 hashing and used it for hashing passwords in `register`, `login` and `update_profile` functions in views.py.

## Notes

- __Used the same numbering that was used for Phase 1.__
