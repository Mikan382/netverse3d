import { identityApi, IdentityError, type AccountProfile } from './identity-api.ts';

const STORAGE_KEY = 'netverse.identity.refresh';
const RETRY_MS = 15000;
const ended = new Set([
  'COMMON.UNAUTHENTICATED',
  'IDENTITY.ACCOUNT_SUSPENDED',
  'IDENTITY.REFRESH_INVALID',
  'IDENTITY.REFRESH_REUSED',
  'IDENTITY.SESSION_REVOKED',
]);

type SessionView = {
  checking: boolean;
  profile: AccountProfile | null;
  retryAt: number | null;
  error: string | null;
};

const INITIAL: SessionView = { checking: true, profile: null, retryAt: null, error: null };
const SIGNED_OUT: SessionView = { ...INITIAL, checking: false };

type TokenPair = Awaited<ReturnType<typeof identityApi.login>>;

export function createIdentitySession() {
  let view = INITIAL;
  const listeners = new Set<() => void>();
  let refreshToken: string | null = null;
  let expiresAt = 0;
  let revision = 0;
  let started = false;
  let pendingRefresh: Promise<void> | null = null;

  function publish(next: SessionView) {
    view = next;
    for (const listen of listeners) listen();
  }

  function remember(next: string | null) {
    refreshToken = next;
    try {
      if (next) sessionStorage.setItem(STORAGE_KEY, next);
      else sessionStorage.removeItem(STORAGE_KEY);
    } catch {
      return;
    }
  }

  function forget(error: string | null = null) {
    revision += 1;
    remember(null);
    expiresAt = 0;
    publish({ ...SIGNED_OUT, error });
  }

  async function accept(pair: TokenPair, turn: number, knownProfile: AccountProfile | null) {
    if (revision !== turn) return;
    remember(pair.refreshToken);
    const lifetime = pair.expiresIn * 1000;
    expiresAt = Date.now() + lifetime;
    const profile = knownProfile ?? (await identityApi.profile(pair.accessToken));
    if (revision !== turn) return;
    publish({
      checking: false,
      profile,
      retryAt: expiresAt - Math.min(60000, lifetime / 5),
      error: null,
    });
  }

  function refresh() {
    if (pendingRefresh) return pendingRefresh;
    if (!refreshToken) return Promise.resolve();
    const turn = revision;
    pendingRefresh = identityApi
      .refresh(refreshToken)
      .then((pair) => accept(pair, turn, view.profile))
      .catch((error: unknown) => {
        if (revision !== turn) return;
        const code = error instanceof IdentityError ? error.code : 'CLIENT.UNAVAILABLE';
        if (ended.has(code)) {
          forget(code);
          return;
        }
        const now = Date.now();
        const profile = expiresAt > now ? view.profile : null;
        publish({
          checking: false,
          profile,
          retryAt: profile ? Math.min(now + RETRY_MS, expiresAt) : now + RETRY_MS,
          error: profile ? null : code,
        });
      })
      .finally(() => {
        pendingRefresh = null;
      });
    return pendingRefresh;
  }

  return {
    snapshot: () => view,
    serverSnapshot: () => INITIAL,
    subscribe(listener: () => void) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    restore() {
      if (started) return;
      started = true;
      try {
        refreshToken = sessionStorage.getItem(STORAGE_KEY);
      } catch {
        refreshToken = null;
      }
      if (refreshToken) void refresh();
      else publish(SIGNED_OUT);
    },
    refresh,
    async login(email: string, password: string) {
      const turn = ++revision;
      const pair = await identityApi.login(email, password);
      try {
        await accept(pair, turn, null);
      } catch (error) {
        if (revision === turn) forget();
        await identityApi.logout(pair.refreshToken).catch(() => undefined);
        throw error;
      }
    },
    async logout() {
      const previous = refreshToken;
      forget();
      if (previous) await identityApi.logout(previous);
    },
  };
}
