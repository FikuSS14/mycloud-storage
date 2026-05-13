import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { uploadFile } from '../store/filesSlice';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [comment, setComment] = useState('');
  const dispatch = useDispatch();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      dispatch(uploadFile({ file, comment }));
      setFile(null);
      setComment('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Загрузить файл</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} required />
      <input placeholder="Комментарий" value={comment} onChange={(e) => setComment(e.target.value)} />
      <button type="submit">Загрузить</button>
    </form>
  );
}

export default FileUpload;