import { useEffect, useRef, useState, type FormEvent, type ReactNode } from 'react';
import { vi } from './text/vi.ts';
import styles from './account-panel.module.css';

type Mode = 'login' | 'register' | 'verify' | 'forgot' | 'reset';
type Fields = { email: string; password: string; code: string; displayName: string };
type Actions = Record<Mode, (fields: Fields) => Promise<unknown>>;

type Props = {
  checking: boolean;
  account: { label: string } | null;
  sessionError: string | null;
  actions: Actions;
  resend: (email: string) => Promise<unknown>;
  logout: () => Promise<void>;
  children?: ReactNode;
};

const text = vi.account;
const nextMode: Record<Exclude<Mode, 'login'>, Mode> = {
  register: 'verify',
  verify: 'login',
  forgot: 'reset',
  reset: 'login',
};

function messageFor(error: unknown) {
  const code = error instanceof Error ? error.message : '';
  return Object.hasOwn(text.errors, code)
    ? text.errors[code as keyof typeof text.errors]
    : text.errors['CLIENT.UNAVAILABLE'];
}

export default function AccountPanel({
  checking,
  account,
  sessionError,
  actions,
  resend,
  logout,
  children,
}: Props) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState<Mode>('login');
  const [email, setEmail] = useState('');
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  useEffect(() => {
    const dialog = dialogRef.current;
    if (open && dialog && !dialog.open) dialog.showModal();
    else if (!open && dialog?.open) dialog.close();
  }, [open]);

  useEffect(() => {
    if (!open) return;
    dialogRef.current?.querySelector<HTMLInputElement>('[data-account-focus]')?.focus();
  }, [mode, open]);

  function changeMode(next: Mode, message = '') {
    const input = dialogRef.current?.querySelector<HTMLInputElement>('[name="email"]');
    if (input) setEmail(input.value.trim());
    setMode(next);
    setError('');
    setNotice(message);
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (pending) return;
    const data = new FormData(event.currentTarget);
    const fields = {
      email: String(data.get('email') ?? '').trim(),
      password: String(data.get('password') ?? ''),
      code: String(data.get('code') ?? '').trim(),
      displayName: String(data.get('displayName') ?? '').trim(),
    };
    setEmail(fields.email);
    setPending(true);
    setError('');
    setNotice('');
    try {
      await actions[mode](fields);
      if (mode === 'login') setOpen(false);
      else changeMode(nextMode[mode], text.notices[mode]);
    } catch (reason) {
      if (
        mode === 'login' &&
        reason instanceof Error &&
        reason.message === 'IDENTITY.EMAIL_NOT_VERIFIED'
      ) {
        changeMode('verify');
      }
      setError(messageFor(reason));
    } finally {
      setPending(false);
    }
  }

  async function resendCode() {
    if (pending) return;
    setPending(true);
    setError('');
    setNotice('');
    try {
      await resend(email);
      setNotice(text.notices.register);
    } catch (reason) {
      setError(messageFor(reason));
    } finally {
      setPending(false);
    }
  }

  async function signOut() {
    setEmail('');
    setMode('login');
    setError('');
    setNotice('');
    setOpen(true);
    setPending(true);
    try {
      await logout();
    } catch {
      setError(text.logoutError);
    } finally {
      setPending(false);
    }
  }

  const needsCode = mode === 'verify' || mode === 'reset';
  const needsNewPassword = mode === 'register' || mode === 'reset';

  return (
    <>
      <div className={styles.accountBar} role="group" aria-label={text.accountLabel}>
        {account && <span className={styles.accountName}>{account.label}</span>}
        {account ? (
          <button className={styles.outline} type="button" onClick={signOut}>
            {text.signOut}
          </button>
        ) : (
          <button
            className={styles.outline}
            type="button"
            aria-haspopup="dialog"
            disabled={checking}
            onClick={() => {
              changeMode('login');
              if (sessionError) setError(messageFor(new Error(sessionError)));
              setOpen(true);
            }}
          >
            {checking ? text.checking : text.actions.login}
          </button>
        )}
        {children}
      </div>
      <dialog
        ref={dialogRef}
        className={styles.dialog}
        aria-labelledby="account-title"
        onKeyDown={(event) => event.stopPropagation()}
        onCancel={(event) => {
          event.preventDefault();
          if (!pending) setOpen(false);
        }}
      >
        {open && (
          <>
            <header className={styles.header}>
              <h1 id="account-title">{text.titles[mode]}</h1>
              <button
                className={styles.close}
                type="button"
                aria-label={text.close}
                disabled={pending}
                onClick={() => setOpen(false)}
              >
                ×
              </button>
            </header>
            <form key={mode} className={styles.form} onSubmit={submit} aria-busy={pending}>
              <label className={styles.field}>
                {text.email}
                <input
                  type="email"
                  name="email"
                  autoComplete="username"
                  defaultValue={email}
                  maxLength={320}
                  required
                  readOnly={needsCode || pending}
                  data-account-focus={!needsCode || undefined}
                />
              </label>
              {mode === 'register' && (
                <label className={styles.field}>
                  {text.displayName}
                  <input
                    name="displayName"
                    autoComplete="nickname"
                    maxLength={120}
                    readOnly={pending}
                  />
                </label>
              )}
              {needsCode && (
                <label className={styles.field}>
                  {text.code}
                  <input
                    name="code"
                    inputMode="numeric"
                    autoComplete="one-time-code"
                    pattern="[0-9]{6}"
                    maxLength={6}
                    required
                    readOnly={pending}
                    data-account-focus
                  />
                </label>
              )}
              {(mode === 'login' || needsNewPassword) && (
                <label className={styles.field}>
                  {needsNewPassword ? text.newPassword : text.password}
                  <input
                    type="password"
                    name="password"
                    autoComplete={needsNewPassword ? 'new-password' : 'current-password'}
                    minLength={needsNewPassword ? 8 : undefined}
                    maxLength={72}
                    required
                    readOnly={pending}
                  />
                  {needsNewPassword && <span>{text.passwordHint}</span>}
                </label>
              )}
              {error && (
                <p className={styles.error} role="alert">
                  {error}
                </p>
              )}
              {notice && (
                <p className={styles.notice} role="status">
                  {notice}
                </p>
              )}
              <button type="submit" className={styles.primary} disabled={pending}>
                {pending ? text.processing : text.actions[mode]}
              </button>
            </form>
            <div className={styles.links}>
              {mode === 'login' ? (
                <>
                  <button type="button" disabled={pending} onClick={() => changeMode('register')}>
                    {text.actions.register}
                  </button>
                  <button type="button" disabled={pending} onClick={() => changeMode('forgot')}>
                    {text.titles.forgot}
                  </button>
                </>
              ) : (
                <button type="button" disabled={pending} onClick={() => changeMode('login')}>
                  {text.backToLogin}
                </button>
              )}
              {mode === 'verify' && (
                <button type="button" disabled={pending} onClick={resendCode}>
                  {text.resend}
                </button>
              )}
              {mode === 'reset' && (
                <button type="button" disabled={pending} onClick={() => changeMode('forgot')}>
                  {text.resend}
                </button>
              )}
            </div>
          </>
        )}
      </dialog>
    </>
  );
}
