USE mydb;

Select Usuarios.Login, count(User_ref.loginUsuario) from Usuarios
INNER JOIN User_ref ON Usuarios.Login = User_ref.loginUsuario
GROUP BY Usuarios.Cidade
