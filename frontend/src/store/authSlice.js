import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import API from '../services/api';

// Логин: отправляем POST /login/
export const login = createAsyncThunk('auth/login', async (credentials) => {
  const response = await API.post('/login/', credentials);
  return response.data.user;  
});

// Регистрация: отправляем POST /register/
export const register = createAsyncThunk('auth/register', async (userData) => {
  const response = await API.post('/register/', userData);
  return response.data.user;
});

// Выход: отправляем POST /logout/
export const logout = createAsyncThunk('auth/logout', async () => {
  await API.post('/logout/');
  return null;
});

// Проверка текущего пользователя (для обновления страницы)
export const fetchMe = createAsyncThunk('auth/fetchMe', async () => {
  const response = await API.get('/me/');
  return response.data;
});

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null, loading: false, error: null },
  reducers: {
    // можно добавить очистку ошибок
    clearError: (state) => { state.error = null; },
  },
  extraReducers: (builder) => {
    builder
      // Логин
      .addCase(login.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(login.fulfilled, (state, action) => { state.loading = false; state.user = action.payload; })
      .addCase(login.rejected, (state, action) => { state.loading = false; state.error = action.error.message; })
      // Регистрация
      .addCase(register.pending, (state) => { state.loading = true; })
      .addCase(register.fulfilled, (state, action) => { state.loading = false; state.user = action.payload; })
      .addCase(register.rejected, (state, action) => { state.loading = false; state.error = action.error.message; })
      // Выход
      .addCase(logout.fulfilled, (state) => { state.user = null; })
      // Проверка me
      .addCase(fetchMe.fulfilled, (state, action) => { state.user = action.payload; });
  },
});

export const { clearError } = authSlice.actions;
export default authSlice.reducer;