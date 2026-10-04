import { useEffect, useRef, useState } from 'react'
import '../App.css'

export default function App() {
  // --- Health fetch state ---
  const [fetchState, setFetchState] = useState('loading') // 'loading' | 'success' | 'error'
  const [health, setHealth] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  // --- Streaming state ---
  const [streamChunks, setStreamChunks] = useState([])
  const [streaming, setStreaming] = useState(false)
  const abortRef = useRef(null)

  // Fetch health on mount
  useEffect(() => {
    fetch('/api/health')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((data) => {
        setHealth(data)
        setFetchState('success')
      })
      .catch((err) => {
        setErrorMsg(err instanceof Error ? err.message : String(err))
        setFetchState('error')
      })
  }, [])

  async function handleStream() {
    if (streaming) {
      abortRef.current?.abort()
      return
    }

    setStreamChunks([])
    setStreaming(true)
    const controller = new AbortController()
    abortRef.current = controller

    try {
      const res = await fetch('/api/stream-test', { signal: controller.signal })
      if (!res.body) throw new Error('No response body')

      const reader = res.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        const text = decoder.decode(value, { stream: true })
        setStreamChunks((prev) => [...prev, text])
      }
    } catch (err) {
      if (err?.name !== 'AbortError') {
        setStreamChunks((prev) => [...prev, `[error: ${String(err)}]`])
      }
    } finally {
      setStreaming(false)
    }
  }

  return (
    <main id="main-content">
      <h1>College Club Knowledge Base</h1>
      <p className="subtitle">Milestone 0 — skeleton deployment check</p>

      <section id="health-section" aria-label="Health check">
        <h2>GET /api/health</h2>
        {fetchState === 'loading' && <p className="status loading">Loading…</p>}
        {fetchState === 'error' && (
          <p className="status error" role="alert">
            Error: {errorMsg}
          </p>
        )}
        {fetchState === 'success' && health && (
          <pre id="health-json" className="json-block">
            {JSON.stringify(health, null, 2)}
          </pre>
        )}
      </section>

      <section id="stream-section" aria-label="Streaming test">
        <h2>GET /api/stream-test</h2>
        <button
          id="stream-btn"
          onClick={() => void handleStream()}
          aria-busy={streaming}
        >
          {streaming ? 'Stop streaming' : 'Test streaming'}
        </button>

        {streamChunks.length > 0 && (
          <pre id="stream-output" className="json-block stream-output">
            {streamChunks.join('')}
          </pre>
        )}
      </section>
    </main>
  )
}
