import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../store/authSlice';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [loginInput, setLoginInput] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await dispatch(login({ login: loginInput, password })).unwrap();
      navigate('/files');  // после входа -> на страницу файлов
    } catch (err) {
      console.error('Ошибка входа:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Вход</h2>
      <div>
        <input
          type="text"
          placeholder="Логин"
          value={loginInput}
          onChange={(e) => setLoginInput(e.target.value)}
          required
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit">Войти</button>
      <p>Нет аккаунта? <a href="/register">Регистрация</a></p>
    </form>
  );
}

export default Login;