import { Button } from "@/components/ui/Button";
import type { Patient } from "@/services/patientsApi";

type Props = {
  patient: Patient;
  deleting: boolean;
  error: string | null;
  onClose: () => void;
  onConfirm: () => void;
};

export function DeletePatientModal(props: Props) {
  return (
    <div
      className="modal-backdrop"
      role="presentation"
      onClick={() => {
        if (!props.deleting) props.onClose();
      }}
    >
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-modal-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <h2 id="delete-modal-title">Delete patient</h2>
          <Button variant="icon" onClick={props.onClose} aria-label="Close" disabled={props.deleting}>
            ×
          </Button>
        </div>
        <form
          className="form"
          onSubmit={(e) => {
            e.preventDefault();
            props.onConfirm();
          }}
        >
          <p>
            Are you sure you want to delete{" "}
            <strong>
              {props.patient.first_name} {props.patient.last_name}
            </strong>
            ?
          </p>
          {props.error && <p className="error">{props.error}</p>}
          <div className="modal-actions">
            <Button variant="secondary" onClick={props.onClose} disabled={props.deleting}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" danger disabled={props.deleting}>
              {props.deleting ? "Deleting…" : "Delete"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
