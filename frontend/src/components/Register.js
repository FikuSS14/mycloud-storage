import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { register } from '../store/authSlice';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [form, setForm] = useState({
    login: '',
    full_name: '',
    email: '',
    password: '',
    password_confirm: ''
  });
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await dispatch(register(form)).unwrap();
      navigate('/login');  
    } catch (err) {
      console.error('Ошибка регистрации:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Регистрация</h2>
      <input name="login" placeholder="Логин" value={form.login} onChange={handleChange} required />
      <input name="full_name" placeholder="Полное имя" value={form.full_name} onChange={handleChange} required />
      <input name="email" placeholder="Email" type="email" value={form.email} onChange={handleChange} required />
      <input name="password" placeholder="Пароль" type="password" value={form.password} onChange={handleChange} required />
      <input name="password_confirm" placeholder="Подтверждение" type="password" value={form.password_confirm} onChange={handleChange} required />
      <button type="submit">Зарегистрироваться</button>
      <p>Уже есть аккаунт? <a href="/login">Вход</a></p>
    </form>
  );
}

export default Register;