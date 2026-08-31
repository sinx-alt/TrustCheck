import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { Shield, Sparkles } from 'lucide-react'
import { ChatBubble } from './components/ChatBubble'
import { ErrorBubble } from './components/ErrorBubble'
import { InputBar } from './components/InputBar'
import { LoadingBubble } from './components/LoadingBubble'
import { ResultCard } from './components/ResultCard'
import { Sidebar } from './components/Sidebar'
import { TopBar } from './components/TopBar'
import { useAnalyze } from './hooks/useAnalyze'
import type { Exchange } from './types'

const HISTORY_KEY = 'trustcheck-history'
const welcomeMessages = ["Paste a suspicious message, link, or offer below. TrustCheck breaks down the signals so you can decide with confidence.", "Scam messages are built to rush you. TrustCheck slows things down — showing exactly what looks off, and why.", "Paste anything that feels a little too urgent, too good, or too unfamiliar. We'll walk through the evidence with you.", "Not sure if it's real? Paste it below and let's look at the evidence together.", "TrustCheck reads the message the way a careful friend would — checking for pressure, mismatched links, and claims that don't add up.", "One paste is all it takes. We'll extract the links, check the claims, and explain the risk in plain language.", "From urgent bank alerts to too-good-to-be-true offers — paste it here and see what's really going on.", "Suspicious text? Sketchy link? Drop it below and we'll show you exactly what raised the flag.", "TrustCheck won't just tell you 'this looks fake.' It'll show you the evidence behind the verdict.", "Before you click, pay, or share — let TrustCheck take a closer look and explain what it finds."]
const composerHints = [
  'TrustCheck offers guidance, not certainty. Always verify important requests independently.',
  "TrustCheck helps you spot risk - it doesn't replace independent verification.",
  'This is a second opinion, not a final verdict. Always verify through official channels.',
  'Guidance, not certainty. When it matters, verify independently.',
  "No tool catches everything. Always double-check important requests.",
  "Think of this as a second pair of eyes - not the final word. Always verify important requests independently.",
  'We help you pause and check. The final call - and any important verification - is always yours.',
]
const welcomeHeadlines = [
  'Pause. Check. Proceed with clarity.',
  "Don't just detect scams - explain them.",
  'See the evidence, not just the verdict.',
  'Know why it is risky - not just that it is.',
  'Clarity before you click.',
  'Every warning, backed by evidence.',
  "Think twice. We'll show you why.",
  'Before you click, check the evidence.',
  'Not a guess. A breakdown.',
  'Read between the red flags.',
]

const chooseRandom = (options: string[]) => options[Math.floor(Math.random() * options.length)]
const randomInterval = () => 7000 + Math.random() * 8000

const useRotatingMessage = (options: string[]) => {
  const [message, setMessage] = useState(() => chooseRandom(options))
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    let changeTimer: ReturnType<typeof setTimeout>
    let showTimer: ReturnType<typeof setTimeout>

    const scheduleChange = () => {
      changeTimer = setTimeout(() => {
        setIsVisible(false)
        showTimer = setTimeout(() => {
          setMessage(chooseRandom(options))
          setIsVisible(true)
          scheduleChange()
        }, 350)
      }, randomInterval())
    }

    scheduleChange()
    return () => { clearTimeout(changeTimer); clearTimeout(showTimer) }
  }, [options])

  return { message, isVisible }
}

const loadHistory = (): Exchange[] => {
  try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]') as Exchange[] } catch { return [] }
}

function App() {
  const [exchanges, setExchanges] = useState<Exchange[]>(loadHistory)
  const [activeId, setActiveId] = useState<string | undefined>(() => loadHistory()[0]?.id)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const { analyze, isLoading } = useAnalyze()
  const [errorId, setErrorId] = useState<string>()
  const [hasChatStarted, setHasChatStarted] = useState(false)
  const [isComposerSettling, setIsComposerSettling] = useState(false)
  const welcomeMessage = useRotatingMessage(welcomeMessages)
  const composerHint = useRotatingMessage(composerHints)
  const welcomeHeadline = useRotatingMessage(welcomeHeadlines)
  const threadEnd = useRef<HTMLDivElement>(null)
  const composer = useRef<HTMLDivElement>(null)
  const composerStart = useRef<DOMRect | null>(null)

  useEffect(() => { localStorage.setItem(HISTORY_KEY, JSON.stringify(exchanges)) }, [exchanges])
  useEffect(() => { threadEnd.current?.scrollIntoView({ behavior: 'smooth' }) }, [exchanges, isLoading])
  useLayoutEffect(() => {
    if (!hasChatStarted || !composerStart.current || !composer.current) return
    const element = composer.current
    const end = element.getBoundingClientRect()
    element.style.setProperty('--composer-start-x', `${composerStart.current.left - end.left}px`)
    element.style.setProperty('--composer-start-y', `${composerStart.current.top - end.top}px`)
    composerStart.current = null
    setIsComposerSettling(true)
  }, [hasChatStarted])

  const submit = async (message: string) => {
    const id = `${Date.now()}`
    composerStart.current = composer.current?.getBoundingClientRect() || null
    setHasChatStarted(true)
    setActiveId(id); setErrorId(undefined)
    setExchanges((current) => [...current, { id, message, createdAt: Date.now() }])
    try {
      const response = await analyze(message)
      setExchanges((current) => current.map((item) => item.id === id ? { ...item, response } : item))
    } catch { setErrorId(id) }
  }

  const retry = () => {
    const exchange = exchanges.find((item) => item.id === errorId)
    if (exchange) submit(exchange.message)
  }

  const newChat = () => { setActiveId(undefined); setErrorId(undefined); setHasChatStarted(false); setIsComposerSettling(false); setDrawerOpen(false) }
  const selectExchange = (exchange: Exchange) => { setActiveId(exchange.id); setDrawerOpen(false) }
  const activeExchange = exchanges.find((item) => item.id === activeId)

  return <div className="app-shell">
    <TopBar onMenu={() => setDrawerOpen(true)} onNew={newChat} />
    <div className="workspace">
      <Sidebar exchanges={exchanges} activeId={activeId} open={drawerOpen} onClose={() => setDrawerOpen(false)} onSelect={selectExchange} />
      <main className={`main-panel${!activeExchange ? ' is-empty' : ''}`}>
        <div className="thread">
          {!activeExchange && <div className="welcome"><div className="welcome-icon"><Shield size={26} /></div><p className="eyebrow">A second opinion for the internet</p><h1 className={`rotating-copy ${welcomeHeadline.isVisible ? 'is-visible' : 'is-hidden'}`}>{welcomeHeadline.message}</h1><p className={`welcome-copy rotating-copy ${welcomeMessage.isVisible ? 'is-visible' : 'is-hidden'}`}>{welcomeMessage.message}</p><div className="welcome-note"><Sparkles size={16} /> <span>Mock analysis is active while the API is being connected.</span></div></div>}
          {activeExchange && <><ChatBubble message={activeExchange.message} />{isLoading && activeExchange.id === activeId && <LoadingBubble />}{activeExchange.response && <ResultCard response={activeExchange.response} />}{errorId === activeExchange.id && <ErrorBubble onRetry={retry} />}</>}
          <div ref={threadEnd} />
        </div>
        <div ref={composer} onAnimationEnd={() => setIsComposerSettling(false)} className={`composer-area${hasChatStarted ? ' is-chatting' : ''}${isComposerSettling ? ' is-settling' : ''}`}><InputBar disabled={isLoading} onSubmit={submit} /><p className={`composer-hint rotating-copy ${composerHint.isVisible ? 'is-visible' : 'is-hidden'}`}>{composerHint.message}</p></div>
      </main>
    </div>
  </div>
}

export default App
