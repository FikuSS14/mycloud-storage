import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
});

// Функция получения CSRF-токена из куки
const getCSRFToken = () => {
  const name = 'csrftoken';  
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return value;
  }
  return null;
};

// Перехватчик — добавляем CSRF-токен в заголовок
API.interceptors.request.use(config => {
  const token = getCSRFToken();
  if (token) {
    config.headers['X-CSRFToken'] = token;  
    console.log('CSRF-токен добавлен в заголовок:', token);
  }
  console.log('Отправка:', config.method, config.url);
  return config;
});

export default API;