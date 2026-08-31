import { X } from 'lucide-react'
import type { Exchange } from '../types'

interface SidebarProps {
  exchanges: Exchange[]
  activeId?: string
  open: boolean
  onClose: () => void
  onSelect: (exchange: Exchange) => void
}

export const Sidebar = ({ exchanges, activeId, open, onClose, onSelect }: SidebarProps) => (
  <>
    <div className={`drawer-backdrop ${open ? 'is-open' : ''}`} onClick={onClose} />
    <aside className={`sidebar ${open ? 'is-open' : ''}`} aria-label="Analysis history">
      <div className="sidebar-heading"><div><p className="eyebrow">Your workspace</p><h2>History</h2></div><button className="icon-button drawer-close" onClick={onClose} aria-label="Close history"><X size={19} /></button></div>
      <div className="history-list">
        {exchanges.length === 0 && <p className="empty-history">Your analyzed messages will appear here.</p>}
        {exchanges.map((exchange) => {
          const level = exchange.response?.risk_level ?? 'UNKNOWN'
          return <button key={exchange.id} className={`history-item ${activeId === exchange.id ? 'active' : ''}`} onClick={() => onSelect(exchange)}>
            <span className="history-message">{exchange.message}</span><span className={`risk-tag risk-${level.toLowerCase()}`}>{level}</span>
          </button>
        })}
      </div>
      <div className="sidebar-footer">Private by design <span>•</span> Mock mode</div>
    </aside>
  </>
)
