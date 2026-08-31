import { ShieldCheck } from 'lucide-react'
import type { AnalyzeResponse, RiskLevel } from '../types'

interface ResultCardProps { response: AnalyzeResponse }

export const ResultCard = ({ response }: ResultCardProps) => {
  const level: RiskLevel = response.risk_level ?? 'UNKNOWN'
  const score = typeof response.risk_score === 'number' ? response.risk_score : null
  const label = level === 'UNKNOWN' ? 'Could not be verified' : `${level[0]}${level.slice(1).toLowerCase()} risk`
  return <article className="result-card">
    <div className="result-topline"><div className={`risk-badge risk-${level.toLowerCase()}`}><span className="risk-dot" />{label}</div><span className="result-caption">TrustCheck analysis</span></div>
    <div className="score-row"><div><span className="score-label">Risk score</span><strong>{score === null ? '—' : score}<small>/100</small></strong></div><div className={`score-meter meter-${level.toLowerCase()}`}><span style={{ width: `${score ?? 0}%` }} /></div></div>
    {!!response.urls?.length && <section className="detail-section"><h3>Links found</h3>{response.urls.map((url) => <p className="detail-value" key={url}>{url}</p>)}</section>}
    {!!response.brands?.length && <section className="detail-section"><h3>Brands mentioned</h3><div className="chip-row">{response.brands.map((brand) => <span className="chip" key={brand}>{brand}</span>)}</div></section>}
    {!!response.signals?.length && <section className="detail-section"><h3>Signals</h3><ul className="signal-list">{response.signals.map((signal) => <li key={signal}>{signal}</li>)}</ul></section>}
    {!!response.explanation?.length && <section className="detail-section"><h3>What we noticed</h3><ul className="explanation-list">{response.explanation.map((item) => <li key={item}>{item}</li>)}</ul></section>}
    <div className="safe-action"><ShieldCheck size={20} /><div><h3>Safer next step</h3><p>{response.safe_action || 'Pause before interacting and verify the sender through a trusted channel.'}</p></div></div>
  </article>
}
