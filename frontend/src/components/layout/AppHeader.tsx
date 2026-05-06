import { Button } from "@/components/ui/Button";

type Props = {
  showLogout: boolean;
  onLogout: () => void;
};

export function AppHeader(props: Props) {
  return (
    <header className="header">
      <div>
        <h1>Patient management</h1>
        <p className="muted">Patients for your clinic only.</p>
      </div>
      {props.showLogout && (
        <Button variant="secondary" onClick={props.onLogout}>
          Log out
        </Button>
      )}
    </header>
  );
}
