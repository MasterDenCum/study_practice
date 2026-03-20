import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <Router>
      <div className="navbar">
        <div>
          <span style={{ fontSize: '24px', fontWeight: 'bold', color: 'white', marginRight: '40px' }}>NEXUS PLAY</span>
          <Link to="/">Магазин</Link>
          {token && <Link to="/library">Библиотека</Link>}
        </div>
        <div>
          {!token ? (
            <>
              <Link to="/login">Войти</Link>
              <Link to="/register">Регистрация</Link>
            </>
          ) : (
            <button className="btn btn-logout" onClick={logout}>Выйти</button>
          )}
        </div>
      </div>

      <div className="container">
        <Routes>
          <Route path="/" element={<Store token={token} />} />
          <Route path="/library" element={<Library token={token} />} />
          <Route path="/login" element={<Login setToken={setToken} />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

// Компонент Магазина
function Store({ token }) {
  const [games, setGames] = useState([]);

  useEffect(() => {
    axios.get(`${API_URL}/games`).then(res => setGames(res.data));
  }, []);

  const buyGame = async (id) => {
    if (!token) return alert('Сначала авторизуйтесь!');
    try {
      await axios.post(`${API_URL}/buy/${id}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Игра успешно добавлена в библиотеку!');
    } catch (e) {
      alert(e.response?.data?.detail || 'Ошибка покупки');
    }
  };

  return (
    <div>
      <h2>Популярное и рекомендуемое</h2>
      {games.map(g => (
        <div key={g.id} className="card">
          <div>
            <h3 style={{margin: '0 0 10px 0', color: '#fff'}}>{g.title}</h3>
            <p style={{margin: 0, fontSize: '14px'}}>{g.description}</p>
          </div>
          <div style={{textAlign: 'right'}}>
            <p style={{marginTop: 0}}>{g.price} ₽</p>
            <button className="btn" onClick={() => buyGame(g.id)}>В корзину</button>
          </div>
        </div>
      ))}
    </div>
  );
}

// Компонент Библиотеки (Решение проблемы: отсутствие доступа к играм)
function Library({ token }) {
  const [myGames, setMyGames] = useState([]);

  useEffect(() => {
    if (token) {
      axios.get(`${API_URL}/library`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => setMyGames(res.data));
    }
  }, [token]);

  if (!token) return <h2>Пожалуйста, войдите в систему</h2>;

  return (
    <div>
      <h2>Моя Библиотека</h2>
      {myGames.length === 0 ? <p>Ваша библиотека пуста.</p> : null}
      {myGames.map(g => (
        <div key={g.id} className="card" style={{backgroundImage: 'linear-gradient(to right, #1b2838, #2a475e)'}}>
          <h3 style={{margin: 0, color: '#fff'}}>{g.title}</h3>
          <button className="btn" style={{background: '#0078d7', color: 'white'}}>Скачать / Играть</button>
        </div>
      ))}
    </div>
  );
}

// Компонент Авторизации
function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    try {
      const res = await axios.post(`${API_URL}/login`, formData);
      localStorage.setItem('token', res.data.access_token);
      setToken(res.data.access_token);
      navigate('/');
    } catch (e) {
      alert('Ошибка авторизации');
    }
  };

  return (
    <div>
      <h2>Вход в систему</h2>
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label>Логин</label>
          <input value={username} onChange={e => setUsername(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Пароль</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
        </div>
        <button className="btn" type="submit">Войти</button>
      </form>
    </div>
  );
}

// Компонент Регистрации
function Register() {
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const navigate = useNavigate();

  const handleReg = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/register`, form);
      alert('Успешно! Теперь войдите.');
      navigate('/login');
    } catch (e) {
      alert('Ошибка: пользователь существует');
    }
  };

  return (
    <div>
      <h2>Создание аккаунта</h2>
      <form onSubmit={handleReg}>
        <div className="form-group">
          <label>Логин</label>
          <input onChange={e => setForm({...form, username: e.target.value})} required />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input type="email" onChange={e => setForm({...form, email: e.target.value})} required />
        </div>
        <div className="form-group">
          <label>Пароль</label>
          <input type="password" onChange={e => setForm({...form, password: e.target.value})} required />
        </div>
        <button className="btn" type="submit">Зарегистрироваться</button>
      </form>
    </div>
  );
}

export default App;
