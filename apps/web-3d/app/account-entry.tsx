'use client';

import { useEffect, useState, useSyncExternalStore } from 'react';
import { identityApi } from '../src/net/identity-api.ts';
import { createIdentitySession } from '../src/net/identity-session.ts';
import AccountPanel from '../src/ui/account-panel.tsx';
import { vi } from '../src/ui/text/vi.ts';

export default function AccountEntry() {
  const [session] = useState(createIdentitySession);
  const { checking, profile, retryAt, error } = useSyncExternalStore(
    session.subscribe,
    session.snapshot,
    session.serverSnapshot,
  );

  useEffect(() => session.restore(), [session]);

  useEffect(() => {
    if (retryAt === null) return;
    const timer = setTimeout(() => void session.refresh(), Math.max(0, retryAt - Date.now()));
    return () => clearTimeout(timer);
  }, [retryAt, session]);

  return (
    <AccountPanel
      checking={checking}
      account={
        profile ? { label: profile.displayName || profile.email || vi.account.signedIn } : null
      }
      sessionError={error}
      actions={{
        login: ({ email, password }) => session.login(email, password),
        register: ({ email, password, displayName }) =>
          identityApi.register(email, password, displayName),
        verify: ({ email, code }) => identityApi.verify(email, code),
        forgot: ({ email }) => identityApi.forgot(email),
        reset: ({ email, code, password }) => identityApi.reset(email, code, password),
      }}
      resend={identityApi.resend}
      logout={session.logout}
    />
  );
}
