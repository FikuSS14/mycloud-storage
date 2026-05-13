import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import API from '../services/api';

export const fetchFiles = createAsyncThunk('files/fetch', async () => {
  const response = await API.get('/files/');
  return response.data;
});

export const uploadFile = createAsyncThunk('files/upload', async ({ file, comment }) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('comment', comment);
  const response = await API.post('/files/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
});

export const deleteFile = createAsyncThunk('files/delete', async (fileId) => {
  await API.delete(`/files/${fileId}/`);
  return fileId;
});

export const renameFile = createAsyncThunk('files/rename', async ({ fileId, newName }) => {
  const response = await API.patch(`/files/${fileId}/rename/`, { original_name: newName });
  return response.data;
});

export const updateComment = createAsyncThunk('files/comment', async ({ fileId, comment }) => {
  const response = await API.patch(`/files/${fileId}/comment/`, { comment });
  return response.data;
});

const filesSlice = createSlice({
  name: 'files',
  initialState: { items: [], loading: false },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchFiles.fulfilled, (state, action) => { state.items = action.payload; })
      .addCase(uploadFile.fulfilled, (state, action) => { state.items.push(action.payload); })
      .addCase(deleteFile.fulfilled, (state, action) => { 
        state.items = state.items.filter(f => f.id !== action.payload); 
      })
      .addCase(renameFile.fulfilled, (state, action) => {
        const index = state.items.findIndex(f => f.id === action.payload.id);
        if (index !== -1) state.items[index] = action.payload;
      })
      .addCase(updateComment.fulfilled, (state, action) => {
        const index = state.items.findIndex(f => f.id === action.payload.id);
        if (index !== -1) state.items[index] = action.payload;
      });
  },
});

export default filesSlice.reducer;