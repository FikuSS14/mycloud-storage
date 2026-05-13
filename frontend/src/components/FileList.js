import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchFiles, deleteFile, renameFile, updateComment } from '../store/filesSlice';
import API from '../services/api';

function FileList() {
  const dispatch = useDispatch();
  const files = useSelector((state) => state.files.items);
  const [editingId, setEditingId] = useState(null);
  const [newName, setNewName] = useState('');
  const [editingCommentId, setEditingCommentId] = useState(null);
  const [newComment, setNewComment] = useState('');

  useEffect(() => {
    dispatch(fetchFiles());
  }, [dispatch]);

  const handleDownload = async (fileId, originalName) => {
    const response = await API.get(`/files/${fileId}/download/`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', originalName);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const handleCopyLink = (specialLink) => {
    const link = `http://127.0.0.1:8000/api/download/${specialLink}/`;
    navigator.clipboard.writeText(link);
    alert('Ссылка скопирована!');
  };

  const handleRename = (fileId, currentName) => {
    if (newName && newName !== currentName) {
      dispatch(renameFile({ fileId, newName }));
    }
    setEditingId(null);
    setNewName('');
  };

  const handleUpdateComment = (fileId, currentComment) => {
    if (newComment !== currentComment) {
      dispatch(updateComment({ fileId, comment: newComment }));
    }
    setEditingCommentId(null);
    setNewComment('');
  };

  return (
    <div>
      <h2>Мои файлы</h2>
      {files.length === 0 && <p>Нет файлов. Загрузите первый!</p>}
      <ul>
        {files.map((file) => (
          <li key={file.id} style={{ marginBottom: '20px', border: '1px solid #ccc', padding: '10px' }}>
            <div>
              <strong>
                {editingId === file.id ? (
                  <input
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    onBlur={() => handleRename(file.id, file.original_name)}
                    onKeyPress={(e) => e.key === 'Enter' && handleRename(file.id, file.original_name)}
                    autoFocus
                  />
                ) : (
                  <span onDoubleClick={() => { setEditingId(file.id); setNewName(file.original_name); }}>
                    {file.original_name}
                  </span>
                )}
              </strong>
              {' '}
              ({file.size} байт)
            </div>
            <div>
              Комментарий: 
              {editingCommentId === file.id ? (
                <input
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  onBlur={() => handleUpdateComment(file.id, file.comment)}
                  onKeyPress={(e) => e.key === 'Enter' && handleUpdateComment(file.id, file.comment)}
                  autoFocus
                />
              ) : (
                <span onDoubleClick={() => { setEditingCommentId(file.id); setNewComment(file.comment || ''); }}>
                  {file.comment || 'Нет комментария'}
                </span>
              )}
            </div>
            <div>
              <button onClick={() => handleDownload(file.id, file.original_name)}>Скачать</button>
              <button onClick={() => handleCopyLink(file.special_link)}>Скопировать ссылку</button>
              <button onClick={() => dispatch(deleteFile(file.id))}>Удалить</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FileList;