import { useEffect, useState } from 'react';
import API from '../services/api';

function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get('/users/').then(res => {
      setUsers(res.data);
      setLoading(false);
    }).catch(err => {
      console.error('Доступ запрещён или ошибка', err);
      setLoading(false);
    });
  }, []);

  const handleDelete = (userId) => {
    if (window.confirm('Удалить пользователя?')) {
      API.delete(`/users/${userId}/`).then(() => {
        setUsers(users.filter(u => u.id !== userId));
      });
    }
  };

  const handleToggleAdmin = (userId, currentStatus) => {
    API.post(`/users/${userId}/promote/`).then(() => {
      setUsers(users.map(u => 
        u.id === userId ? { ...u, is_admin: !currentStatus } : u
      ));
    });
  };

  if (loading) return <div>Загрузка...</div>;

  return (
    <div>
      <h2>Управление пользователями (админ-панель)</h2>
      <table border="1">
        <thead>
          <tr><th>ID</th><th>Логин</th><th>Имя</th><th>Email</th><th>Админ</th><th>Действия</th></tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.login}</td>
              <td>{user.full_name}</td>
              <td>{user.email}</td>
              <td>{user.is_admin ? 'Да' : 'Нет'}</td>
              <td>
                <button onClick={() => handleToggleAdmin(user.id, user.is_admin)}>
                  {user.is_admin ? 'Снять админа' : 'Назначить админа'}
                </button>
                <button onClick={() => handleDelete(user.id)} disabled={user.login === 'admin'}>
                  Удалить
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminUsers;