import { Button } from "@/components/ui/Button";

type Props = {
  search: string;
  onSearchChange: (value: string) => void;
  onAddPatient: () => void;
  onRefresh: () => void;
  isFetching: boolean;
};

export function PatientToolbar(props: Props) {
  return (
    <div className="toolbar toolbar-right">
      <input
        placeholder="Search patients"
        value={props.search}
        onChange={(e) => props.onSearchChange(e.target.value)}
      />
      <Button
        variant="secondary"
        onClick={() => void props.onRefresh()}
        disabled={props.isFetching}
      >
        Refresh
      </Button>
      <Button variant="primary" onClick={props.onAddPatient}>
        Add patient
      </Button>
    </div>
  );
}
