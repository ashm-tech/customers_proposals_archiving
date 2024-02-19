Default login: `admin`
Default password: `admin`
To generate new password, use command:
`htpasswd -nb admin 'newpassword' > ./project/usersfile.txt`
And then restart server for password change to take effect.

Команда запуска всего проекта:
`docker compose up -d --build`

