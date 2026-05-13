import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from './store/authSlice';
import Login from './components/Login';
import Register from './components/Register';
import FileList from './components/FileList';
import FileUpload from './components/FileUpload';
import AdminUsers from './components/AdminUsers';

function App() {
  const user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(logout());
  };

  if (!user) {
    return (
      <BrowserRouter>
        <div>
          <h1>My Cloud Storage</h1>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        </div>
      </BrowserRouter>
    );
  }

  return (
    <BrowserRouter>
      <div>
        <h1>My Cloud Storage</h1>
        <p>Привет, {user.full_name} ({user.is_admin ? 'Админ' : 'Пользователь'})</p>
        <nav>
          <Link to="/files">Мои файлы</Link> | 
          <Link to="/upload">Загрузить</Link> |
          {user.is_admin && <span> <Link to="/admin">Админ-панель</Link> | </span>}
          <button onClick={handleLogout}>Выйти</button>
        </nav>

        <Routes>
          <Route path="/files" element={<FileList />} />
          <Route path="/upload" element={<FileUpload />} />
          {user.is_admin && <Route path="/admin" element={<AdminUsers />} />}
          <Route path="*" element={<Navigate to="/files" />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;