import { Menu, Plus } from 'lucide-react'

interface TopBarProps {
  onMenu: () => void
  onNew: () => void
}

export const TopBar = ({ onMenu, onNew }: TopBarProps) => (
  <header className="topbar">
    <button className="icon-button topbar-menu" onClick={onMenu} aria-label="Open history" title="Open history"><Menu size={21} /></button>
    <div className="brand-lockup"><span className="brand-mark">TC</span><span>TrustCheck</span></div>
    <button className="new-button" onClick={onNew}><Plus size={16} /> <span>New</span></button>
  </header>
)
