import { Routes, Route, Link, useLocation, Navigate } from 'react-router-dom'
import { useAuth } from './auth/AuthContext'
import BeansPage from './pages/BeansPage'
import ShopsPage from './pages/ShopsPage'
import JournalPage from './pages/JournalPage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'

function BrandMark() {
  return (
    <svg className="brand-mark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M12 3C8 8 6 11 6 14.5C6 18.09 8.69 21 12 21C15.31 21 18 18.09 18 14.5C18 11 16 8 12 3Z"
        stroke="var(--color-crema)"
        strokeWidth="1.6"
      />
      <path d="M12 6.5C12 10 12 15 12 20.5" stroke="var(--color-crema)" strokeWidth="1.6" />
    </svg>
  )
}

function Nav() {
  const { token, logout } = useAuth()
  const location = useLocation()
  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="nav">
      <Link to="/" className="brand">
        <BrandMark />
        Coffeans
      </Link>
      <div className="nav-links">
        <Link to="/beans" className={isActive('/beans') ? 'active' : ''}>
          Beans
        </Link>
        <Link to="/shops" className={isActive('/shops') ? 'active' : ''}>
          Shops &amp; roasteries
        </Link>
        {token && (
          <Link to="/journal" className={isActive('/journal') ? 'active' : ''}>
            My journal
          </Link>
        )}
        {token ? (
          <button className="btn btn-secondary" onClick={logout}>
            Log out
          </button>
        ) : (
          <Link to="/login" className="btn btn-secondary">
            Log in
          </Link>
        )}
      </div>
    </nav>
  )
}

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <div className="app-shell">
      <Nav />
      <Routes>
        <Route path="/" element={<Navigate to="/beans" replace />} />
        <Route path="/beans" element={<BeansPage />} />
        <Route path="/shops" element={<ShopsPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route
          path="/journal"
          element={
            <ProtectedRoute>
              <JournalPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  )
}
