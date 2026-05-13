import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import filesReducer from './filesSlice';

export const store = configureStore({
  reducer: { 
    auth: authReducer,
    files: filesReducer 
  },
});