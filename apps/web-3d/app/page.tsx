import ShopView from './shop-view.tsx';
import AccountEntry from './account-entry.tsx';
import PwaActions from '../src/ui/pwa-actions.tsx';

export default function Page() {
  return (
    <>
      <ShopView />
      <AccountEntry />
      <PwaActions />
    </>
  );
}
