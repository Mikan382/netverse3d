import { useEffect, useRef, useState } from 'react';
import type { InboxClient, InboxPage } from '../types/inbox.ts';
import { vi } from './text/vi.ts';
import styles from './inbox-panel.module.css';

const text = vi.inbox;
const REFRESH_MS = 30000;
const dateFormat = new Intl.DateTimeFormat('vi-VN', { dateStyle: 'medium', timeStyle: 'short' });

export default function InboxPanel({ client }: { client: InboxClient }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const activeLoad = useRef<AbortController | null>(null);
  const writing = useRef(false);
  const [open, setOpen] = useState(false);
  const [pageNumber, setPageNumber] = useState(1);
  const [page, setPage] = useState<InboxPage | null>(null);
  const [unread, setUnread] = useState<number | null>(null);
  const [failure, setFailure] = useState<'load' | 'write' | null>(null);
  const [saving, setSaving] = useState(false);
  const [request, setRequest] = useState(0);

  useEffect(() => {
    async function load() {
      if (document.visibilityState !== 'visible' || writing.current) return;
      activeLoad.current?.abort();
      const controller = new AbortController();
      activeLoad.current = controller;
      const { signal } = controller;
      try {
        const [count, latest] = await Promise.all([
          client.count(signal),
          open ? client.list(pageNumber, signal) : null,
        ]);
        if (signal.aborted) return;
        setUnread(count.count);
        if (latest) setPage(latest);
        setFailure((previous) => (previous === 'load' ? null : previous));
      } catch {
        if (!signal.aborted && open) setFailure('load');
      }
    }

    void load();
    const timer = setInterval(() => void load(), REFRESH_MS);
    document.addEventListener('visibilitychange', load);
    return () => {
      activeLoad.current?.abort();
      clearInterval(timer);
      document.removeEventListener('visibilitychange', load);
    };
  }, [client, open, pageNumber, request]);

  async function mark(id?: string) {
    if (writing.current) return;
    writing.current = true;
    activeLoad.current?.abort();
    setSaving(true);
    setFailure(null);
    try {
      if (id) await client.markRead(id);
      else await client.markAllRead();
      setRequest((current) => current + 1);
    } catch {
      setFailure('write');
    } finally {
      writing.current = false;
      setSaving(false);
    }
  }

  const current = page?.page === pageNumber ? page : null;
  const hasUnread = unread !== null && unread > 0;

  return (
    <>
      <button
        className={styles.toggle}
        type="button"
        aria-label={hasUnread ? text.withUnread(unread) : text.title}
        aria-haspopup="dialog"
        onClick={() => {
          setPageNumber(1);
          setFailure(null);
          setOpen(true);
          dialog.current?.showModal();
        }}
      >
        {text.title}
        {hasUnread && (
          <span className={styles.badge} aria-hidden="true">
            {unread > 99 ? '99+' : unread}
          </span>
        )}
      </button>
      <dialog
        ref={dialog}
        className={styles.dialog}
        aria-labelledby="inbox-title"
        aria-busy={saving}
        onClose={() => setOpen(false)}
        onKeyDown={(event) => event.stopPropagation()}
      >
        <header className={styles.header}>
          <h2 id="inbox-title">{text.title}</h2>
          <button type="button" aria-label={text.close} onClick={() => dialog.current?.close()}>
            ×
          </button>
        </header>
        <div className={styles.toolbar}>
          <p role="status">{unread !== null && text.unread(unread)}</p>
          <button type="button" disabled={!hasUnread || saving} onClick={() => void mark()}>
            {text.readAll}
          </button>
        </div>
        {failure && (
          <div className={styles.feedback}>
            <p role="alert">{failure === 'load' ? text.loadError : text.markError}</p>
            <button
              type="button"
              onClick={() => {
                setFailure(null);
                setRequest((value) => value + 1);
              }}
            >
              {text.retry}
            </button>
          </div>
        )}
        {!current && !failure && (
          <p role="status" className={styles.feedback}>
            {text.loading}
          </p>
        )}
        {current &&
          (current.content.length === 0 ? (
            <p className={styles.feedback}>{text.empty}</p>
          ) : (
            <ul className={styles.list}>
              {current.content.map((item) => (
                <li className={styles.item} key={item.id} data-unread={item.readAt === null}>
                  <h3>{item.title}</h3>
                  <p>{item.body}</p>
                  <div className={styles.meta}>
                    <time dateTime={item.createdAt}>
                      {dateFormat.format(new Date(item.createdAt))}
                    </time>
                    {item.readAt === null && (
                      <button type="button" disabled={saving} onClick={() => void mark(item.id)}>
                        {text.markRead}
                      </button>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          ))}
        {current && current.totalPages > 1 && (
          <nav className={styles.pagination} aria-label={text.pages}>
            <button
              type="button"
              disabled={pageNumber === 1 || saving}
              onClick={() => setPageNumber(pageNumber - 1)}
            >
              {text.previous}
            </button>
            <span>{text.page(pageNumber, current.totalPages)}</span>
            <button
              type="button"
              disabled={pageNumber >= current.totalPages || saving}
              onClick={() => setPageNumber(pageNumber + 1)}
            >
              {text.next}
            </button>
          </nav>
        )}
      </dialog>
    </>
  );
}
